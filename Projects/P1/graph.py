# Imports
import random
from node import Node

class Graph:	
	''' Graph object '''

	def __init__(self, matrix):
		''' Constructor '''
		
		self.graph = []
		self.matrix = matrix.copy()

		# Create graph with node objects
		for i, row in enumerate(matrix):
			self.graph.append([Node((i, j), int(col)) for j, col in enumerate(row)])


	def abundant(self, abundants, exceptions):
		''' Marks other butters as obstacles '''

		for node in abundants:
			if exceptions is not None and node not in exceptions:
				self.graph[node[0]][node[1]].g = -1


	def get_neighbors(self, node, shuffle = True):
		''' Returns the neightbors of the given node '''
		x, y = node.get_coor()
		width, height = len(self.graph), len(self.graph[0])

		neightbors = [self.graph[x + step[0]][y + step[1]] for step in  [(-1,0), (1,0), (0,-1), (0,1)]  if ((0 <= x + step[0] < width) and (0 <= y + step[1] < height) and self.graph[x + step[0]][y + step[1]].g != -1)]

		# Shuffle
		if shuffle: random.shuffle(neightbors)

		return neightbors


	def reset(self):
		''' Resets all the parents for a new start '''

		for i, row in enumerate(self.graph):
			for j, col in enumerate(row):
				self.graph[i][j].parent = None
				self.graph[i][j].positioning = []