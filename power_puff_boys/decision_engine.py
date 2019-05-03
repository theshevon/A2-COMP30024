from math import sqrt
from power_puff_boys.board import *
from power_puff_boys.node_utilities import *
from power_puff_boys.priority_queue import *

class DecisionEngine():
    """Used to find path to exit nodes"""

    board                 = None
    colour                = None
    exits                 = None
    open_node_combs       = None
    init_node_comb        = None
    closed_node_combs     = None
    open_node_combs_queue = None
    states                = None

    def __init__(self, piece_nodes):

        # create board storing information about other players peices
        self.board  = Board()
        self.colour = colour
        self.exits  = self.board.get_exit_nodes(colour)

    def update_board(self, colour, action):
        self.board.update_piece_node(colour, action)

    def get_next_move(board, colour):
        pass

    def find_path(self):

        self.states = {}

        # node combinations that are known but not been explored
        self.open_node_combs = set()

        # node combinations that have been explored
        self.closed_node_combs = set()

        # priority queue holding f-costs and their associated node combinations
        self.open_node_combs_queue = PriorityQueue()

        self.init_node_comb = NodeCombination(set([tuple(node) for \
                                                        node in board.get_piece_nodes[colour]]))
        self.open_node_combs.add(self.init_node_comb)
        self.add_state(self.init_node_comb)
        self.states[self.init_node_comb].g_cost = 0
        self.open_node_combs_queue.add(0, self.init_node_comb)


        # blocked nodes here are nodes occupied by enemy pieces
        blocked_nodes = set()
        for colour_ in board.piece_nodes:
            if colour_ != colour:
                for node in board.piece_nodes[colour_]:
                    blocked_nodes.add(node)

        while self.open_node_combs:

            curr_node_comb = self.open_node_combs_queue.poll()
            
            self.open_node_combs.discard(curr_node_comb)
            self.closed_node_combs.add(curr_node_comb)

            # if current node combination just contains an empty tuple, we have
            # reached the goal state
            if not curr_node_comb.nodes: 
                break

            for successor_comb in self.get_successor_combs(curr_node_comb, 
                                                                blocked_nodes):
                
                # creates a new node for child if not already initiated
                self.add_state(successor_comb)

                if successor_comb not in self.closed_node_combs:
                    
                    self.open_node_combs.add(successor_comb)

                    # get cost to move into the next position 
                    traversal_cost = 1 + self.states[curr_node_comb].g_cost
                    
                    # if the new cost is lower, update successor combination's 
                    # parent and g_cost
                    if self.update_state(successor_comb, traversal_cost, curr_node_comb):
                        # adds updated f_cost of successor combination to the 
                        # priority queue
                        
                        f_cost = traversal_cost + self.states[successor_comb].h_cost
                        self.open_node_combs_queue.add(f_cost, successor_comb)

        self.print_path(curr_node_comb)

    def add_state(self, node_comb):

        if node_comb not in self.states:
            self.states[node_comb] = State()
            self.states[node_comb].h_cost = self.board.get_heuristic_cost(node_comb, self.colour)

    def update_state(self, node_comb, new_cost, new_parent):
        '''updates a state and returns True if the new traversal cost is smaller 
           than its current traversal cost. Returns false otherwise.'''

        state = self.states[node_comb]

        if new_cost < state.g_cost:
            state.g_cost = new_cost
            state.parent = new_parent
            return True
        
        return False 

    def get_successor_combs(self, curr_node_comb, blocked_nodes):
        '''returns the possible successor combs for a given node combination'''

        nodes = curr_node_comb.nodes
        successor_combs = set()

        for node in nodes:

            # -- find explorable nodes

            explorable_nodes = set()
            
            # if the node is an exit node, add an empty tuple to the explorable set
            if node in self.exits:
                explorable_nodes.add(tuple())

            # find explorable nodes by assessing a node's neighbours
            for neighbour in self.board.get_neighbouring_nodes(node):

                if self.board.is_on_board(neighbour):
                    
                    if (neighbour in blocked_nodes) or (neighbour in nodes):
                    
                        # add landing node only if it's an unoccupied node on the board
                        landing_node = self.board.get_landing_node(node, neighbour, blocked_nodes)
                        if landing_node and (landing_node not in nodes):
                            explorable_nodes.add(landing_node)

                    else:
                        explorable_nodes.add(neighbour)
            
            # -- create and add possible successor combs

            for explorable in explorable_nodes:

                temp = nodes.copy()
                temp.discard(node)

                if explorable:
                    temp.add(explorable)

                successor_combs.add(NodeCombination(temp))

        return successor_combs
    
    def get_dist(self, node_1, node_2):
        '''returns the euclidean distance between two nodes'''

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)

    def print_path(self, target_node_comb):
        '''prints the path for the initial node combination to escape the board
        '''
        
        # -- recursive case

        if self.states[target_node_comb].parent != self.init_node_comb:
            self.print_path(self.states[target_node_comb].parent)

        # -- base case

        start = (self.states[target_node_comb].parent.nodes - target_node_comb.nodes).copy().pop()
        end   = (target_node_comb.nodes - self.states[target_node_comb].parent.nodes).copy()

        if end:
            
            end   = end.pop()

            # if the action is to a neighbour, it will be a 'MOVE', otherwise 
            # a 'JUMP'
            if (self.get_dist(start, end) <= sqrt(2)):
                print(self.move_.format(start, end))
                # self.debugger.update(start, end)
            else:
                print(self.jump_.format(start, end))
                # self.debugger.update(start, end)

        else:
            print(self.exit_.format(start))
            # self.debugger.piece_locns.remove(start)

        # self.debugger.print_board()
        # time.sleep(1) # sleep used to show the pieces moving in a cinematic fashion
        




       




