from math import sqrt
from random import randint
from 2tiles.node_utilities import *
from 2tiles.priority_queue import *
from 2tiles.GameMechanics import *
from 2tiles.min_max import *
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
    DEPTH = 4
    def __init__(self, colour):

        self.colour      = colour
        self.exit_nodes  = self.game_mechanics.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_next_move(self, state):
        """
        Uses min max to determin next move.
        """
        #print(state.piece_nodes)
        value ,next_state = self.min_max.alpha_beta( state , self.DEPTH , float("-inf") , float("+inf") , self.colour, self.colour)
        #print(state.piece_nodes)
        return self.format_move(state, next_state, self.colour)


    #doesn't work because new pieces can be aquired 
    def format_move(self, initial_state, final_state , colour):

        start = (initial_state.piece_nodes[colour] - final_state.piece_nodes[colour]).copy()
        end   = (final_state.piece_nodes[colour] - initial_state.piece_nodes[colour]).copy()

        print(start)
        #print(initial_state.piece_nodes)
        print(end)
        if(start) :
            start = start.pop()
        else:
            return ("PASS", None)
        
        if(end):
            #checks if a piece has been jumped
            for piece in end:
                if( self.game_mechanics.get_dist(start, piece) > sqrt(2)):
                    return ("JUMP" , (start,piece))
            return ( "MOVE" , (start, piece))
        else:
            return ("EXIT", start)

            







    