# imports
from node import Node
from graph import Graph
import math

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


    def positioning(self, matrix, neighbor, robot, butters, all_goals):
        ''' Repositions the Robot to push the Butter in desired direction '''

        parent = neighbor.parent
        butters = butters.copy()

        # In case its the starting node
        if parent is None: return []

        # Calculate deltas
        delta_x = neighbor.x - parent.x
        delta_y = neighbor.y - parent.y        

        if delta_x == 0:        # Horizontal
            dest = (parent.x, parent.y + 1) if (delta_y < 0) else (parent.x, parent.y - 1)        
        else:                   # Vertical
            dest = (parent.x + 1, parent.y) if (delta_x < 0) else (parent.x - 1, parent.y)

        # If no previous positioning is available, then robot has not moved
        if len(parent.positioning) == 0:
            parent.positioning.append(robot)

        # Remove initial target butter location (IDK but it works)
        for node in parent.positioning:
            try: butters.remove(node)
            except: pass

        # Get a path
        path = self.search(
            matrix = matrix,
            start = parent.positioning[-1],
            goal = dest,
            butters = butters,
            all_goals = all_goals,
            abundants = [parent.get_coor()]
        ) + [(parent.get_coor(), [])]           # Add the parent node which robot will push

        # Return final results
        return [] if (len(path) == 0) else [node[0] for node in path]


    def search(self, matrix, start, goal, butters, all_goals, robot = None, abundants = []):
        ''' Core A* algorithm '''

        graph = Graph(matrix)

        # ONLY IF GOAL IS A BUTTER!
        if goal in butters:
            graph.abundant(abundants = butters, exceptions = [goal])
        elif len(abundants) != 0:
            graph.abundant(abundants = butters + abundants, exceptions = [])

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

                    # Set parent                    
                    neighbor.parent = current                

                    # Trace robot if not None
                    if robot is not None:
                        neighbor.positioning = self.positioning(
                            matrix = matrix,
                            neighbor = neighbor,
                            robot = robot,
                            butters = butters,
                            all_goals = all_goals,
                        )

                        if len(neighbor.positioning) == 1:
                            neighbor.p = math.inf       # Infinity
                            open_set.remove(neighbor.get_coor())

                    # Adjust neighbors' properties
                    neighbor.h = self.heuristic(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h + neighbor.p

        # No path found ):
        return []