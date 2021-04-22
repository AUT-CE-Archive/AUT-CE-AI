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
		['1', '1', '1', '1', '-1', '-1', '1', '1', '1', '1'],
		['1', '-1', '1', '1', '2', '2', '1', '1', '1', '1'],
		['-1', '1', '1', '2', '2', '2', '2', '1', '-1', '-1'],
		['-1', '1', '1', '-1', '-1', '2', '2', '1', '1', '-1'],
		['1', '1', '1', '1', '2', '2', '1', '1', '1', '1'],
		['1', '1', '1', '1', '-1', '1', '-1', '1', '1', '1'],
	]

	robat = (0, 0)

	butters = [
		(2, 3), (2, 6)
	]

	destinations = [
		(5, 5), (3, 8)
	]



	graph = Graph(matrix)

	astar = Astar()
	path = astar.search(graph, (0, 0), (4, 0))
	
	for node in path:
		print(node.get_coor(), end = ' ')
'''

5	5
2	2	2	2	2
2r	1	1	1	2
2	1	1b	1	2
2	1	x	1	2
2	2	2p	2	2

'''