# Imports
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


    # def a_star_search(self, graph, start, goal):
    #     ''' Main A* algorithm '''

    #     frontier = PriorityQueue()
    #     frontier.put(start, 0)

    #     came_from: Dict[Location, Optional[Location]] = {}
    #     cost_so_far: Dict[Location, float] = {}

    #     came_from[start] = None
    #     cost_so_far[start] = 0
        
    #     while not frontier.empty():
    #         current: Location = frontier.get()
            
    #         if current == goal:
    #             break
            
    #         for next in graph.neighbors(current):
    #             new_cost = cost_so_far[current] + graph.cost(current, next)
    #             if next not in cost_so_far or new_cost < cost_so_far[next]:
    #                 cost_so_far[next] = new_cost
    #                 priority = new_cost + heuristic(next, goal)
    #                 frontier.put(next, priority)
    #                 came_from[next] = current
        
    #     return came_from, cost_so_far

    def search(self, graph, start, goal):

        # Create frontier queue
        frontier = PriorityQueue()
        frontier.put(start, 0)

        # History dictionary
        history = {}

        # G score - Cost of the cheapest path from start to n currently known
        g_scores = {}
        g_scores[start] = 0

        while not frontier.empty():

            # Get the node with highest priority
            current = frontier.get()

            if current == goal:
                break

            for neighbor in graph.get_neighbors(current):

                # Get neighbor's x, y
                x, y = neighbor.get_coor()

                new_g_score = g_scores[current] + graph.graph[x][y].g

                if (neighbor not in g_scores) or (new_g_score < g_scores[neighbor]):
                    g_scores[neighbor] = new_g_score

                    # Calculate f()
                    f = new_g_score + self.heuristic(neighbor, goal)

                    # Add neighbor to the frontier
                    frontier.put(neighbor, f)

                    history[neighbor] = current

        return history