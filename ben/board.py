from math import sqrt
from copy import deepcopy
from ben.game_state import *

class Board:
    """
    Represents the Chexers board, which is considered to be composed of nodes.
    """

    SIZE = 3

    # starting nodes for the different teams
    START_NODES =  {
                        "red"   : { (-3,0), (-3,1),  (-3,2),  (-3,3) },
                        "blue"  : {  (0,3),  (1,2),   (2,1),   (3,0) },
                        "green" : { (0,-3), (1,-3),  (2,-3),  (3,-3) }
                   }

    # exit nodes for the different teams
    EXIT_NODES  =  {
                        "red"   : { (3,-3),  (3,-2),  (3,-1),  (3,0) },
                        "blue"  : { (-3,0), (-2,-1), (-1,-2), (0,-3) },
                        "green" : { (-3,3),  (-2,3),  (-1,3),  (0,3) }
                   }

    # coefficents for lines through exits (cf[0]q + cf[1]r + cf[2] = 0) 
    EXIT_LINE_CFS = {   
                        "blue"  : (1, 1, 3), 
                        "red"   : (1, 0, -3), 
                        "green" : (0, 1, -3) 
                    }

    TEAMS = { "red" , "blue", "green" }

    game_state  = None

    def __init__(self):
       
       exit_counts = { "red" : 0, "blue" : 0, "green" : 0 }
       self.game_state = GameState(self.START_NODES, exit_counts)

    def get_game_state(self):
        """
        Returns the current game state.
        """

        return deepcopy(self.game_state)

    def get_exit_nodes(self, colour):
        """
        Returns the set of exit nodes for a particular colour.
        """

        return self.EXIT_NODES[colour]

    def update_board(self, colour, action):
        """
        Updates the game state after a player performs an action.
        """

        self.game_state.update(colour, action)

    def get_piece_nodes(self, colour):
        """
        Returns a set containing the nodes occupied by pieces of a specified 
        colour.
        """
        
        return self.game_state.get_team_piece_nodes(colour)

    def get_all_piece_nodes(self):
        """
        Returns a set containing the nodes occupied by all the pieces on the 
        board.
        """

        return self.game_state.get_all_piece_nodes()

    def get_landing_node(self, curr_node, node_to_jump_over):
        """
        Returns the landing node when when jumping from one node over another.
        Returns None if the landing node is not on the board (i.e. a jump 
        isn't possible).
        """

        occupied_nodes = self.get_all_piece_nodes()

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_node = (q,r)

        return landing_node if ((self.is_on_board(landing_node)) and \
                                (landing_node not in occupied_nodes)) else None

    def is_on_board(self, node):
        """
        Returns True if a node is within the board.
        """
       
        ran = range(-self.SIZE, self.SIZE+1)
        return node in [(q,r) for q in ran for r in ran if -q-r in ran]

    def get_euclidean_distance(self, node_1, node_2):
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
        r_end   = node[1] + 2
        col = 0
        for q in range(node[0]-1, node[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)

                if (possible_neighbour != node) and \
                                        (self.is_on_board(possible_neighbour)):
                    neighbours.append(possible_neighbour)

            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def get_min_no_of_moves_to_exit(self, node, colour):
        """
        Returns the minimum possible moves from a node to an exit nodes.
        """
        
        cfs = self.EXIT_LINE_CFS[colour]
        
        # shortest number of 'move' actions to reach an exit node
        n_min_moves = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

        return n_min_moves

