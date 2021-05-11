# Imports
#from mapper import *
import gui
from a_star import IDS

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


	# Animate the routes
	# 


	#pairs = get_routes (
	#	matrix = matrix,		
	#	butters = butters,
	#	goals = goals
	#)
	pairs = [((2,3) , (3,5))]
	print('Routes:', pairs, end = '\n' * 3)
	
	astar = IDS()
	for pair in pairs:

		print('Pair {0}'.format(pair), ':')
		
		path = astar.search3(
			matrix = matrix,
			start = pair[0],
			goal = pair[1],
			butters = butters,
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