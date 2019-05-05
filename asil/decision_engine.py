from math import sqrt
from random import randint
from power_puff_boys.node_utilities import *
from power_puff_boys.priority_queue import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT                  = (999, 999)
    colour                = None
    exit_nodes            = None
    open_node_combs       = None
    init_node_comb        = None
    closed_node_combs     = None
    open_node_combs_queue = None
    states                = None

    def __init__(self, colour, board):

        self.colour      = colour
        self.exit_nodes  = board.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_next_move(self, board):
        """
        Returns a random move out of the list of valid moves.
        """

        nodes = board.get_piece_nodes(self.colour)

        # generate all possible moves
        possible_successors = self.get_all_possible_moves(board, nodes)
        
        # no moves possible
        if len(possible_successors) == 0:
            return ("PASS", None)

        # pick a random move
        action = possible_successors[randint(0, len(possible_successors) - 1)]

        if action[1] == self.EXIT:
            return ("EXIT", action[0])
        else:
            if board.get_dist(action[0], action[1]) <= sqrt(2):
                return ("MOVE", action)
            return ("JUMP", action)


    def get_all_possible_moves(self, board, nodes):
        """
        Returns a list of all the possible nodes that can be moved to. An exit 
        is denoted by (999, 999).
        """

        possible_moves = []
        occupied_nodes = board.get_all_piece_nodes()        

        for node in nodes:

            # check if an exit is one of the possible moves
            if node in self.exit_nodes:
                possible_moves.append((node, self.EXIT))
            
            # add neighbouring nodes to list
            for neighbouring_node in board.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node = board.get_landing_node(node, neighbouring_node, occupied_nodes)
                    if (landing_node):
                        possible_moves.append((node, landing_node))
                
                else:
                    possible_moves.append((node, neighbouring_node))

        return possible_moves
        
            







    