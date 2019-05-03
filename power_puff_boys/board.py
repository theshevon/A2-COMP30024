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

    def update_piece_node(self, colour, action):
        '''updates the position of a piece after a move'''
        
        if (action == "PASS"):
            return 
        
        # remove prev location
        self.piece_nodes[colour].discard(action[1][0])

        # add updated piece location if move wasn't an exit
        if ((action == "MOVE") or (action == "JUMP")):
            self.piece_nodes[colour].add(action[1][1])

    def get_piece_nodes(self, colour):
        '''returns a set containing the locations of pieces of a specified colour'''
        
        return start_nodes[colour]

    def get_heuristic_cost(self, node_comb, colour):
        '''adds the heuristic cost for a given node group of a particular colour'''

        cost = 0
        for node in node_comb.nodes:
            cost += self.get_distance_estimate(node, self.exit_line_cfs[colour])
        
        return cost

    def get_distance_estimate(self, node, cfs):
        '''returns the minimum possible sequence of moves from each node to 
        any exit node'''
        
        # shortest number of 'move' actions to reach an exit node
        min_move_cost = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

        # shortest number of  'jump' actions to reach an exit node
        min_jump_cost = min_move_cost // 2 + min_move_cost % 2 + 1

        return min_jump_cost

    def is_on_board(self, node):
        '''returns True if a given node is on a board'''

        return node in self.all_nodes

    def get_landing_node(self, curr_node, node_to_jump_over, blocked_nodes):
        '''returns the landing node when when jumping from one node over another.
           returns None if the landing node is not on the board (i.e. a jump 
           isn't possible)'''

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_node = (q,r)

        return landing_node if ((landing_node in self.all_nodes) and (landing_node not in blocked_nodes)) else None

    def get_exit_nodes(self, colour):
        '''returns the set of exit nodes for a particular colour'''

        return self.exit_nodes[colour]

    def get_neighbouring_nodes(self, node):
        '''returns a list of possible neighbouring nodes'''

        neighbours = []

        r_start = node[1]
        r_end = node[1] + 2
        col = 0
        for q in range(node[0]-1, node[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)

                if possible_neighbour != node:
                    neighbours.append(possible_neighbour)

            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours