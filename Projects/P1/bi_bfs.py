# imports
from node import Node
from graph import Graph
import math
from a_star import Astar


class AdjacentNode:
    ''' AdjacentNode object '''
     
    def __init__(self, vertex):
        ''' Constructor '''

        self.vertex = vertex
        self.next = None


class BI_BFS:
    ''' BI_BFS Object '''

    def __init__(self):
        ''' Constructor '''
        
        # Initialize vertices and graph with vertices
        self.vertices = 100

        # Dictionaries for paths of robot
        self.src_robot_paths, self.dest_robot_paths = {}, {}


    def positioning(self, matrix, neighbor, robot, butters, all_goals, parents, robot_paths):
        ''' Repositions the Robot to push the Butter in desired direction '''

        parent = parents[neighbor.get_coor()]

        # In case its the starting node
        # if parent == -1: return []

        parent = Node(parent, matrix[parent[0]][parent[1]])
        butters = butters.copy()        

        # Calculate deltas
        delta_x = neighbor.x - parent.x
        delta_y = neighbor.y - parent.y        

        if delta_x == 0:        # Horizontal
            dest = (parent.x, parent.y + 1) if (delta_y < 0) else (parent.x, parent.y - 1)        
        else:                   # Vertical
            dest = (parent.x + 1, parent.y) if (delta_x < 0) else (parent.x - 1, parent.y)        

        # If no previous positioning is available, then robot has not moved
        if parent.get_coor() not in robot_paths:
            robot_paths[parent.get_coor()] = [robot]

        # Remove initial target butter location (IDK but it works)
        for node in robot_paths[parent.get_coor()]:
            try: butters.remove(node)
            except: pass

        # Get a path
        astar = Astar()
        path = astar.search(
            matrix = matrix,
            start = robot_paths[parent.get_coor()][-1],
            goal = dest,
            butters = butters,
            all_goals = all_goals,
            abundants = [parent.get_coor()]
        ) + [(parent.get_coor(), [])]           # Add the parent node which robot will push

        # Return final results
        return [] if (len(path) == 0) else [node[0] for node in path]


    # Function for adding undirected edge
    def add_edge(self, src, dest):
        
        node1 = AdjacentNode(dest)        
        self.graph[dest] = node1
                
        node2 = AdjacentNode(src)
        self.graph[src] = node2

        node2.next = self.graph[dest]
        node1.next = self.graph[src]


    # Function for Breadth First Search
    def bfs(self, graph, list_edges, queue, visited, parents, robot, all_goals, butters, robot_paths):
        ''' Core BFS algorithm '''

        current = queue.pop(0)  # Get current node
        
        start = Node(current, 0)
        for node in graph.get_neighbors(start, shuffle = False):
            if (current, node.get_coor()) or (node.get_coor() , current) not in list_edges:
                self.add_edge(current, node.get_coor())
                list_edges.append((current, node.get_coor()))

        # Traverse neighbors
        connected_node = self.graph[current]
        for node in graph.get_neighbors(start, shuffle = False):            
            vertex = node.get_coor()

            if vertex not in visited:
                queue.append(vertex)
                visited[vertex] = True
                parents[vertex] = current
            else:
                if not visited[vertex]:
                    queue.append(vertex)
                    visited[vertex] = True
                    parents[vertex] = current

            if robot is not None:
                robot_path = self.positioning(
                    matrix = graph.matrix,
                    neighbor = node,
                    robot = robot,
                    butters = butters,
                    all_goals = all_goals,
                    parents = parents,
                    robot_paths = robot_paths,
                )

                if len(robot_path) == 1:
                    continue

                # print(start.get_coor(), node.get_coor(), robot_path)
                robot_paths[node.get_coor()] = robot_path

            connected_node = connected_node.next

                
    # Check for intersecting vertex
    def is_intersecting(self):
        
        # Returns intersecting node if present else -1
        for coor_1 in self.src_visited.keys():
            for coor_2 in self.dest_visited.keys():
                if (coor_1 == coor_2): return coor_1
                
        return None


    def search(self, matrix, start, goal, butters, all_goals, robot = None, abundants = []):
        ''' Core Bi-BFS algorithm '''

        src, dest = start, goal

        graph = Graph(matrix)
        start = Node(src, 0)
        goal = Node(dest, 0)
        list_edges = []

        self.graph = {}

        # ONLY IF GOAL IS A BUTTER!
        if goal in butters:
            graph.abundant(abundants = butters, exceptions = [goal])
        elif len(abundants) != 0:
            graph.abundant(abundants = butters + abundants, exceptions = [])
        else:
            graph.abundant(abundants = butters, exceptions = [start])
        
        # Initializing queue for forward and backward search
        self.src_queue, self.dest_queue = list(), list()
        
        # Initializing source and destination visited nodes as False
        self.src_visited, self.dest_visited = {}, {}
        
        # Initializing source and destination parent nodes
        self.src_parents, self.dest_parents = {}, {}        


        def initialize(self, queue, visited, parent, node, coor):

            # Append neighbors for source
            for i in graph.get_neighbors(node):
                if (coor, i.get_coor()) or (i.get_coor() , coor)  not in list_edges:
                    self.add_edge(coor, i.get_coor())
                    list_edges.append((coor, i.get_coor()))

            queue.append(coor)
            visited[coor], parent[coor] = True, -1


        # Initialzie start
        initialize(self, self.src_queue, self.src_visited, self.src_parents, start, src)

        # Initialzie goal
        initialize(self, self.dest_queue, self.dest_visited, self.dest_parents, goal, dest)
        

        while self.src_queue and self.dest_queue:
            
            # BFS in forward direction from Source Vertex
            # try:
            self.bfs(
                graph = graph,
                list_edges = list_edges,
                queue = self.src_queue,
                visited = self.src_visited,
                parents = self.src_parents,
                robot = robot,
                all_goals = all_goals,
                butters = butters,
                robot_paths = self.src_robot_paths,
            )
            # except:
            #     print('Err - BFS src')
            #     return []

            # BFS in reverse direction from Destination Vertex
            # try:
            self.bfs(
                graph = graph,
                list_edges = list_edges,
                queue = self.dest_queue,
                visited = self.dest_visited,
                parents = self.dest_parents,
                robot = goal,
                all_goals = all_goals,
                butters = butters,
                robot_paths = self.dest_robot_paths,
                reverse = True,
            )
            # except:
            #     print('Err - BFS dest')
            #     return []
            
            # Check for intersecting vertex
            intersecting_node = self.is_intersecting()

            # If intersecting vertex exists then path from source to destination exists
            if intersecting_node is not None:

                path = []
                node = intersecting_node

                while node != start.get_coor():
                    robot_path = []
                    if robot is not None:
                        if node in self.src_robot_paths:
                            robot_path = self.src_robot_paths[node]
                        else:
                            return []

                    path.insert(0, (node, robot_path))
                    node = self.src_parents[node]

                # Insert initial position
                path.insert(0, (start.get_coor(), []))

                node = intersecting_node
                while node != goal.get_coor():                    
                    path.append((self.dest_parents[node], []))
                    node = self.dest_parents[node]

                return path

        return []