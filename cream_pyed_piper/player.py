"""
Implementation of an Autonomous agent that will play the Chexers board game 
against two other players.

Version No: 2.0
Version Details:
Implementation that utilises a heuristic that's based on minimising team 
displacement, distance to exit and the enemies pieces while maximising their 
number of pieces.

Written by David Crowe and Shevon Mendis, May 2019
"""

from cream_pyed_piper.board import *
from cream_pyed_piper.decision_engine import *

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
        self.decision_engine = DecisionEngine(colour, self.board)
        
    def action(self):
        """
        Returns a MOVE, JUMP or EXIT action for the player's turn. If none of 
        the latter moves are possible, returns a PASS action.
        """

        return self.decision_engine.get_next_action(self.board)


    def update(self, colour, action):
        """
        Updates the board and game state after a player has performed an action.
        """

        self.board.update_game_state(colour, action)


if __name__ == "__main__":
    player = AIPlayer("red")
    player.action()
            
