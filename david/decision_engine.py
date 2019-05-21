from math           import sqrt
from david.board    import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    MAX_SEARCH_DEPTH = 5

    colour                = None
    exit_nodes            = None
    states                = None

    def __init__(self, colour):
        self.colour   = colour

    def get_next_move(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        utility, next_state = self.minimax(board, board.current_state, self.MAX_SEARCH_DEPTH, float("-inf"), float("+inf"), self.colour, self.colour)
        
        return self.format_move(board, board.current_state, next_state, self.colour)

    def format_move(self, board, initial_state, final_state, colour):

        start = (initial_state.piece_nodes[colour] - final_state.piece_nodes[colour]).copy()
        end   = (final_state.piece_nodes[colour] - initial_state.piece_nodes[colour]).copy()

        if start:
            start = start.pop()
        else:
            return ("PASS", None)
        
        if end:

            # checks if a piece has been jumped
            for piece in end:
                if board.get_dist(start, piece) > sqrt(2):
                    return ("JUMP" , (start,piece))
            return ( "MOVE" , (start, piece))
        else:
            return ("EXIT", start)
    
    def minimax(self, board, state, depth, alpha, beta, curr_colour, max_colour):

        next_colour = { "red" : "green", "green" : "blue", "blue" : "red" }

        if (depth == 0) or (state.is_terminal()):
            return self.evaluate_state(board, state, max_colour), None
        
        is_maximising_player = True if max_colour == curr_colour else False

        if is_maximising_player:
            
            best_utility      = float("-inf")
            best_child_state  = None

            for child_state in board.get_all_successor_states(state, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility > best_utility:
                    best_utility     = utility
                    best_child_state = child_state
                alpha = max(alpha, best_utility)

                if alpha >= beta:
                    break

            return best_utility, best_child_state

        else:

            best_utility = float("+inf")
            best_action  = None

            for child_state in board.get_all_successor_states(state, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility < best_utility:
                    best_utility = utility
                    best_child_state = child_state
                beta = min(beta, best_utility)

                if alpha >= beta:
                    break
            
            return best_utility, best_child_state

    def evaluate_state(self, board, state, max_colour):
        
        MAX_DISTANCE = 24
        weight = 0
        feature_total = 0
        
        for colour in state.piece_nodes:

            if(colour == max_colour):
                weight = 1
            else:
                weight = -1

            for coord in state.piece_nodes[colour]:
                feature_total += weight*(6-board.get_min_no_of_moves_to_exit(coord,colour))

            feature_total+= 15*weight* state.exit_counts[colour]

            if(state.exit_counts[colour]==4):
                feature_total += 100*weight

        return feature_total







    