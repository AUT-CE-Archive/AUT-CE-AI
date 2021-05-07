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

		self.fill = None

		if weight == 1:
			self.fill = '#833d0b'
		elif weight == 2:
			self.fill = '#f94141'
		else:
			self.fill = '#4d2307'
		
		self.draw()
		self.canvas.pack()


	def draw(self):
		''' Draws the object '''

		self.canvas.create_rectangle(			
			self.x,
			self.y,
			self.x + self.size,
			self.y + self.size,
			fill = self.fill,
			outline = 'black'
		)


class Item:

	def __init__(self, canvas, x, y, fill, text):		
		''' Constructor '''

		self.canvas = canvas
		self.x, self.y = x, y
		self.fill = fill
		self.text = text		

		self.draw()
		self.canvas.pack()


	def draw(self):
		''' Draws the object '''

		self.canvas.create_text(
			self.x,
			self.y,
			text = self.text,
			fill = self.fill,
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

		self.matrix = matrix
		self.butters = butters
		self.goals = goals
		self.robot = robot
		self.plates = []
		self.items = []

		self.master = Tk()
		self.master.title(self.title)
		self.master.resizable(0, 0)

		# Tk properties
		self.size = 50

		self.canvas = Canvas(
			master = self.master,
			width = len(self.matrix[0]) * self.size,
			height = len(self.matrix) * self.size
		)


	def animate(self):
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

				# Butters
				if (i, j) in self.butters:
					butter = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'B', fill = '#ffff00')
					butter.draw()
					self.items.append(butter)


				# Goals
				if (i, j) in self.goals:
					goal = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'P', fill = '#ffff00')
					goal.draw()
					self.items.append(goal)

				# Robot
				if (i, j) == self.robot:
					robot = Item(canvas = self.canvas, x = self.size * j + (self.size // 2), y = self.size * i + (self.size // 2), text = 'R', fill = '#ffff00')
					robot.draw()
					self.items.append(robot)
					
		mainloop()