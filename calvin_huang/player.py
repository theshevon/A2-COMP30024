"""
Implementation of an Autonomous agent that will play the Chexers board game 
against two other players.

Version No: 2.1
Version Details:
- Improved ordering of moves
- stopped using recursive deepcopy
Current Issues:
- Weird 'float' to 'int' conversion error

Written by David Crowe and Shevon Mendis, May 2019
"""

from calvin_huang.GameMechanics import *
from calvin_huang.decision_engine import *
from calvin_huang.min_max_node import *

class AIPlayer:
    """
    Represents a Controller for an agent that plays Chexers.
    """
    game_mechanics  = None 
    current_state   = None
    decision_engine = None

    def __init__(self, colour):
        """
        Initialises the player by building up an inner implementation of the 
        game board.
        """
        #Need to include a way of
        self.game_mechanics  = GameMechanics()
        self.current_state   = State(GameMechanics.start_nodes , GameMechanics.start_exit_counts)
        self.decision_engine = DecisionEngine(colour)
        
    def action(self):
        """
        Returns a MOVE, JUMP or EXIT action for the player's turn. If none of 
        the latter moves are possible, returns a PASS action.
        """
        return self.decision_engine.get_next_move(self.current_state)


    def update(self, colour, action):
        """
        Updates the board after a player has made a move.
        """

        self.game_mechanics.update_node(self.current_state, colour, action)

if __name__ == "__main__":
    player = AIPlayer("red")
    player.action()
            
