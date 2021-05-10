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