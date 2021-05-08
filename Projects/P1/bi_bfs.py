# imports
from node import Node
from graph import Graph
import math


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


    # Function for adding undirected edge
    def add_edge(self, src, dest):
        
        node1 = AdjacentNode(dest)        
        self.graph[dest] = node1
                
        node2 = AdjacentNode(src)
        self.graph[src] = node2
        
        node2.next = self.graph[dest]
        node1.next = self.graph[src]


    # Function for Breadth First Search
    def bfs(self, graph, list_edges, queue, visited, parent, robot, all_goals, butters):
        ''' Core BFS algorithm '''

        current = queue.pop(0)
        
        start = Node(current, 0)
        for node in graph.get_neighbors(start):
            if (current, node.get_coor()) or (node.get_coor() , current) not in list_edges:
                self.add_edge(current, node.get_coor())
                list_edges.append((current, node.get_coor()))

        connected_node = self.graph[current]
        for node in graph.get_neighbors(start):
            vertex = node.get_coor()

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
            try:
                self.bfs(
                    graph = graph,
                    list_edges =list_edges,
                    queue = self.src_queue,
                    visited = self.src_visited,
                    parent = self.src_parent,
                    robot = robot,
                    all_goals = all_goals,
                    butters = butters,
                )
            except:
                print('Err - BFS src')
                return []

            # BFS in reverse direction from Destination Vertex
            try:
                self.bfs(
                    graph = graph,
                    list_edges = list_edges,
                    queue = self.dest_queue,
                    visited = self.dest_visited,
                    parent = self.dest_parent,
                    robot = robot,
                    all_goals = all_goals,
                    butters = butters,
                )
            except:
                print('Err - BFS dest')
                return []
            
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