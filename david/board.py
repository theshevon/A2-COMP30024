from math import sqrt
from david.game_state import *

class Board():

    SIZE    = 3

    COLOURS = { "red", "green", "blue" }
    
    # starting nodes for the different teams
    START_NODES = {
                        "red"   : { (-3,0), (-3,1),  (-3,2),  (-3,3) },
                        "blue"  : {  (0,3),  (1,2),   (2,1),   (3,0) },
                        "green" : { (0,-3), (1,-3),  (2,-3),  (3,-3) }
                  }

    # initial exit counts for the different teams
    START_EXIT_COUNTS = {
                            "red"   : 0,
                            "blue"  : 0,
                            "green" : 0
                        }

    # exit nodes for the different teams
    EXIT_NODES  =   {
                        "red"   : { (3,-3), (3,-2),  (3,-1),  (3,0)  },
                        "blue"  : { (-3,0), (-2,-1), (-1,-2), (0,-3) },
                        "green" : { (-3,3), (-2,3),  (-1,3),  (0,3)  }
                    }

    # coefficents for lines through exits (cf[0]q + cf[1]r + cf[2] = 0) 
    EXIT_LINE_CFS = {   
                        "blue"  : (1, 1, 3), 
                        "red"   : (1, 0, -3), 
                        "green" : (0, 1, -3) 
                    }

    EXIT_NODE     = (999, 999)

    current_state = None
    
    def __init__(self):
        self.current_state = GameState(self.START_NODES, self.START_EXIT_COUNTS)
                        
    def update_state(self, colour, action):
        """
        Updates the position of a piece after a move was taken.
        """

        # a pass action does not require any updating        
        if action[0] == "PASS":
            return 

        action = list(action)
        action[1] = list(action[1])
    
        
        if action[0] == "EXIT_NODE":
            self.current_state.piece_nodes[colour].discard(action[1])
            return

        # and if the move wasn't an exit update the set to reflect the pieces 
        # new location
        if (action[0] == "MOVE") or (action[0] == "JUMP"):
            
            self.current_state.piece_nodes[colour].add(action[1][1])
            self.current_state.piece_nodes[colour].discard(action[1][0])

        # check if a piece got cut
        if action[0] == "JUMP":
            # get the node that was jumped over
            q = int((action[1][1][0] + action[1][0][0]) / 2)
            r = int((action[1][1][1] + action[1][0][1]) / 2)
            jumped_over_node = (q, r)
            self.current_state.change_piece_node(jumped_over_node, colour)
                
    def get_piece_nodes(self, state, colour):
        """
        Returns a set containing the nodes occupied by pieces of a specified 
        colour.
        """
        
        return state.piece_nodes[colour]

    def get_landing_node(self, curr_node, node_to_jump_over, blocked_nodes):
        """
        Returns the landing node when when jumping from one node over another.
        Returns None if the landing node is not on the board (i.e. a jump 
        isn't possible).
        """

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_node = (q, r)
        return landing_node if (self.is_on_board(landing_node) and (landing_node not in blocked_nodes)) else None

    def get_exit_nodes(self, colour):
        """
        Returns the set of exit nodes for a particular colour.
        """

        return self.EXIT_NODES[colour]

    def is_on_board(self, node):
        """
        Returns True if a node is within the board.
        """

        ran = range(-self.SIZE, self.SIZE+1)
        return (node[0] in ran) and (node[1] in ran) and (-node[0]-node[1] in ran)

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
        Returns a list of all the possible moves in the form of a triple where
        index
            0: corresponds to the starting node
            1: corresponds to the final node (An exit is denoted by (999, 999)
            2: corresponds to a node occupied by a piece that was jumped over
               nodes that can be moved to. An exit 
        """    

        possible_moves = []
        occupied_nodes = state.get_all_piece_nodes()        

        for node in state.piece_nodes[colour]:

            # check if an exit is one of the possible moves
            if node in self.EXIT_NODES[colour]:
                possible_moves.append((node, self.EXIT_NODE, None))
            
            # add neighbouring nodes to list
            for neighbouring_node in self.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node = self.get_landing_node(node, neighbouring_node, occupied_nodes)
                    if landing_node:
                        possible_moves.append((node, landing_node , neighbouring_node))
                
                else:
                    possible_moves.append((node, neighbouring_node, None))

        return possible_moves        

    def get_all_successor_states(self, state, colour):
        """
        Returns a list of all the possible states that can be moved to.
        
        """

        jump_states  =[]
        exit_states = []
        move_states = []

        for moved_from, moved_to, piece_jumped in self.get_all_possible_moves(state, colour):

            temp_state = state.copy()

            # remove the piece that moved
            temp_state.piece_nodes[colour].discard(moved_from)

            # if pieces hasn't exited add moved_to
            if moved_to == self.EXIT_NODE:
                temp_state.exit_counts[colour] += 1
                exit_states.append(temp_state)
            else:
                temp_state.piece_nodes[colour].add(moved_to)

            # check if a new piece has been gained
            if piece_jumped:
                temp_state.change_piece_node(piece_jumped, colour)
                jump_states.append(temp_state)
            else:
                move_states.append(temp_state)

        possible_states = exit_states + jump_states + move_states
        
        # if no move is available, the child state is the current state
        if not possible_states:
            return [state]

        return possible_states

    def get_min_no_of_moves_to_exit(self, node, colour):

        """
        Returns the minimum possible moves from a node to an exit nodes.
        """
        
        cfs = self.EXIT_LINE_CFS[colour]
        
        # shortest number of 'move' actions to reach an exit node
        n_min_moves = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

        return n_min_moves

    def get_dist(self, node_1, node_2):
        """
        Returns the Euclidean distance between two nodes.
        """

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)