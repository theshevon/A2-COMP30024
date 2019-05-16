from math import sqrt
from random import randint
from cpp.node_utilities import *
from cpp.priority_queue import *
import sys

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT                  = (999, 999)
    colour                = None
    exit_nodes            = None
    open_node_combs       = None
    init_node_comb        = None
    closed_node_combs     = None
    open_node_combs_queue = None
    states                = None

    def __init__(self, colour, board):

        self.colour      = colour
        self.exit_nodes  = board.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_action(self, board, move):
        """
        Returns an action based on a move.
        """
        if move[1] == self.EXIT:
            return ("EXIT", move[0])
        else:
            if board.get_dist(move[0], move[1]) <= sqrt(2):
                return ("MOVE", move)
            return ("JUMP", move)

    def get_next_move(self, board):
        """
        Returns a random move out of the list of valid moves.
        """

        nodes = board.get_piece_nodes(self.colour)

        # generate all possible moves
        possible_moves = self.get_all_possible_moves(board, nodes)
        
        # no moves possible so pass
        if len(possible_moves) == 0:
            return ("PASS", None)

        # iterate through the moves and pick the best based on the heuristic
        best_action  = None
        best_utility = -sys.maxsize
        # print("START: ", nodes)
        for move in possible_moves:
            # detemine the action
            action = self.get_action(board, move)
            # print("ACTION: ", action)
            # carry out the action
            board.update_node(self.colour, action)
            # print("AFTER ACTION:", board.get_piece_nodes(self.colour))

            # evaluate move
            utility = self.evaluate_state(board)
            
            # compare with current state. if better, tag it as the best move
            if (utility >= best_utility):
                best_utility = utility
                best_action = action                

            # undo move
            board.undo_last_move()
            # print("AFTER UNDO:", board.get_piece_nodes(self.colour))
        
        return best_action
            
    def get_all_possible_moves(self, board, nodes):
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

                    landing_node = board.get_landing_node(node, neighbouring_node, occupied_nodes)
                    if (landing_node):
                        possible_moves.append((node, landing_node))
                
                else:
                    possible_moves.append((node, neighbouring_node))

        return possible_moves
   
    def evaluate_state(self, board):
        
        nodes = board.get_piece_nodes(self.colour)
        n_nodes = len(nodes)

        # - get average distance to exit
        total_dist = 0
        for node in nodes:
            total_dist = board.get_distance_estimate(node, self.colour)
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
        n_enemy_pieces = len(board.get_all_enemy_piece_nodes(self.colour))

        # - calculate utility
        utility = n_nodes - avg_dist_centre - avg_dist_to_exit - n_enemy_pieces

        return utility
        











    