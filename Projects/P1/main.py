# Imports
from mapper import *
from gui import GUI

# Driver function
if __name__ == '__main__':

	dims = None
	matrix = []
	butters = []
	goals = []
	robot = None

	lines = []
	with open('map (4).txt', 'r') as file: lines = file.readlines()

	dims = [int(x) for x in lines[0].strip().split('\t')]

	for i, line in enumerate(lines[1:]):		

		splitted = line.replace('x', '-1').strip().split('\t')

		for j, value in enumerate(splitted):
			
			try:
				splitted[j] = int(splitted[j])
			except:
				if splitted[j][1] == 'b':
					butters.append((i, j))
				elif splitted[j][1] == 'p':
					goals.append((i, j))
				else:
					robot = (i, j)
				splitted[j] = int(splitted[j][0])
		matrix.append(splitted)

	# matrix = [
	# 	['1', '1', '1', '1', '-1', '-1', '1', '1', '1', '1'],
	# 	['1', '-1', '1', '1', '2', '2', '1', '1', '1', '1'],
	# 	['-1', '1', '1', '2', '2', '2', '2', '1', '-1', '-1'],
	# 	['-1', '1', '1', '-1', '-1', '2', '2', '1', '1', '-1'],
	# 	['1', '1', '1', '1', '2', '2', '1', '1', '1', '1'],
	# 	['1', '1', '1', '1', '-1', '1', '-1', '1', '1', '1'],
	# ]
 
	# robot = (0, 0)

	# butters = [
	# 	(2, 3), (2, 6)
	# ]

	# goals = [
	# 	(5, 5), (3, 8)
	# ]	

	# Animate the routes
	gui = GUI(
		title = 'A* Algorithm',
		matrix = matrix.copy(),
		butters = butters.copy(),
		goals = goals.copy(),
		robot = robot,
	)	

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



	gui.animate()