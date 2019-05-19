
class State():
	
	def __init__( self , piece_nodes,  exit_counts):
		self.piece_nodes = dict(piece_nodes)
		#way to keep count of number of pieces exited 
		self.exit_counts = dict(exit_counts)

	def copy(self):

		piece_nodes = dict()
		exit_counts = dict()

		for colour in self.piece_nodes:
			piece_nodes[colour]= set(self.piece_nodes[colour])
			exit_counts[colour]= int(self.exit_counts[colour])

		return State(piece_nodes, exit_counts)
