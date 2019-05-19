
class State():
	
	def __init__( self , piece_nodes,  exit_counts):
		self.piece_nodes = dict(piece_nodes)
		#way to keep count of number of pieces exited 
		self.exit_counts = dict(exit_counts)
