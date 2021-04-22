from node import Node

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


    def search(self, graph, start, goal):

        # Convert coordinates to Node objects
        start = Node(start, 0)
        goal = Node(goal, 0)

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
                
                if node.f < current.f:
                    current = node

            if current.get_coor() == goal.get_coor():

                # Backtrack the path
                path = []
                while current.parent is not None:
                    path.append(current)
                    current = current.parent

                return path

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
                    neighbor.h = self.heuristic(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current

        # No path found ):
        return []