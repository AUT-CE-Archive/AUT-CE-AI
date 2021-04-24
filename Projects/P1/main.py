# Imports
from a_star import Astar
import heapq
from graph import Graph




def get_best_butter_path(matrix, start, butters):

	astar = Astar()
	graph = Graph(matrix)

	best_butter_path = None
	best_f_sum = None

	for butter in butters:

		path = astar.search(matrix = matrix, start = start, goal = butter, butters = butters)

		f_sum = 0
		for node in path:
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

		path = astar.search(matrix = matrix, start = start, goal = goal, butters = butters, robot = robot)

		f_sum = 0
		for node in path:
			f_sum += graph.graph[node[0]][node[1]].f


		if (best_f_sum is None) or (f_sum < best_f_sum):
			best_f_sum = f_sum
			best_goal_path = path

	return best_goal_path


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
	]

	goals = [
		(5, 5), (3, 8)
	]

	best_butter_path = get_best_butter_path(matrix = matrix, start = robot, butters = butters)
	print(best_butter_path)

	best_goal_path = get_best_goal_path(matrix = matrix, start = best_butter_path[-1], goals = goals, butters = butters, robot = robot)
	print(best_goal_path)