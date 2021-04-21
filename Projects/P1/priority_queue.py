# Imports
import heapq
from graph import Node


class PriorityQueue:
	''' Priority Queue object '''

	def __init__(self):
		''' Constructor '''
		self.elements: List[Tuple[float, Node]] = []
    

	def empty(self) -> bool:
		''' Checks whether queue is empty or not '''
		return not self.elements
    

	def put(self, item, priority):
		''' Inserts a new element into the queue '''
		heapq.heappush(self.elements, (priority, (item.x, item.y)))
    

	def get(self):
		''' Returns the element with lowest weight from the queue '''
		return heapq.heappop(self.elements)[1]