# imports
from node import Node
from graph import Graph
import math

class IDS:
    ''' IDS Object '''

    def __init__(self):
        ''' Constructor '''
        
        self.visited = set()            # Keep all visited nodes for the first pass here (TButter IDS)
        self.robot_visited = set()      # Keep all visied nodes for the second pass (Robot IDS)


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


    def DLS(self, graph, start, goal, max_depth, robot, butters, all_goals):
        ''' Core DLS algorithm '''
  
        if start.get_coor() == goal.get_coor():

            # Backtrack
            path = []
            while start.parent is not None:
                path.append((start.get_coor(), start.positioning))
                start = start.parent
            return path + [(start.get_coor(), [])]

        if max_depth <= 0: return []
        
        for neighbor in graph.get_neighbors(start):

            # Add node to visited set to avoid revisiting
            self.visited.add(start.get_coor())

            if neighbor.get_coor() not in self.visited:

                neighbor.parent = start     # Set parent

                if robot is not None:

                    self.robot_visited = self.visited.copy()   # Copy visited
                    self.visited = set()                       # Empty visited set for the second pass

                    neighbor.positioning = self.positioning(
                        matrix = graph.matrix,
                        neighbor = neighbor,
                        robot = robot,
                        butters = butters,
                        all_goals = all_goals
                    )

                    self.visited = self.robot_visited.copy()   # Reassign the visited set with the actual values
                    self.robot_visited = set()

                # Recursive
                path = []
                if robot is not None and len(neighbor.positioning) == 1:
                    continue

                path = self.DLS(graph, neighbor, goal, max_depth - 1, robot, butters, all_goals)

                if path != []:
                    return path

        return []


    def search(self, matrix, start, goal, butters, all_goals, robot = None, abundants = []):
        ''' Core IDS-DFS algorithm '''

        graph = Graph(matrix)
        start = Node(start, 0)
        goal = Node(goal, 0)
        max_depth = len(graph.graph) * len(graph.graph[0])

        # ONLY IF GOAL IS A BUTTER!
        if goal in butters:
            graph.abundant(abundants = butters, exceptions = [goal])
        elif len(abundants) != 0:
            graph.abundant(abundants = butters + abundants, exceptions = [])
        # else:
        #     graph.abundant(abundants = butters + all_goals, exceptions = [goal])

        for depth in range(max_depth):

            # Resets parents & positionings from the last run
            graph.reset()

            # Reset visited set
            self.visited = set()

            path = self.DLS(graph, start, goal, depth, robot, butters, all_goals)            

            if path != []:

                return path[::-1]       # Return reversed path

        return []