# Imports
from tkinter import *
from a_star import Astar
from ids import IDS

class Plate:

	def __init__(self, canvas, x, y, size, weight):		
		''' Constructor '''

		self.canvas = canvas
		self.x, self.y = x, y
		self.size = size
		self.weight = weight

		self.fill = None		
		
		self.draw()
		self.canvas.pack()


	def draw(self, fill = None):
		''' Draws the object '''

		if fill is None:
			if self.weight == 1:
				self.fill = '#833d0b'
			elif self.weight == 2:
				self.fill = '#f94141'
			else:
				self.fill = '#4d2307'
		else:
			self.fill = fill

		self.canvas.create_rectangle(			
			self.x,
			self.y,
			self.x + self.size,
			self.y + self.size,
			fill = self.fill,
			outline = 'black'
		)


class Item:

	def __init__(self, canvas, x, y, text):
		''' Constructor '''

		self.canvas = canvas
		self.x, self.y = x, y
		self.text = text

		self.draw()
		self.canvas.pack()


	def draw(self, fill = '#ffff00'):
		''' Draws the object '''

		self.canvas.create_text(
			self.x,
			self.y,
			text = self.text,
			fill = fill,
			font = ('freemono', 10, 'bold')
		)



class GUI:

	def __init__(self, model, matrix, butters, goals, robot):
		''' Constructor '''

		if isinstance(model, Astar):
			self.title = 'A* algorithm'
		elif isinstance(model, IDS):
			self.title = 'IDS algorithm'
		else:
			self.title = 'Bidirectional BFS algorithm'

		# Initialize
		self.model = model
		self.matrix, self.butters, self.goals, self.robot = matrix, butters, goals, robot
		self.plates, self.items = [], []

		# TK properties
		self.master = Tk()
		self.master.title(self.title)
		self.master.resizable(0, 0)
		self.size = 50

		# Create canvas
		self.canvas = Canvas(
			master = self.master,
			width = len(self.matrix[0]) * self.size,
			height = len(self.matrix) * self.size
		)		


	def animate(self, routes):
		''' Animates the GUI '''

		for i, row in enumerate(self.matrix):
			for j, col in enumerate(row):

				# Plates
				plate = Plate(
					canvas = self.canvas,
					x = self.size * j,
					y = self.size * i,
					size = self.size,
					weight = self.matrix[i][j]
				)
				plate.draw()
				self.plates.append(plate)


		# robot_route = set()
		# for pair, route in routes:
		# 	for butter_loc, robot_path in route:
		# 		for node in robot_path:
		# 			robot_place = Plate(
		# 				canvas = self.canvas,
		# 				x = self.size * node[0],
		# 				y = self.size * node[1],
		# 				size = self.size,
		# 				weight = self.matrix[node[0]][node[1]]
		# 			)
		# 			robot_place.draw(fill = '#4ae856')
		# 			self.items.append(robot_place)


		for i, row in enumerate(self.matrix):
			for j, col in enumerate(row):

				# Butters
				if (i, j) in self.butters:
					butter = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'B')
					butter.draw()
					self.items.append(butter)


				# Goals
				if (i, j) in self.goals:
					goal = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'P')
					goal.draw()
					self.items.append(goal)

				# Robot
				if (i, j) == self.robot:
					robot = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'R')
					robot.draw()
					self.items.append(robot)		
		
		mainloop()