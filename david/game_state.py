class GameState():
	"""
	Class that represents a game state by information such as the positions
	of each team's pieces and the exit counts for each team.
	"""

	COLOURS 	   = { "red", "green", "blue" }
	WIN_EXIT_COUNT = 4
	piece_nodes    = None
	exit_nodes     = None
	
	def __init__(self, piece_nodes, exit_counts):
		
		self.piece_nodes = dict(piece_nodes)
		self.exit_counts = dict(exit_counts)

	def is_terminal(self):
		"""
        Returns True if the state results in a team winning.
        """

		for colour in self.COLOURS:
			if self.exit_counts[colour] == self.WIN_EXIT_COUNT:
				return True
		
		return False
	
	def change_piece_node(self, jumped_over_node, new_colour):
		"""
        Changes the assignment of a node to a different colour, provided that
        a piece has been cut.
        """
        
		for colour in self.COLOURS:
			if jumped_over_node in self.piece_nodes[colour]:
				self.piece_nodes[colour].discard(jumped_over_node)
				self.piece_nodes[new_colour].add(jumped_over_node)
				return
		
	def get_all_piece_nodes(self):
		"""
        Returns a set containing the nodes occupied by pieces.
        """

		piece_nodes = set()
		for colour in self.COLOURS:
			piece_nodes = piece_nodes.union(self.piece_nodes[colour])
		
		return piece_nodes

	def copy(self):
		"""
		Returns a deep copy of the game state.
		"""

		piece_nodes = dict()
		exit_counts = dict()

		for colour in self.piece_nodes:
			piece_nodes[colour]= set(self.piece_nodes[colour])
			exit_counts[colour]= int(self.exit_counts[colour])

		return GameState(piece_nodes, exit_counts)

