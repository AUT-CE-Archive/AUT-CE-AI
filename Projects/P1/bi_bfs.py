# imports
from node import Node
from graph import Graph
import math


class AdjacentNode:
     
    def __init__(self, vertex):

        self.vertex = vertex
        self.next = None


class BI_BFS:
    ''' BI_BFS Object '''

    def __init__(self):
        ''' Constructor '''
        
        # Initialize vertices and graph with vertices
        self.vertices = 100        


    def positioning(self, matrix, neighbor, robot, butters):
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
    def bfs(self, graph, list_edges, queue, visited, parent):
        ''' Core BFS algorithm '''

        current = queue.pop(0)
        
        start =Node(current, 0)
        for i in graph.get_neighbors(start):
            if (current, i.get_coor()) or (i.get_coor() , current) not in list_edges:
                self.add_edge(current, i.get_coor())
                list_edges.append((current, i.get_coor()))

        connected_node = self.graph[current]
        for i in graph.get_neighbors(start):
            vertex = i.get_coor()

            if vertex not in visited:
                queue.append(vertex)
                visited[vertex] = True
                parent[vertex] = current

            else:
                if not visited[vertex]:
                    queue.append(vertex)
                    visited[vertex] = True
                    parent[vertex] = current

            connected_node = connected_node.next

                
    # Check for intersecting vertex
    def is_intersecting(self):
        
        # Returns intersecting node if present else -1
        for i in self.src_visited.keys():
            for j in self.dest_visited.keys():
                if (i == j): return i
                
        return None


    def search(self, matrix, start, goal, butters, all_goals, robot = None, abundants = []):
        ''' Core Bi-BFS algorithm '''

        src, dest = start, goal

        graph = Graph(matrix)        
        start = Node(src, 0)
        goal = Node(dest, 0)
        list_edges = []

        self.graph = {}
        
        # Initializing queue for forward and backward search
        self.src_queue, self.dest_queue = list(), list()
        
        # Initializing source and destination visited nodes as False
        self.src_visited, self.dest_visited = {}, {}
        
        # Initializing source and destination parent nodes
        self.src_parent, self.dest_parent = {}, {}

        

        def initialize(self, queue, visited, parent, node, coor):

            # Append neighbors for source
            for i in graph.get_neighbors(node):
                if (coor, i.get_coor()) or (i.get_coor() , coor)  not in list_edges:
                    self.add_edge(coor, i.get_coor())
                    list_edges.append((coor, i.get_coor()))

            queue.append(coor)
            visited[coor], parent[coor] = True, -1


        # Initialzie start
        initialize(self, self.src_queue, self.src_visited, self.src_parent, start, src)

        # Initialzie goal
        initialize(self, self.dest_queue, self.dest_visited, self.dest_parent, goal, dest)
        

        while self.src_queue and self.dest_queue:
            
            # BFS in forward direction from Source Vertex
            self.bfs(graph, list_edges, self.src_queue, self.src_visited, self.src_parent)

            # BFS in reverse direction from Destination Vertex
            self.bfs(graph, list_edges, self.dest_queue, self.dest_visited, self.dest_parent)
            
            # Check for intersecting vertex
            intersecting_node = self.is_intersecting()
            
            # If intersecting vertex exists then path from source to destination exists
            if intersecting_node is not None:

                path = [(intersecting_node, [])]

                node = intersecting_node

                while node != start.get_coor():
                    path.insert(0, (self.src_parent[node], []))
                    node = self.src_parent[node]

                node = intersecting_node
                while node != goal.get_coor():
                    path.append((self.dest_parent[node], []))
                    node = self.dest_parent[node]

                return path

        return []