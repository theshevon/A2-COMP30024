from math import sqrt
from Wildcat.game_state import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT         = (999, 999)
    MAX_DEPTH    = 4
    TEAM_COLOURS = { "red", "green", "blue" }
    colour       = None

    def __init__(self, colour):

        self.colour = colour

    def get_next_action(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        action, _ = self.best_reply_search(board, board.get_game_state(), float("-inf"), float("+inf"), self.MAX_DEPTH, True)
        
        return action

    def get_all_possible_actions(self, state, board, is_max):
        """
        Returns a triple containing lists of all the possible 'jump', 'exit'  
        and 'move' actions that a player can perform. 
        An exit move is a special case and is denoted by the two-tuple 
        ("EXIT", (999, 999)).
        """

        jump_actions = []
        exit_actions = []
        move_actions = []
        occupied_nodes = state.get_all_piece_nodes()

        # find the nodes corresponding to the max player / min players
        if is_max:
            colours_and_nodes = [(self.colour, node) for node in state.get_team_piece_nodes(self.colour)]
        else:
            colours_and_nodes = []
            for colour in self.TEAM_COLOURS:
                if colour == self.colour:
                    continue
                colours_and_nodes += [(colour, node) for node in state.get_team_piece_nodes(colour)]

        
        for colour, node in colours_and_nodes:
            
            # check if an exit is one of the possible moves
            if node in board.get_exit_nodes(colour):
                exit_actions.append((colour, ("EXIT", node)))
            
            # consider the nodes we can move to
            for neighbouring_node in board.get_neighbouring_nodes(node):

                # if a neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:
                    
                    landing_node = board.get_landing_node(node, neighbouring_node)
                    if landing_node:
                        jump_actions.append((colour, ("JUMP", (node, landing_node))))
                
                else:
                    move_actions.append((colour, ("MOVE", (node, neighbouring_node))))

        # aggregate moves in the specified order
        possible_actions = jump_actions + exit_actions + move_actions
        return possible_actions        

    def get_all_successor_states(self, state, board, is_max):
        """
        Returns a list of 2 tuples containing the all the possible states that 
        the game can be succeeded into, given its current state and the action
        required to move into that state.
        """

        successor_states = []

        # generate all possible_actions
        possible_actions = self.get_all_possible_actions(state, board, is_max)
                
        # for each move, create a new game state
        for colour, action in possible_actions:
            
            successor_state = deepcopy(state)
            successor_state.update(colour, action)
            successor_states.append((successor_state, action))
            
        return successor_states
    
    def evaluate_state(self, board, state):
        
        utility = 0
        player_nodes = state.get_team_piece_nodes(self.colour)
        n_nodes = len(player_nodes)

        if n_nodes == 0:
            if state.get_exit_count(self.colour) == state.WIN_EXIT_COUNT:
                return float("+inf")
            else:
                return float("-inf")

        # - get average distance to exit
        total_no_moves_to_exit = 0.1
        for p_node in player_nodes:
            total_no_moves_to_exit += board.get_min_no_of_moves_to_exit(p_node, self.colour)
        avg_no_of_moves_to_exit = total_no_moves_to_exit / n_nodes

        return avg_no_of_moves_to_exit

    
    def best_reply_search(self, board, state, alpha, beta, depth, is_max):

        # stop searching if depth limit has been reached or if state results
        # in a player winning
        if (depth == 0) or (state.is_terminal()):
            print(depth == 0)
            return None, self.evaluate_state(board, state, self.colour)

        if is_max:
            successor_states = self.get_all_successor_states(state, board, True)
            is_next_turn_max = False
        else:
            successor_states = self.get_all_successor_states(state, board, False)
            is_next_turn_max = True
        
        for child_state, action in successor_states:
            _, utility = -best_reply_search(board, state, -beta, -alpha, depth-1, is_next_turn_max)

            if utility >= beta:
                return action, utility
            
            alpha = max(alpha, utility)
        
        return action, alpha
        


    




    