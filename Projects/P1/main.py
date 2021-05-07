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
		(2, 3), (2, 6)
		# (2, 3)
	]

	goals = [
		(5, 5), (3, 8)
		# (3, 6)
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

	astar = Astar()
	ids = IDS()


	pairs = get_routes (
		matrix = matrix,		
		butters = butters,
		goals = goals,
		model = astar,
	)
	print('Routes:', pairs, end = '\n' * 3)	

	for pair in pairs:

		print('Pair {0}'.format(pair), ':')
		
		# path = astar.search(
		# 	matrix = matrix,
		# 	start = pair[0],
		# 	goal = pair[1],
		# 	butters = butters,
		# 	robot = robot,
		# )

		path = ids.search(
			matrix = matrix,
			start = pair[0],
			goal = pair[1],
			butters = butters,
			all_goals = goals,
			robot = robot,
		)

		# Save robot's latest location if route was completed successfully
		if len(path) != 0:
			robot = path[-2][0]

		# Remove the butter and goal
		butters.remove(pair[0])
		goals.remove(pair[1])

		for node in path:
			print(node)

		print()	