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
 