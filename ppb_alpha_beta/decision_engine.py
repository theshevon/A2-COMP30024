from math import sqrt
from random import randint
from ppb_alpha_beta.node_utilities import *
from ppb_alpha_beta.priority_queue import *

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

    def __init__(self, colour, game_mechanics):

        self.colour      = colour
        self.exit_nodes  = game_mechanics.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_next_move(self, state, game_mechanics):
        """
        Returns a random move out of the list of valid moves.
        """

        # generate all possible moves
        possible_successors = game_mechanics.get_all_possible_moves(state, self.colour)
        
        # no moves possible
        if len(possible_successors) == 0:
            return ("PASS", None)

        # pick a random move
        action = possible_successors[randint(0, len(possible_successors) - 1)]
        action = (action[0], action[1])
        if action[1] == self.EXIT:
            return ("EXIT", action[0])
        else:
            if game_mechanics.get_dist(action[0], action[1]) <= sqrt(2):
                return ("MOVE", action)
            return ("JUMP", action)

            







    