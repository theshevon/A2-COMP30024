class GameState:

    WIN_EXIT_COUNT = 4
    piece_nodes    = {}
    exit_counts    = {}

    def __init__(self, piece_nodes, exit_counts):
        self.copy_dict(self.piece_nodes, piece_nodes)
        self.copy_dict(self.exit_counts, exit_counts, False)


    def get_piece_nodes(self, colour):
        """
        Returns a dictionary containing the nodes occupied by all the pieces on 
        the board, categorised by colour.
        """

        return self.piece_nodes[colour]

    def get_enemy_piece_nodes(self, colour):
        """
        Returns a set containing the nodes occupied by pieces of colours other 
        than the one specified.
        """

        enemy_piece_nodes = set()
        for colour_ in self.piece_nodes:
            if (colour_ == colour):
                continue
            enemy_piece_nodes = enemy_piece_nodes.union(self.piece_nodes[colour])
        
        return enemy_piece_nodes

    def is_terminal(self):
        """
        Returns True if the state results in a team winning.
        """
        
        for colour in self.exit_counts:
            if self.exit_counts[colour] == self.WIN_EXIT_COUNT:
                return True
                
        return False

    def copy_dict(self, to_dict, from_dict, is_type_set=True):
        """
        Conducts a deep copy of one dictionary into another dictionary.
        """

        for colour in ["red", "blue", "green"]:
            if is_type_set:
                to_dict[colour] = from_dict[colour].copy()
            else:
                to_dict[colour] = from_dict[colour]

    def copy(self, gs_to_copy_from):
        """
        Replaces the dictionaries in the game state with those from the 
        'gs_to_copy_from' game state.
        """

        self.copy_dict(self.piece_nodes, gs_to_copy_from.piece_nodes)
        self.copy_dict(self.exit_counts, gs_to_copy_from.exit_counts, False)


