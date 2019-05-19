"""
Implementation of an Autonomous agent that will play the Chexers board game 
against two other players.

Version No: 0.0
Version Details:
Basic implementation that focuses on completing the game without making any
invalid moves. All of the players' moves are random.

Written by David Crowe and Shevon Mendis, May 2019
"""

from adam.board import *
from adam.decision_engine import *

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

        return self.decision_engine.get_next_move(self.board)


    def update(self, colour, action):
        """
        Updates the board after a player has made a move.
        """

        self.board.update_node(colour, action)


if __name__ == "__main__":
    player = AIPlayer("red")
    player.action()
            
