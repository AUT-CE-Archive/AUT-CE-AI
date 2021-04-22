# Imports
from typing import Counter
from priority_queue import PriorityQueue


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

        # Create frontier queue
        frontier = PriorityQueue()
        frontier.put(start, 0)

        # Best route
        path = []        

        # G score - Cost of the cheapest path from start to n currently known
        g_scores = {}
        g_scores[start] = 0

        while not frontier.empty():

            # Get the node with highest priority
            current_x, current_y = frontier.get()
            current = graph.graph[current_x][current_y]

            if current == goal:
                break

            tmp = []

            print(current.get_coor(), [(node.x, node.y) for node in graph.get_neighbors(current)])            

            while True:

                neighbors2 = graph.get_neighbors(current)
                neighbors = []

                print('N2:', [(node.x, node.y) for node in neighbors2])

                if current.parent is None:
                    neighbors = neighbors2
                    break

                for neighbor in neighbors2:                    

                    x1, y1 = neighbor.get_coor()
                    x2, y2 = current.parent.get_coor()

                    if not (x1 == x2 and y1 == y2):
                        neighbors.append(neighbor)

                if len(neighbors2) == 0:
                    current = current.parent
                else:
                    break

            print('N:', [(node.x, node.y) for node in neighbors])

            for neighbor in neighbors:

                # Get neighbor's x, y
                x, y = neighbor.get_coor()

                g = g_scores[current] + graph.graph[x][y].g

                if (neighbor not in g_scores) or (g < g_scores[neighbor]):
                    g_scores[neighbor] = g

                    h = self.heuristic(neighbor, goal)
                    f = g + h
                    neighbor.f = f

                    # Add neighbor to the frontier
                    frontier.put(neighbor, f)

                    tmp.append(neighbor)

            if len(tmp) != 0:
                best_node = tmp[0]
                for node in tmp:
                    if node.f < best_node.f:
                        best_node = node

                path.append(best_node)
                best_node.parent = current


        return [start] + path