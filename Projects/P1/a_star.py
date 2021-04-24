from node import Node
from graph import Graph

class Astar:
    ''' A* Object '''

    def __init__(self):
        ''' Constructor '''
        pass


    def heuristic(self, coor_1, coor_2):
        ''' Returns the Manhattan heuristic '''

        (x1, y1) = coor_1.get_coor()
        (x2, y2) = coor_2.get_coor()

        return abs(x1 - x2) + abs(y1 - y2)


    def positioning(self, matrix, neighbor, robot):
        ''' Repositions the Robot to push the Butter in desired direction '''

        astar = Astar()
        graph = Graph(matrix)
        parent = neighbor.parent

        # In case its the starting node
        if parent is None:
            return 0, []

        # Calculate deltas
        delta_x = neighbor.x - parent.x
        delta_y = neighbor.y - parent.y

        dest = None

        # Horizontal
        if delta_x == 0:
            if delta_y < 0:
                dest = (parent.x, parent.y + 1)
            else:
                dest = (parent.x, parent.y - 1)
        # Vertical
        else:
            if delta_x < 0:
                dest = (parent.x + 1, parent.y)
            else:
                dest = (parent.x - 1, parent.y)


        # If no previous positioning is available, then robot has not moved
        if len(parent.positioning) == 0:
            parent.positioning.append(robot)

        # Get a path
        # path = astar.robot_search(matrix = matrix, start = parent.positioning[-1], goal = dest, butters = []) + [parent.get_coor()]
        path = astar.search(
            matrix = matrix,
            start = parent.positioning[-1],
            goal = dest,
            butters = []
        )
        path += [(parent.get_coor(), [])]     # Add the parent node which robot will push

        # Calculate the f() of the entire route the robot should move
        f_sum = 0
        for node in path:
            node = node[0]
            f_sum += graph.graph[node[0]][node[1]].g

        # Unreachable goal
        if len(path) == 0:
            return 10000, []
        else:
            return f_sum, [node[0] for node in path]


    def search(self, matrix, start, goal, butters, robot = None):

        butters = butters.copy()
        graph = Graph(matrix)

        # ONLY IF GOAL IS A BUTTER!
        if goal in butters:
            graph.adjust(goal = goal, butters = butters)

        # Convert coordinates to Node objects
        start = Node(start, 0)
        goal = Node(goal, 0)

        # Check if start or goal is not obstacles
        if graph.graph[start.x][start.y].g == -1 or graph.graph[goal.x][goal.y].g == -1:
            return []

        # Define open & closed sets
        open_set = [start.get_coor()]
        closed_set = []

        # While fringe is not empty
        while open_set:

            # Get node with minimum f()
            x, y = open_set[0]
            current = graph.graph[x][y]
            for node in open_set:

                x, y = node
                node = graph.graph[x][y]
                
                if node.f <= current.f:
                    current = node

            if current.get_coor() == goal.get_coor():

                # Backtrack the path
                path = []
                while current.parent is not None:
                    path.append((current.get_coor(), current.positioning))
                    current = current.parent

                return [(start.get_coor(), start.positioning)] + path[::-1]

            # Move current node from open set to closed set
            open_set.remove(current.get_coor())
            closed_set.append(current.get_coor())

            # Search for each neighbor
            neighbors = graph.get_neighbors(current)
            for neighbor in neighbors:

                x, y = neighbor.get_coor()

                # if neighbor has not already been searched
                if neighbor.get_coor() not in closed_set:

                    # Calculate g()
                    g = current.g + graph.graph[x][y].g

                    if neighbor.get_coor() in open_set:
                        if g < neighbor.g:
                            neighbor.g = g
                    else:
                        neighbor.g = g
                        open_set.append(neighbor.get_coor())   # Add the neighbor to the frontier

                    # Adjust neighbors' properties
                    neighbor.parent = current
                    neighbor.h = self.heuristic(neighbor, goal)

                    # Trace robot if not None
                    if robot is not None:
                        neighbor.p, neighbor.positioning = self.positioning(matrix, neighbor, robot)

                    # Calculate f()
                    neighbor.f = neighbor.g + neighbor.h

        # No path found ):
        return []