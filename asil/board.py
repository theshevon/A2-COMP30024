from math import sqrt

class Board:
    """
    Represents the Chexers board, which is considered to be composed of nodes.
    """

    SIZE = 3

    all_nodes   = set()
    piece_nodes = { "red" : set(), "blue" : set(), "green" : set() }

    # starting nodes for the different teams
    start_nodes = {
                        "red"   : { (-3,0), (-3,1),  (-3,2),  (-3,3) },
                        "blue"  : {  (0,3),  (1,2),   (2,1),   (3,0) },
                        "green" : { (0,-3), (1,-3),  (2,-3),  (3,-3) }
                  }

    # exit nodes for the different teams
    exit_nodes  =  {
                        "red"   : { (3,-3), (3,-2),  (3,-1),  (3,0)  },
                        "blue"  : { (-3,0), (-2,-1), (-1,-2), (0,-3) },
                        "green" : { (-3,3), (-2,3),  (-1,3),  (0,3)  }
                   }

    # coefficents for lines through exits (cf[0]q + cf[1]r + cf[2] = 0) 
    EXIT_LINE_CFS = { "blue" : (1, 1, 3) , "red": (1, 0, -3), 
                                                        "green" : (0, 1, -3) }

    def __init__(self):
        """
        Initialises the board by creating and storing its nodes. 
        It also stores the locations of the different pieces on the board.
        """

        # initialise all nodes on board
        ran = range(-self.SIZE, self.SIZE+1)
        for node in [(q,r) for q in ran for r in ran if -q-r in ran]:
            self.all_nodes.add(node)

        # track the locations of each team's pieces
        for colour in self.start_nodes:
            for node in self.start_nodes[colour]:
                self.piece_nodes[colour].add(node)

    def update_node(self, colour, action):
        """
        Updates the position of a piece after a move was taken.
        """

        # a pass action does not require any updating        
        if action[0] == "PASS":
            return 
        
        if action[0] == "EXIT":
            self.piece_nodes[colour].discard(action[1])

        # and if the move wasn't an exit update the set to reflect the pieces 
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
            self.change_piece_node(jumped_over_node, colour)

            
    def change_piece_node(self, node, new_colour):
        """
        Changes the assignment of a node to a different colour, provided that
        a piece has been cut.
        """
        
        for colour in self.piece_nodes:
            if node in self.piece_nodes[colour]:
                self.piece_nodes[colour].discard(node)
                self.piece_nodes[new_colour].add(node)
                return

    def get_piece_nodes(self, colour):
        """
        Returns a set containing the nodes occupied by pieces of a specified 
        colour.
        """
        
        return self.piece_nodes[colour]

    def get_all_piece_nodes(self):
        """
        Returns a set containing the nodes occupied by all the pieces on the 
        board.
        """

        piece_nodes = set()
        for colour in self.piece_nodes:
            piece_nodes = piece_nodes.union(self.piece_nodes[colour])

        return piece_nodes

    def get_landing_node(self, curr_node, node_to_jump_over, blocked_nodes):
        """
        Returns the landing node when when jumping from one node over another.
        Returns None if the landing node is not on the board (i.e. a jump 
        isn't possible).
        """

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_node = (q,r)

        return landing_node if ((landing_node in self.all_nodes) and (landing_node not in blocked_nodes)) else None

    def get_exit_nodes(self, colour):
        """
        Returns the set of exit nodes for a particular colour.
        """

        return self.exit_nodes[colour]

    def is_on_board(self, node):
        """
        Returns True if a node is within the board.
        """
        return node in self.all_nodes

    def get_dist(self, node_1, node_2):
        """
        Returns the Euclidean distance between two nodes.
        """

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)

    def get_neighbouring_nodes(self, node):
        """
        Returns a list of possible neighbouring nodes.
        """

        neighbours = []

        r_start = node[1]
        r_end = node[1] + 2
        col = 0
        for q in range(node[0]-1, node[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)

                if (possible_neighbour != node) and (self.is_on_board(possible_neighbour)) :
                    neighbours.append(possible_neighbour)

            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def get_min_no_of_moves_to_exit(self, node, colour):
        """
        Returns the minimum possible moves from a node to an exit nodes.
        """
        
        cfs = self.EXIT_LINE_CFS[colour]
        
        # shortest number of 'move' actions to reach an exit node
        n_min_moves = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

        return n_min_moves