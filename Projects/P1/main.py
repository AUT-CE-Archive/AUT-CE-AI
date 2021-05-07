# Imports
from mapper import *
from gui import GUI

# Driver function
if __name__ == '__main__':

	# Read Map
	dims, butters, goals, robot, matrix = get_map('maps/map (4).txt')

	# Define model
	# model = Astar()
	model = IDS()

	# Build GUI
	gui = GUI(
		model = model,
		matrix = matrix.copy(),
		butters = butters.copy(),
		goals = goals.copy(),
		robot = robot,
	)

	# Get pairs
	pairs = get_pairs (
		matrix = matrix,
		butters = butters,
		goals = goals,
		model = model,
	)

	# Print pairs to route
	print('Routes:', pairs, end = '\n' * 3)

	paths = []
	for pair in pairs:

		# Print current route
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

		# Save path for animation
		paths.append(path)

		# update robot's latest location if route was completed successfully
		if len(path) != 0:
			robot = path[-2][0]

		# Remove the butter and goal
		butters.remove(pair[0])
		goals.remove(pair[1])

		if path == []:
			print('Haha, Gotcha! Impossible ^_^')

		for node in path:
			print(node)

		print()


	# Animate GUI
	gui.animate()