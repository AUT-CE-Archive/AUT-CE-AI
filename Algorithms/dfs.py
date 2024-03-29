class Graph:
	''' Graph Object '''

	# Constructor
	def __init__(self):
		''' Contructor '''

		self.graph = dict()


	def addEdge(self, u, v):
		''' Adds an Edge to a verticy '''

		if u in self.graph.keys():
			self.graph[u].append(v)
		else:
			self.graph[u] = [v]

	
	def DFSUtil(self, v, visited):
		''' A function used by DFS '''

		visited.add(v)
		print(v, end = ' ')

		for neighbour in self.graph[v]:
			if neighbour not in visited:
				self.DFSUtil(neighbour, visited)

	def DFS(self, v):

		self.DFSUtil(v, visited = set())

# Driver code
if __name__ == '__main__':
	
	g = Graph()
	g.addEdge(0, 1)
	g.addEdge(0, 2)
	g.addEdge(1, 2)
	g.addEdge(2, 0)
	g.addEdge(2, 3)
	g.addEdge(3, 3)

	print("Following is DFS from (starting from vertex 2)")
	g.DFS(2)