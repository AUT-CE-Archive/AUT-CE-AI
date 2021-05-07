# Imports
from mapper import *
import gui

# Driver function
if __name__ == '__main__':

	matrix = [
		['1', '1', '1', '1', '-1', '-1', '1', '1', '1', '1'],
		['1', '-1', '1', '1', '2', '2', '1', '1', '1', '1'],
		['-1', '1', '1', '2', '2', '2', '2', '1', '-1', '-1'],
		['-1', '1', '1', '-1', '-1', '2', '2', '1', '1', '-1'],
		['1', '1', '1', '1', '2', '2', '1', '1', '1', '1'],
		['1', '1', '1', '1', '-1', '1', '-1', '1', '1', '1'],
	]
 
	robot = (0, 0)

	butters = [
		# (2, 3), (2, 6)
		(2, 3)
	]

	goals = [
		# (5, 5), (3, 8)
		(3, 6)
	]


	# Animate the routes
	# gui.animate(
	# 	title = 'A* Algorithm',
	# 	matrix = matrix,
	# 	butters = butters,
	# 	goals = goals,
	# 	robot = robot,
	# 	routes = []
	# )

	model = Astar()
	# model = IDS()


	pairs = get_pairs (
		matrix = matrix,
		butters = butters,
		goals = goals,
		model = model,
	)
	print('Routes:', pairs, end = '\n' * 3)	

	for pair in pairs:

		print('Pair {0}'.format(pair), ':')

		# Get route
		path = get_route(
			matrix = matrix,
			pair = pair,
			butters = butters,
			goals = goals,
			robot = robot,
			model = model,
		)

		# update robot's latest location if route was completed successfully
		if len(path) != 0:
			robot = path[-2][0]

		# Remove the butter and goal
		butters.remove(pair[0])
		goals.remove(pair[1])

		for node in path:
			print(node)

		print()	