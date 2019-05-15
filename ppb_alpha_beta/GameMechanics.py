from math import sqrt

class GameMechanics():

    # starting nodes for the different teams
    start_nodes = {
                        "red"   : { (-3,0), (-3,1),  (-3,2),  (-3,3) },
                        "blue"  : {  (0,3),  (1,2),   (2,1),   (3,0) },
                        "green" : { (0,-3), (1,-3),  (2,-3),  (3,-3) }
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
                state.piece_nodes[colour].discard(action[1])

            # and if the move wasn't an exit update the set to reflect the pieces 
            # new location
            if (action[0] == "MOVE") or (action[0] == "JUMP"):
                state.piece_nodes[colour].add(action[1][1])
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
                state.piece_nodes[colour].discard(node)
                state.piece_nodes[new_colour].add(node)
                return

    def get_piece_nodes(self, state, colour):
        """
        Returns a set containing the nodes occupied by pieces of a specified 
        colour.
        """
        
        return state.piece_nodes[colour]

    def get_all_piece_nodes(self, state , colour):
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
        occupied_nodes = self.get_all_piece_nodes(state, colour)        

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
                        possible_moves.append((node, landing_node , neighbouring_node))
                
                else:
                    possible_moves.append((node, neighbouring_node, None))

        return possible_moves        

    def get_all_possible_states(self, state, colour):
        """
        Returns a list of all the possible states that can be moved to.
        
        """
        possible_states = []
        temp_state = dict()
        for moved_from , moved_to, piece_jumped in get_all_possible_moves(state, colour):
            temp_state = state
            #moves the piece
            temp_state.piece_nodes[colour].discard(moved_from) 
            temp_state.piece_nodes[colour].add(moved_to)
            #checks if a new piece has been gained
            if( piece_jumped):
                change_piece_node(state , piece_jumped, colour)

        return possible_states