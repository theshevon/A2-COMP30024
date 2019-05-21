from math import sqrt
from ben.game_state import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    # TODO: implement transition steps

    EXIT       = (999, 999)
    MAX_DEPTH  = 4
    colour     = None

    def __init__(self, colour):

        self.colour = colour

    def get_next_action(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        _, action = self.minimax(board, board.get_game_state(), self.MAX_DEPTH, float("-inf"), float("+inf"), self.colour, self.colour)

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

        jump_moves     = []
        exit_moves     = []
        move_moves     = []
        team_nodes     = state.get_team_piece_nodes(colour)
        occupied_nodes = state.get_all_piece_nodes()       

        for node in team_nodes:

            # check if an exit is one of the possible moves
            if node in board.get_exit_nodes(colour):
                exit_moves.append((node, self.EXIT))
            
            # add neighbouring nodes to list
            for neighbouring_node in board.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node=board.get_landing_node(node, neighbouring_node)
                    if (landing_node):
                        jump_moves.append((node, landing_node))
                
                else:
                    move_moves.append((node, neighbouring_node))

        # aggregate moves in the specified order
        possible_moves = exit_moves + jump_moves + move_moves
        
        if possible_moves == []:
            return [("PASS", None)]

        # convert all the moves into actions and return it
        return [self.get_action_from_move(board, move) for move in possible_moves]
   
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

    def evaluate_state(self, board, state, colour):
        
        utility        = 0
        player_nodes   = state.piece_nodes[colour]
        n_nodes        = len(player_nodes)

        if n_nodes == 0:
            if state.get_exit_count(colour) == state.WIN_EXIT_COUNT:
                return float("+inf")
            else:
                return float("-inf")

        # - get average distance to exit
        total_no_moves_to_exit = 0.1
        for p_node in player_nodes:
            total_no_moves_to_exit += board.get_min_no_of_moves_to_exit(p_node, colour)
        avg_no_of_moves_to_exit = total_no_moves_to_exit / n_nodes

        # - get army displacement
        # -- calculate coordinates of central node
        central_node = [0, 0]
        for p_node in player_nodes:
            central_node[0] += p_node[0]
            central_node[1] += p_node[1]
        central_node = tuple([coord_val / n_nodes for coord_val in central_node])
        # -- calculate the average distance of each piece from the centroid
        total_dist = 0.1
        for p_node in player_nodes:
            total_dist += board.get_euclidean_distance(central_node, p_node)
        avg_dist_to_centre = total_dist / n_nodes

        # score opponents
        enemy_nodes  = state.get_enemy_piece_nodes(colour)
        enemy_scores = 0.1
        for e_node in enemy_nodes:
            # if enemy can cut one of your pieces, give them a higher score
            for p_node in player_nodes:
                if board.get_euclidean_distance(p_node, e_node) <= sqrt(2):
                    # enemy is on an adjacent node so check if they can cut you
                    # on the board
                    if board.get_landing_node(e_node, p_node):
                        # factor in how many pieces you have on the board b/c
                        # the enemy would be less threatening if you had > (4 - n_pieces_exited)
                        p_pieces_needed_to_exit = state.WIN_EXIT_COUNT - state.get_exit_count(colour)
                        if n_nodes < p_pieces_needed_to_exit:
                            enemy_scores += 10
                        elif n_nodes == p_pieces_needed_to_exit:
                            enemy_scores += 8
                        else:
                            enemy_scores += 3
            enemy_scores += 1

        # score players
        player_scores = 0
        for p_node in player_nodes:
            player_scores += 3

        # TODO: learn how to exit - maybe score based on exit
        # TODO: normalise so that we have at least (4 - n_exited) players
        # TODO: score based on how many pieces we threaten
        # TODO: maybe use these to figure out which player is ahead and then prefer moves that hurts that player? (if two moves score the same as us)

        # calculate utility based on the above scores
        utility = (20 / avg_no_of_moves_to_exit) + \
                  (10 / enemy_scores) + \
                  (2 / avg_dist_to_centre) + \
                  player_scores

        # exit if it results in a terminal state
        if state.get_exit_count(colour) == state.WIN_EXIT_COUNT:
            utility += 100000

        return utility
    
    def evaluate_state_old(self, board, state, colour):
        MAX_DISTANCE = 24
        weight = 0
        feature_total = 0
        for colour_ in state.piece_nodes:

            if(colour_ == colour):
                weight = 1
            else:
                weight = -1

            for coord in state.piece_nodes[colour_]:
                feature_total += weight*(6-board.get_min_no_of_moves_to_exit(coord,colour_))

            feature_total+= 15*weight* state.exit_counts[colour_]

            if(state.exit_counts[colour_]==4):
                feature_total += 100*weight

        return feature_total

    def minimax(self, board, state, depth, alpha, beta, curr_colour, max_colour):

        next_colour = { "red" : "green", "green" : "blue", "blue" : "red" }

        if (depth == 0) or (state.is_terminal()):
            return self.evaluate_state(board, state, max_colour), None
        
        is_maximising_player = True if max_colour == curr_colour else False

        if is_maximising_player:
            
            best_utility = float("-inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility > best_utility:
                    best_utility = utility
                    best_action  = action
                alpha = max(alpha, best_utility)

                if alpha >= beta:
                    break

            return best_utility, best_action

        else:

            best_utility = float("+inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility < best_utility:
                    best_utility = utility
                    best_action  = action
                beta = min(beta, best_utility)

                if alpha >= beta:
                    break
            
            return best_utility, best_action
            



    




    