from math import sqrt
from AI_Papi.game_state import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT   = (999, 999)
    DEPTH  = 4
    colour = None

    def __init__(self, colour):

        self.colour = colour

    def get_next_action(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        _, action = self.minimax(board, board.get_game_state(), self.DEPTH, float("-inf"), float("+inf"), self.colour, self.colour)

        if action is None:
            return ('PASS', None)
            
        return action

    def get_action_from_move(self, board, move):
        """
        Returns an action corresponding to a move.
        """
        if move[1] == self.EXIT:
            return ("EXIT", move[0])
        else:
            if board.get_euclidean_distance(move[0], move[1]) <= sqrt(2):
                return ("MOVE", move)
            return ("JUMP", move)

    def get_all_possible_actions(self, state, board, colour):
        """
        Returns a list of all the possible actions that a player can perform. 
        An exit move is a special case and is denoted by the two-tuple 
        ("EXIT", (999, 999)).
        """

        possible_moves = []
        team_nodes     = state.get_team_piece_nodes(colour)
        occupied_nodes = state.get_all_piece_nodes()       

        for node in team_nodes:

            # check if an exit is one of the possible moves
            if node in board.get_exit_nodes(colour):
                possible_moves.append((node, self.EXIT))
            
            # add neighbouring nodes to list
            for neighbouring_node in board.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node=board.get_landing_node(node, neighbouring_node)
                    if (landing_node):
                        possible_moves.append((node, landing_node))
                
                else:
                    possible_moves.append((node, neighbouring_node))

        # convert all the moves into actions
        possible_actions = []
        for move in possible_moves:
            possible_actions.append(self.get_action_from_move(board, move))
        
        return possible_actions
   
    def get_all_successor_states(self, state, board, colour):
        """
        Returns a list of 2 tuples containing the all the possible states that 
        the game can be succeeded into, given its current state and the action
        required to move into that state.
        """

        successor_states = []

        # generate all possible_actions
        possible_actions = self.get_all_possible_actions(state, board, colour)

        # for each move, create a new game state
        for action in possible_actions:
            
            successor_state = deepcopy(state)
            successor_state.update(colour, action)
            successor_states.append((successor_state, action))
            
        return successor_states

    def evaluate_state(self, board, state, curr_colour, max_colour):
        
        nodes = state.piece_nodes[curr_colour]
        n_nodes = len(nodes)

        # terminal state
        if n_nodes == 0:
            return float("+inf") if curr_colour == max_colour else float("-inf")
        
        # - get average distance to exit
        total_dist = 0
        for node in nodes:
            total_dist = board.get_approx_distance_to_exit(node, curr_colour)
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
            total_dist = board.get_euclidean_distance(central_node, node)
        avg_dist_centre = total_dist / n_nodes

        # - check number of enemy pieces
        n_enemy_pieces = len(state.get_enemy_piece_nodes(curr_colour))

        # - calculate utility
        utility = n_nodes - avg_dist_centre - avg_dist_to_exit - n_enemy_pieces

        return (utility + 10000) if curr_colour == max_colour  else (utility - 10000)
        
    def minimax(self, board, state, depth, alpha, beta, curr_colour, max_colour):
        """
        Returns (utility, action)
        """
        
        next_colour = {"red": "blue" , "blue": "green" , "green": "red"}

        # check if game over (terminal state reached)
        if (depth == 0) or (state.is_terminal()):
            # the exit state cannot have a best child state
            return self.evaluate_state(board, state, curr_colour, max_colour), None

        # maximising player
        if (curr_colour == max_colour):

            best_utility = float("-inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if (utility > best_utility):
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

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if (utility < best_utility):
                    best_utility = utility
                    best_action  = action
                beta = min(beta, utility)

                if (alpha >= beta):
                    break
            return best_utility, best_action










    