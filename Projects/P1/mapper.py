# Imports
from a_star import Astar
from ids import IDS
from graph import Graph

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