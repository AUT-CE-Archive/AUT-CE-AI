# Imports
from a_star import Astar
from graph import Graph
import heapq

# Driver function
if __name__ == '__main__':

	# row_count, column_count = 5, 5

	# input_matrix = [
	# 	['2', '2', '2', '2', '2'],
	# 	['2r', '1', '1', '1', '2'],
	# 	['2', '1', '1b', '1', '2'],
	# 	['2', '1', 'x', '1', '2'],
	# 	['2', '2', '2p', '2', '2'],
	# ]

	matrix = [
		['2', '-1', '2', '2', '2'],
		['2', '1', '1', '1', '-1'],
		['-1', '1', '1', '1', '2'],
		['2', '1', '-1', '1', '-1'],
		['-1', '2', '-1', '2', '2'],
	]	

	graph = Graph(matrix)


	for row in graph.graph:
		for col in row:
			print(col.g, end = '\t')
		print()


	astar = Astar()
	start = graph.graph[0][0]
	goal = graph.graph[3][0]
	path = astar.search(graph, start, goal)
	
	for key in path.keys():
		print(key.get_coor(), path[key].get_coor())


	# print(graph.get_neighbors((3, 3)))

'''

5	5
2	2	2	2	2
2r	1	1	1	2
2	1	1b	1	2
2	1	x	1	2
2	2	2p	2	2

'''