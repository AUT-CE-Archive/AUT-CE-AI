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
        path = {}

        # G score - Cost of the cheapest path from start to n currently known
        g_scores = {}
        g_scores[start] = 0

        while not frontier.empty():

            # Get the node with highest priority
            current_x, current_y = frontier.get()
            current = graph.graph[current_x][current_y]

            if current == goal:
                break

            for neighbor in graph.get_neighbors(current):

                # Get neighbor's x, y
                x, y = neighbor.get_coor()

                g = g_scores[current] + graph.graph[x][y].g

                if (neighbor not in g_scores) or (g < g_scores[neighbor]):
                    g_scores[neighbor] = g

                    h = self.heuristic(neighbor, goal)
                    f = g + h

                    # Add neighbor to the frontier
                    frontier.put(neighbor, f)

                    path[neighbor] = current

        return path


    # def search(self, graph, start, goal):

    #     open_list = PriorityQueue()
    #     open_list.put(start, 0)
    #     closed_list = []

    #     while open_list:

    #         current = open_list.get()
    #         closed_list.append(current)

    #         if current == goal:
    #             break

    #         for neighbor in graph.get_neighbors(current):                

    #             if neighbor not in closed_list:

    #                 g = graph.graph[neighbor.x][neighbor.y].g + 1
    #                 h = self.heuristic(neighbor, goal)
    #                 f = g + h

    #                 for node in open_list:
    #                     if node == neighbor and neighbor.g > node.g:
    #                         continue

    #                 open_list.append(neighbor)