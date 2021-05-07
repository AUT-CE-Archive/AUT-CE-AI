# Imports
from a_star import Astar
from ids import IDS
from graph import Graph

def get_routes(matrix, butters, goals, model):
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
			)

			if (best_route is None) or (len(path) < len(best_route)):
				best_route = path

		# Add the route to the list, remove the goal as it has been reached only when reachable!
		if len(best_route) != 0:
			routes.append((butter, best_route[-1][0]))
			goals.remove(best_route[-1][0])

	return routes