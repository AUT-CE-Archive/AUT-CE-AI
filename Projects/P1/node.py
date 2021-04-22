class Node:
	''' Node object '''

	def __init__(self, coor, g):
		''' Constructor '''
		
		self.g, self.h, self.f = g, None, 0
		self.x, self.y = coor
		self.neighbors = []
		self.parent = None
		self.obstacle = False


	def get_coor(self):
		''' Returns the x, y as typle '''
		return self.x, self.y