from copy import deepcopy

class GameState:

    WIN_EXIT_COUNT = 4

    piece_nodes    = None
    exit_counts    = None

    def __init__(self, piece_nodes, exit_counts):
        
        self.piece_nodes = deepcopy(piece_nodes)
        self.exit_counts = deepcopy(exit_counts)

    def print_info(self):
        print("Piece Nodes:", self.piece_nodes)
        print("Exit Counts:", self.exit_counts)


    def get_team_piece_nodes(self, colour):
        """
        Returns a dictionary containing the nodes occupied by all the pieces on 
        the board, categorised by colour.
        """

        return deepcopy(self.piece_nodes[colour])

    def get_enemy_piece_nodes(self, colour):
        """
        Returns a set containing the nodes occupied by pieces of colours other 
        than the one specified.
        """

        enemy_piece_nodes = set()
        for colour_ in self.piece_nodes:
            if (colour_ == colour):
                continue
            enemy_piece_nodes = enemy_piece_nodes.union(deepcopy(self.piece_nodes[colour]))
        
        return enemy_piece_nodes

    def get_all_piece_nodes(self):
        """
        Returns a set containing the nodes occupied by pieces.
        """

        piece_nodes = set()
        for colour_ in self.piece_nodes:
            piece_nodes = piece_nodes.union(deepcopy(self.piece_nodes[colour_]))
        
        return piece_nodes

    def get_exit_count(self, colour):
        """
        Returns the number of exits for a particular colour.
        """

        return self.exit_counts[colour]
        
    def is_terminal(self):
        """
        Returns True if the state results in a team winning.
        """
        
        for colour in self.exit_counts:
            if self.exit_counts[colour] == self.WIN_EXIT_COUNT:
                return True
                
        return False

    def update(self, colour, action):
        """
        Updates the state that results from a particular action being performed.
        """

        # a pass action does not require any updating        
        if action[0] == "PASS":
            return 
        
        if action[0] == "EXIT":
            self.piece_nodes[colour].discard(action[1])
            self.exit_counts[colour] += 1

        # and if the move wasn't an exit, update the set to reflect the pieces 
        # new location
        if (action[0] == "MOVE") or (action[0] == "JUMP"):
            self.piece_nodes[colour].add(action[1][1])
            self.piece_nodes[colour].discard(action[1][0])

        # check if a piece got cut
        if action[0] == "JUMP":
            # get the node that was jumped over
            q = int((action[1][1][0] + action[1][0][0]) / 2)
            r = int((action[1][1][1] + action[1][0][1]) / 2)
            jumped_over_node = (q, r)
            self.update_piece_node(jumped_over_node, colour)

    def update_piece_node(self, node, new_colour):
        """
        Changes the assignment of a node to a different colour, provided that
        a piece has been cut.
        """
        
        for colour in self.piece_nodes:
            if node in self.piece_nodes[colour]:
                self.piece_nodes[colour].discard(node)
                self.piece_nodes[new_colour].add(node)
                return