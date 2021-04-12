class Graph:
	''' Graph Object '''
	
	def __init__(self):
		''' Contructor '''

		self.graph = dict()


	def addEdge(self, u, v):
		''' Adds an Edge to a verticy '''

		if u in self.graph.keys():
			self.graph[u].append(v)
		else:
			self.graph[u] = [v]


	def BFS(self, s):
		''' Core algorithm '''
		
		visited = set()

		# Create a queue for BFS
		queue = []

		# Add leading node to the queue
		queue.append(s)
		visited.add(s)

		while queue:
			s = queue.pop(0)

			print (s, end = " ")

			for i in self.graph[s]:
				if i not in visited:
					queue.append(i)
					visited.add(i)


# Driver code
if __name__ == '__main__':

	g = Graph()
	g.addEdge(0, 1)
	g.addEdge(0, 2)
	g.addEdge(1, 2)
	g.addEdge(2, 0)
	g.addEdge(2, 3)
	g.addEdge(3, 3)

	print ("Following is Breadth First Traversal"" (starting from vertex 2)")

	g.BFS(2)