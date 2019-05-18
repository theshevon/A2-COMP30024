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
    exit_line_cfs = { "blue" : (1, 1, 3) , "red": (1, 0, -3), 
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