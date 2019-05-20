import heapq

class PriorityQueue:

	def __init__(self):
		self.elements = []
		self.next_element_id = 0

	def empty(self):
		'''returns True if the priority queue is empty'''

		return len(self.elements)== 0

	def add(self, priority, item):
		'''adds a node group to the priority queue'''

		heapq.heappush(self.elements, (priority, self.next_element_id, item))
		self.next_element_id += 1
		
	def poll(self):
		'''returns the node group at the head of the priority queue (i.e., the 
		one with the lowest f score'''

		return heapq.heappop(self.elements)[2]
