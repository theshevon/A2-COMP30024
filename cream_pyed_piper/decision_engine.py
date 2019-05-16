from math import sqrt
from random import randint
from cream_pyed_piper.utilities import *
import sys

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT                  = (999, 999)
    DEPTH                 = 5
    colour                = None
    exit_nodes            = None

    def __init__(self, colour, board):

        self.colour      = colour
        self.exit_nodes  = board.get_exit_nodes(colour)

    def get_next_action(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        utility, action = self.minimax(board, board.curr_game_state, self.DEPTH, float("-inf"), float("+inf"), self.colour, self.colour)

        return action

    def get_action_from_move(self, board, move):
        """
        Returns an action based on a move.
        """
        if move[1] == self.EXIT:
            return ("EXIT", move[0])
        else:
            if board.get_dist(move[0], move[1]) <= sqrt(2):
                return ("MOVE", move)
            return ("JUMP", move)

    def get_all_possible_actions(self, board, nodes):
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

                    landing_node = board.get_landing_node(node, neighbouring_node)
                    if (landing_node):
                        possible_moves.append((node, landing_node))
                
                else:
                    possible_moves.append((node, neighbouring_node))

        # convert all the moves into actions
        possible_actions = []
        for move in possible_moves:
            possible_actions.append(self.get_action_from_move(board, move))
        
        return possible_actions
   
    def evaluate_state(self, board, state, colour):
        
        nodes = state.piece_nodes[colour]
        n_nodes = len(nodes)

        # terminal state
        if n_nodes == 0:
            return float("+inf")
        
        # - get average distance to exit
        total_dist = 0
        for node in nodes:
            total_dist = board.get_distance_estimate(node, colour)
        avg_dist_to_exit = total_dist / n_nodes

        # - get army displacement
        # -- calculate centroid
        central_node = [0, 0]
        for node in nodes:
            central_node[0] += node[0]
            central_node[1] += node[1]
        central_node = tuple([x / n_nodes for x in central_node])
        # -- calculate average distance of each piece from centroid
        total_dist = 0
        for node in nodes:
            total_dist = board.get_dist(central_node, node)
        avg_dist_centre = total_dist / n_nodes

        # - check number of enemy pieces
        n_enemy_pieces = len(state.get_enemy_piece_nodes(colour))

        # - calculate utility
        utility = n_nodes - avg_dist_centre - avg_dist_to_exit - n_enemy_pieces

        return utility
        
    def minimax(self, board, state, depth, alpha, beta, curr_colour, max_colour):
        """
        Returns (utility, action)
        """
        
        next_colour = {"red": "blue" , "blue": "green" , "green": "red"}

        # check if game over (terminal state reached)
        if (depth == 0) or (state.is_terminal()):
            # the exit state cannot have a best child state
            return self.evaluate_state(board, state, curr_colour), None

        # maximising player
        if (curr_colour == max_colour):

            best_utility = float("-inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(board, curr_colour):
                utility, action = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility > best_utility:
                    best_utility = utility
                    best_action  = action
                alpha = max(alpha, utility)

                if (alpha >= beta):
                    break
            return best_utility, best_action

        # minimising player
        else:

            best_utility = float("+inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(board, curr_colour):
                utility, action = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility < best_utility:
                    best_utility = utility
                    best_action  = action
                beta = min(beta, utility)

                if (alpha >= beta):
                    break
            return best_utility, best_action

    def get_all_successor_states(self, board, colour):
        """
        Returns a list of 2 tuples containing the all the possible states that 
        the game can be succeeded into, given its current state and the action
        required to move into that state.
        """

        successor_states = []

        piece_nodes = board.get_piece_nodes(colour)

        # generate all possible_actions
        possible_actions = self.get_all_possible_actions(board, piece_nodes)

        # for each move, create a new game state
        for action in possible_actions:

            # carry out the action
            board.update_game_state(self.colour, action)

            state = GameState(board.curr_game_state.piece_nodes, 
                                board.curr_game_state.exit_counts)
            successor_states.append((state, action))

            # undo the action
            board.revert_to_previous_state()

        return successor_states








    