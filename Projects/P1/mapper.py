# Imports
from a_star import Astar
from graph import Graph

def get_routes(matrix, butters, goals):
	''' Returns the routes the robot must go '''

	astar = Astar()
	routes = []
	goals = goals.copy()
	
	for butter in butters:

		best_route = None
		for goal in goals:

			path = astar.search(
				matrix = matrix,
				start = butter,
				goal = goal,
				butters = butters,
			)

			if (best_route is None) or (len(path) < len(best_route)):
				best_route = path

		# Add the route to the list, remove the goal as it has been reached
		routes.append((butter, best_route[-1][0]))
		goals.remove(best_route[-1][0])

	return routes


def get_best_butter_path(matrix, start, butters):

	astar = Astar()
	graph = Graph(matrix)

	best_butter_path = None
	best_f_sum = None

	for butter in butters:

		path = astar.search(
			matrix = matrix,
			start = start,
			goal = butter,
			butters = butters
		)

		f_sum = 0
		for node in path:
			node = node[0]
			f_sum += graph.graph[node[0]][node[1]].f

		if (best_f_sum is None) or (f_sum < best_f_sum):
			best_f_sum = f_sum
			best_butter_path = path

	return best_butter_path


def get_best_goal_path(matrix, start, goals, butters, robot):

	astar = Astar()
	graph = Graph(matrix)

	best_goal_path = None
	best_f_sum = None	

	for goal in goals:

		path = astar.search(
			matrix = matrix,
			start = start[0],
			goal = goal,
			butters = butters,
			robot = robot
		)

		f_sum = 0
		for node in path:
			node = node[0]
			f_sum += graph.graph[node[0]][node[1]].f


		if (best_f_sum is None) or (f_sum < best_f_sum):
			best_f_sum = f_sum
			best_goal_path = path

	return best_goal_path