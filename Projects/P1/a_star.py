# imports
from node import Node
from graph import Graph
import math

class IDS:
    ''' A* Object '''

    def __init__(self):
        ''' Constructor '''
        pass


    


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


    def search(self, matrix, start, goal, butters, robot = None, abundants = []):
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
                            butters = butters
                        )

                        if len(neighbor.positioning) == 1:
                            neighbor.p = math.inf       # Infinity
                            open_set.remove(neighbor.get_coor())

                    # Adjust neighbors' properties
                    neighbor.h = self.heuristic(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h + neighbor.p

        # No path found ):
        return []


















    def search2(self, matrix, start, goal, butters, robot = None, abundants = []):
        ''' Core A* algorithm '''

        graph = Graph(matrix)


        def DLS(self,src,target,maxDepth):
  
            if src.get_coor() == target.get_coor() : 
                list_path=[]
                list_path.append(target.get_coor())
                
               
                
                
                return list_path
               

            if maxDepth <= 0 : return []
  
            
            for i in graph.get_neighbors(src):
                
                list_1=DLS(self , i,target,maxDepth-1)
                if(list_1!=[]): 
                    print(list_1)
                    list_1.append(src.get_coor())
                    return list_1
            return []
  

        def IDDFS(self,src, target, maxDepth , graph):
           
  
        
            for i in range(maxDepth):
                list_1=DLS(graph , src, target, i)
                if (list_1 !=[]):
                    
                    
                    return list_1
            return []   
    
        
        start = Node(start, 0)
        goal = Node(goal, 0)
        list_end = IDDFS(self , start , goal , 70 , graph)
        print(list_end)
        
        return list_end 



    def search3(self, matrix, start, goal, butters, robot = None, abundants = []):
        ''' Core A* algorithm '''

        graph = Graph(matrix)


        class AdjacentNode:
     
            def __init__(self, vertex):
         
                self.vertex = vertex
                self.next = None

        class BidirectionalSearch:
            
            def __init__(self, vertices):
                
                # Initialize vertices and
                # graph with vertices
                self.vertices = vertices
                self.graph = {}
                
                # Initializing queue for forward
                # and backward search
                self.src_queue = list()
                self.dest_queue = list()
                
                # Initializing source and
                # destination visited nodes as False
                self.src_visited = {}
                self.dest_visited = {}
                
                # Initializing source and destination
                # parent nodes
                self.src_parent = {}
                self.dest_parent = {}
                
            # Function for adding undirected edge
            def add_edge(self, src, dest):
                
                # Add edges to graph
                
                # Add source to destination
                node1 = AdjacentNode(dest)
                
                self.graph[dest] = node1
                print(self.graph)
                
                
                
        
                # Since graph is undirected add
                # destination to source
                node2 = AdjacentNode(src)
                self.graph[src] = node2
                node2.next = self.graph[dest]
                node1.next = self.graph[src]
                
            # Function for Breadth First Search
            def bfs(self, graph2,list_edges,direction = 'forward' ):
                
                if direction == 'forward':
                    
                    # BFS in forward direction
                    current = self.src_queue.pop(0)
                    
                    start =Node(current, 0)
                    for i in graph2.get_neighbors(start):
                        if (current, i.get_coor()) or (i.get_coor() , current)  not in list_edges:
                            self.add_edge(current, i.get_coor())
                            list_edges.append((current, i.get_coor()))

                    connected_node = self.graph[current]
                    for i in graph2.get_neighbors(start):
                    #while connected_node:
                        vertex = i.get_coor()
                        print(vertex)
                        print('gggg')
                        print(current)


                        
                        if vertex not in self.src_visited:
        
                                self.src_queue.append(vertex)
                                self.src_visited[vertex] = True
                                self.src_parent[vertex] = current

                        else:
                            if not self.src_visited[vertex]:
                                self.src_queue.append(vertex)
                                self.src_visited[vertex] = True
                                self.src_parent[vertex] = current

                            
                        connected_node = connected_node.next
                        
                else:
                    
                    # BFS in backward direction
                    current = self.dest_queue.pop(0)

                    start =Node(current, 0)
                    for i in graph2.get_neighbors(start):
                        if (current, i.get_coor()) or (i.get_coor() , current)  not in list_edges:
                            self.add_edge(current, i.get_coor())
                            list_edges.append((current, i.get_coor()))


                    connected_node = self.graph[current]

                    for i in graph2.get_neighbors(start):
                    #while connected_node:
                        vertex = i.get_coor()
                        print(vertex)
                        print('gggg')
                        print(current)

                    
                    #while connected_node:
                        #vertex = connected_node.vertex
                        

                        if vertex not in self.dest_visited:
                            self.dest_queue.append(vertex)
                            self.dest_visited[vertex] = True
                            self.dest_parent[vertex] = current
                        else:
                            if not self.dest_visited[vertex]:
                                self.dest_queue.append(vertex)
                                self.dest_visited[vertex] = True
                                self.dest_parent[vertex] = current
                            
                        connected_node = connected_node.next
                        
            # Check for intersecting vertex
            def is_intersecting(self):
                
                # Returns intersecting node
                # if present else -1
                for i in self.src_visited.keys():
                    for j in self.dest_visited.keys():
                        if (i==j):
                            return i
                        
                return -1
        
            # Print the path from source to target
            def print_path(self, intersecting_node,
                        src, dest):
                                
                # Print final path from
                # source to destination
                path = list()
                path.append(intersecting_node)
                i = intersecting_node
                
                while i != src:
                    path.append(self.src_parent[i])
                    i = self.src_parent[i]
                    
                path = path[::-1]
                i = intersecting_node
                
                while i != dest:
                    path.append(self.dest_parent[i])
                    i = self.dest_parent[i]
                    
                print("*****Path*****")
                path = list(map(str, path))
                
                print(' '.join(path))
            
            # Function for bidirectional searching
            def bidirectional_search(self, src, dest , graph , list_edges):
                
                # Add source to queue and mark
                # visited as True and add its
                # parent as -1
                
                start = Node(src, 0)
                for i in graph.get_neighbors(start):
                    if (src, i.get_coor()) or (i.get_coor() , src)  not in list_edges:
                        self.add_edge(src, i.get_coor())
                        list_edges.append((src, i.get_coor()))
                self.src_queue.append(src)
                self.src_visited[src] = True
                self.src_parent[src] = -1
                
                # Add destination to queue and
                # mark visited as True and add
                # its parent as -1
                end = Node(dest, 0)
                for i in graph.get_neighbors(end):
                    if (dest, i.get_coor()) or (i.get_coor() , dest)  not in list_edges:
                        self.add_edge(dest, i.get_coor())
                        list_edges.append((dest, i.get_coor()))



                self.dest_queue.append(dest)
                self.dest_visited[dest] = True
                self.dest_parent[dest] = -1
        
                while self.src_queue and self.dest_queue:
                    
                    # BFS in forward direction from
                    # Source Vertex
                    self.bfs(graph , list_edges ,direction = 'forward')
                    print('sssss') 
                    # BFS in reverse direction
                    # from Destination Vertex
                    self.bfs(graph , list_edges ,direction = 'backward')
                    
                    # Check for intersecting vertex
                    intersecting_node = self.is_intersecting()
                    
                    # If intersecting vertex exists
                    # then path from source to
                    # destination exists
                    if intersecting_node != -1:
                        print(f"Path exists between {src} and {dest}")
                        print(f"Intersection at : {intersecting_node}")
                        self.print_path(intersecting_node,
                                        src, dest)
                        break
                        #exit(0)
                return -1
        n = 100
        
        # Source Vertex
        src = (2,3)
        
        # Destination Vertex
        dest = (5,5)
        
        # Create a graph
        graph2 = BidirectionalSearch(n)

        list_edges = []
        out = graph2.bidirectional_search(src, dest , graph ,list_edges)
        
        if out == -1:
            print(f"Path does not exist between {src} and {dest}")    
                    
         

        





        

       