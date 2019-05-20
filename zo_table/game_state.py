import numpy as np
class State():
	
	def __init__( self , piece_nodes,  exit_counts , z_key):
		self.piece_nodes = dict(piece_nodes)
		#way to keep count of number of pieces exited 
		self.exit_counts = dict(exit_counts)
		self.z_key = np.uint64(z_key)

	def copy(self):

		piece_nodes = dict()
		exit_counts = dict()

		for colour in self.piece_nodes:
			piece_nodes[colour]= set(self.piece_nodes[colour])
			exit_counts[colour]= int(self.exit_counts[colour])

		return State(piece_nodes, exit_counts, self.z_key)
