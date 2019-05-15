import sys

class NodeCombination:
    
    nodes = {}

    def __init__(self, nodes):
        self.nodes  = nodes

    def __str__(self):
        return str(sorted(self.nodes))

    def __hash__(self):
        return hash(tuple(sorted(self.nodes)))

    def __eq__(self, other):
        return self.nodes == other.nodes
 
class State:

    def __init__(self):
        self.g_cost = sys.maxsize
        self.h_cost = None
        self.parent = None

    # purely for debugging purposes
    def print_info(self):
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)