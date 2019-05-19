"""
Implementation of an Autonomous agent that will play the Chexers board game 
against two other players.

Version No: 2.2
Version Details:
- Utilises a minimax tree with alpha-beta pruning to determine the best move
- The best move is determined by evaulating a game state using a heuristic that:
    - Minimises team army displacement
    - Minimises the distance to the exit
    - Minimises the number of enemy pieces
        - Scores the enemies based on how threatening they are to our agent's 
          pieces. The score factors in how many pieces you have on the board as
          an enemy would be less threatening if you had > (4 - n_pieces_exited)
          on the board
    - Maximises the number of team pieces
Current Issues:
- Still not exiting competently- agent has a tendency to cluster at corner and 
  repeat the same moves until game times out.

Written by David Crowe and Shevon Mendis, May 2019
"""

from AI_Papi.board import *
from AI_Papi.decision_engine import *

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

        return self.decision_engine.get_next_action(self.board)


    def update(self, colour, action):
        """
        Updates the board after a player has performed an action.
        """

        self.board.update_board(colour, action)

            
