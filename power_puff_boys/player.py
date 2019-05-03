"""
Implementation of an Autonomous agent that will play the Chexers board game 
against two other players.

Version No: 1.0
Version Details:
Basic implementation that focuses on completing the game without making any
invalid moves. The only strategy, if any, is that the player would cut another
player's piece if in danger of being cut themselves.

Written by David Crowe and Shevon Mendis, May 2019
"""

from power_puff_boys.board import *
from power_puff_boys.decision_engine import *

class AIPlayer:
    """
    Represents a Controller for an agent that plays Chexers.
    """

    board           = None
    decision_engine = None

    def __init__(self, colour):
        """
        Initialises the player by building up an inner implementation of the 
        game board.
        """

        self.board           = Board()
        self.decision_engine = DecisionEngine(colour)
        
    def action(self):
        """
        Returns a MOVE, JUMP or EXIT action for the player's turn. If none of 
        the latter moves are possible, returns a PASS action.
        """

        return decision_engine.get_next_move(self.board)


    def update(self, colour, action):
        """
        Updates the board after a player has made a move.
        """

        self.board.update_node(self, colour, action)

        
            
