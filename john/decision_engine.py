from math import sqrt
from random import randint

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    EXIT                  = (999, 999)
    colour                = None
    exit_nodes            = None

    def __init__(self, colour, board):

        self.colour      = colour
        self.exit_nodes  = board.get_exit_nodes(colour)
        print("EXITS:", self.exit_nodes)

    def get_next_move(self, board):
        """
        Returns a random move out of the list of valid moves.
        """

        nodes = board.get_piece_nodes(self.colour)

        # generate all possible moves
        possible_successors = self.get_all_possible_moves(board, nodes)
        
        # no moves possible
        if len(possible_successors) == 0:
            return ("PASS", None)

        # if cutting an opponents piece is possible, then cut it
        # else try to find the best 
        piece_nodes   = board.piece_nodes
        best_reducton = float("-inf")
        best_move     = possible_successors[0]
        cut_possible  = False

        for move in self.get_jump_moves(board, possible_successors):

            # get the jumped over node
            q = int((move[1][0] + move[0][0]) / 2)
            r = int((move[1][1] + move[0][1]) / 2)
            jumped_over_node = (q, r)

            # check if the jumped over node was occupied by an enemy - if 
            # multiple cuts possible, select the cut that will move the the 
            # team closes to the exit
            for colour in piece_nodes:
                if colour == self.colour:
                    continue
                for node in piece_nodes[colour]:
                    if node == jumped_over_node:
                        
                        curr_dist = board.get_min_no_of_moves_to_exit(move[0],\
                                                                    self.colour)
                        new_dist  = board.get_min_no_of_moves_to_exit(move[1],\
                                                                    self.colour)

                        reduction = curr_dist - new_dist
                        if reduction > best_reducton:
                            best_reducton = reduction
                            best_move     = move
                            cut_possible  = True
            
        if not cut_possible:

            for move in possible_successors:

                # an exit move would be the best 
                if move[1] == self.EXIT:
                    best_move     = move
                    best_reducton = float("+inf")
                    continue

                # if not an exit move, check the distance to the exit reduces with
                # a move
                curr_dist = board.get_min_no_of_moves_to_exit(move[0], self.colour)
                new_dist  = board.get_min_no_of_moves_to_exit(move[1], self.colour)

                reduction = curr_dist - new_dist
                if reduction > best_reducton:
                    best_reducton = reduction
                    best_move = move

        if best_move[1] == self.EXIT:
            return ("EXIT", best_move[0])
        else:
            if board.get_dist(best_move[0], best_move[1]) <= sqrt(2):
                return ("MOVE", best_move)
            return ("JUMP", best_move)


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
        
    def get_jump_moves(self, board, moves):
        """
        Filters and returns the jump moves from a list of moves.
        """

        return [move for move in moves if ((move[1] != self.EXIT) and \
                                (board.get_dist(move[0], move[1]) > sqrt(2)))]







    