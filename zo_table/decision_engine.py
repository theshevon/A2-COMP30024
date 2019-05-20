from math import sqrt
from random import randint
from zo_table.game_state import *
from zo_table.GameMechanics import *
from zo_table.min_max import *

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

    game_mechanics = GameMechanics()
    min_max = MIN_MAX()
    DEPTH = 5
    def __init__(self, colour):

        self.colour      = colour
        self.exit_nodes  = self.game_mechanics.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_next_move(self, state):
        """
        Uses min max to determin next move.
        """
        #print(state.piece_nodes)
        value , move = self.min_max.alpha_beta( state , self.DEPTH , float("-inf") , float("+inf") , self.colour, self.colour)
        #print(state.piece_nodes)
        return self.game_mechanics.get_move_from_tuple(move) 
        #return self.format_move(state, next_state, self.colour)



            







    