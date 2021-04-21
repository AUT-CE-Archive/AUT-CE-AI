
class Node:
	''' Node object '''

	def __init__(self, x, y, g):
		''' Constructor '''
		self.x, self.y, self.g = x, y, g


	def get_coor(self):
		''' Returns the x, y as typle '''
		return self.x, self.y


class Graph:
	''' Graph object '''

	def __init__(self, graph):
		''' Constructor '''
		self.graph = []

		# Create graph with node objects
		for i, row in enumerate(graph):
			self.graph.append([Node(i, j, int(col)) for j, col in enumerate(row)])


	def get_neighbors(self, node):
		''' Returns the neightbors of the given node '''
		x, y = node.get_coor()
		width, height = len(self.graph), len(self.graph[0])

		return [self.graph[x + step[0]][y + step[1]] for step in  [(-1,0), (1,0), (0,-1), (0,1)]  if ((0 <= x + step[0] < width) and (0 <= y + step[1] < height) and self.graph[x + step[0]][y + step[1]].g != -1)]