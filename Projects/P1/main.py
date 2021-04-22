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


	for row in graph.graph:
		for col in row:
			print(col.g, end = '\t')
		print()


	astar = Astar()

	butter_paths = []
	for butter in butters:

		butter_x, butter_y = butter
		robat_x, robat_y = robat

		# path = astar.search(graph, start = graph.graph[robat_x][robat_y], goal = graph.graph[butter_x][butter_y])
		path = astar.search(graph, start = graph.graph[0][0], goal = graph.graph[3][2])		
		butter_paths.append(path)


	for path in butter_paths:
		print([(node.x, node.y) for node in path])


	# start = graph.graph[0][0]
	# goal = graph.graph[3][0]
	# path = astar.search(graph, start, goal)
	
	# for node in path:
	# 	print(node.get_coor())
'''

5	5
2	2	2	2	2
2r	1	1	1	2
2	1	1b	1	2
2	1	x	1	2
2	2	2p	2	2

'''