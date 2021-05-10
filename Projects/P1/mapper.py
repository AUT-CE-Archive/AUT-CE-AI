# Imports
from a_star import Astar
from ids import IDS
from graph import Graph
from bi_bfs import BI_BFS


def get_pairs(matrix, butters, goals, model):
	''' Returns the routes the robot must go '''

	routes = []
	goals = goals.copy()
	
	for butter in butters:

		best_route = None
		for goal in goals:

			path = model.search(
				matrix = matrix,
				start = butter,
				goal = goal,
				butters = butters,
				all_goals = goals,
			)

			if (best_route is None) or (len(path) < len(best_route)):
				best_route = path

		# Add the route to the list, remove the goal as it has been reached only when reachable!
		if len(best_route) != 0:
			routes.append((butter, best_route[-1][0]))
			goals.remove(best_route[-1][0])

	return routes


def get_route(matrix, pair, butters, goals, robot, model):
	''' Get's a route given the search model '''

	start = pair[0]
	goal = pair[1]

	return model.search(
		matrix = matrix,
		start = start,
		goal = goal,
		butters = butters,
		all_goals = goals,
		robot = robot,
	)

def get_map(file_path):
	'''	Reads the map, returns properties '''

	dims = None
	matrix = []
	butters = []
	goals = []
	robot = None

	lines = []
	with open(file_path, 'r') as file: lines = file.readlines()

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


	return dims, butters, goals, robot, matrix


def short_view(route, matrix):
	''' Prints a short view of the route '''

	robot_route = []
	robot_dir = []
	cost = 0

	for butter_loc, robot_path in route:
		for node in robot_path:
			robot_route.append(node)
			cost += matrix[node[0]][node[1]]
	
	dir_map = {
		(1, 0): 'D',
		(-1, 0): 'U',
		(0, 1): 'R',
		(0, -1): 'L',
		(0, 0): ''
	}

	for i in range(1, len(robot_route)):
		prev = robot_route[i - 1]
		curr = robot_route[i]

		delta_x = curr[0] - prev[0]
		delta_y = curr[1] - prev[1]		

		_dir = dir_map[(delta_x, delta_y)]
		robot_dir.append(_dir)

	print(' '.join([_dir for _dir in robot_dir if _dir != '']))
	print(cost)
	print(len(robot_dir))


def extended_view(route, matrix):
	''' Prints an extended view of the route '''

	print('Butter Loc\t|\t Robot Path')
	for butter_loc, robot_path in route:
		print(butter_loc, '\t\t|\t', robot_path)


def view_route(route, matrix, type):
	''' Views the route '''

	if type == 'basic':
		short_view(route = route, matrix = matrix)
	else:
		extended_view(route = route, matrix = matrix)
	print()