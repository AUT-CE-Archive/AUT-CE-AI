class Node:
	''' Node object '''

	def __init__(self, coor, g):
		''' Constructor '''
		
		# Node properties		
		self.x, self.y = coor
		self.parent = None

		# A* properties
		self.g, self.h, self.f, self.p = g, None, 0, None

		# Gloabal properties
		self.positioning = []		


	def get_coor(self):
		''' Returns the x, y as typle '''
		return self.x, self.y