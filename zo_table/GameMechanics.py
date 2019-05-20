from math import sqrt
from zo_table.game_state import *
from zo_table.zobrist_keys import *
import copy
class GameMechanics():
    zobrist = Zobrist()

    # starting nodes for the different teams
    start_nodes = {
                        "red"   : { (-3,0), (-3,1),  (-3,2),  (-3,3) },
                        "blue"  : {  (0,3),  (1,2),   (2,1),   (3,0) },
                        "green" : { (0,-3), (1,-3),  (2,-3),  (3,-3) }
                  }

    start_exit_counts = {
                        "red"   : 0,
                        "blue"  : 0,
                        "green" : 0
                  }

    # exit nodes for the different teams
    exit_nodes  =  {
                        "red"   : { (3,-3), (3,-2),  (3,-1),  (3,0)  },
                        "blue"  : { (-3,0), (-2,-1), (-1,-2), (0,-3) },
                        "green" : { (-3,3), (-2,3),  (-1,3),  (0,3)  }
                    }

                        
    def update_node(self, state,  colour, action):
            """
            Updates the position of a piece after a move was taken.
            """

            # a pass action does not require any updating        
            if action[0] == "PASS":
                return 
            
            if action[0] == "EXIT":

                self.zobrist.apply_piece(state, action[1],colour)
                state.piece_nodes[colour].discard(action[1])
                #increase the exit ccount by one
                self.zobrist.increase_exit(state, state.exit_counts[colour]+ 1 ,colour)
                state.exit_counts[colour] +=1
            # and if the move wasn't an exit update the set to reflect the pieces 
            # new location
            if (action[0] == "MOVE") or (action[0] == "JUMP"):
                self.zobrist.apply_piece(state, action[1][1],colour)
                state.piece_nodes[colour].add(action[1][1])
                self.zobrist.apply_piece(state, action[1][0], colour)
                state.piece_nodes[colour].discard(action[1][0])

            # check if a piece got cut
            if action[0] == "JUMP":
                # get the node that was jumped over
                q = int((action[1][1][0] + action[1][0][0]) / 2)
                r = int((action[1][1][1] + action[1][0][1]) / 2)
                jumped_over_node = (q, r)
                self.change_piece_node( state, jumped_over_node, colour)
 
                
    def change_piece_node(self, state , node, new_colour):
        """
        Changes the assignment of a node to a different colour, provided that
        a piece has been cut.
        """
        
        for colour in state.piece_nodes:
            if node in state.piece_nodes[colour]:
                self.zobrist.apply_piece(state, node, colour)
                state.piece_nodes[colour].discard(node)
                self.zobrist.apply_piece(state, node, new_colour)
                state.piece_nodes[new_colour].add(node)
                return

    def get_piece_nodes(self, state, colour):
        """
        Returns a set containing the nodes occupied by pieces of a specified 
        colour.
        """
        
        return state.piece_nodes[colour]

    def get_all_piece_nodes(self, state):
        """
        Returns a set containing the nodes occupied by all the pieces on the 
        board.
        """

        piece_nodes = set()
        for colour in state.piece_nodes:
            piece_nodes = piece_nodes.union(state.piece_nodes[colour])

        return piece_nodes

    def get_landing_node(self, curr_node, node_to_jump_over, blocked_nodes):
        """
        Returns the landing node when when jumping from one node over another.
        Returns None if the landing node is not on the board (i.e. a jump 
        isn't possible).
        """

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_node = (q,r)

        return landing_node if (self.is_on_board(landing_node) and (landing_node not in blocked_nodes)) else None

    def get_exit_nodes(self, colour):
        """
        Returns the set of exit nodes for a particular colour.
        """

        return self.exit_nodes[colour]
    #Need to update
    def is_on_board(self, coord):
        """
        Returns True if a node is within the board.
        """
        board_size = 3 
        ran = range(-board_size, board_size + 1)
        if (coord[0] in ran) and (coord[1] in ran) and (-coord[0] - coord[1] in ran):
            return True
        else:
            return False            

    def get_dist(self,  node_1, node_2):
        """
        Returns the Euclidean distance between two nodes.
        """

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)

    def get_neighbouring_nodes(self, node):
        """
        Returns a list of possible neighbouring nodes.
        """

        neighbours = []

        r_start = node[1]
        r_end = node[1] + 2
        col = 0
        for q in range(node[0]-1, node[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)

                if (possible_neighbour != node) and (self.is_on_board(possible_neighbour)) :
                    neighbours.append(possible_neighbour)

            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def get_all_possible_moves(self, state, colour):
        """
        Returns a list of all the possible nodes that can be moved to. An exit 
        is denoted by (999, 999).
        """
        #piece jumped set to none if action MOVE or EXIT
        #( moved_from , moved_to , piece_jumped)

        possible_moves = []
        occupied_nodes = self.get_all_piece_nodes(state)        

        for node in state.piece_nodes[colour]:

            # check if an exit is one of the possible moves
            if node in self.exit_nodes[colour]:
                possible_moves.append((node, (999,999)))

            # add neighbouring nodes to list
            for neighbouring_node in self.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node = self.get_landing_node(node, neighbouring_node, occupied_nodes)
                    if (landing_node):
                        possible_moves.append((node, landing_node))
                
                else:
                    possible_moves.append((node, neighbouring_node))

        if len(possible_moves) == 0:
            possible_moves.append(((999,999), (999,999)))
        return possible_moves        

    def get_all_possible_states(self, state, colour):
        """
        Returns a list of all the possible states that can be moved to.
        
        """
        jump_states  =[]
        exit_states = []
        move_states = []

        for action in self.get_all_possible_moves(state, colour):
            move = self.get_move_from_tuple(action)
            temp_state = state.copy()
            self.update_node(temp_state, colour, move)
            if move[0]== "JUMP":
                jump_states.append((temp_state, action))
            elif move[0]== "MOVE":
                move_states.append((temp_state, action))
            elif move[0]== "EXIT":
                move_states.append((temp_state, action))
            elif move[0]== "PASS":
                move_states.append((temp_state, action))
        #ordered to promote high scoring states first 
        return exit_states + jump_states + move_states

    def initialise_board(self):
        state = State(self.start_nodes , self.start_exit_counts, 0)


        for colour in  state.piece_nodes:

            for piece in state.piece_nodes[colour]:
                self.zobrist.apply_piece(state, piece ,colour)
            #print(state.z_key)

            self.zobrist.apply_exit(state, state.exit_counts[colour], colour)

        return state

    def get_dist(self,  node_1, node_2):
        """
        Returns the Euclidean distance between two nodes.
        """

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)


    def get_move_from_tuple(self, action):
        #
        if(action[0] == (999,999) ):
            return ("PASS", None)
        elif(action[1] == (999,999)):
            #print("exit")
            return ("EXIT" , action[0])

        elif(self.get_dist(action[0], action[1]) <= sqrt(2)):
            return ("MOVE", action)
        else:
            return ("JUMP", action)