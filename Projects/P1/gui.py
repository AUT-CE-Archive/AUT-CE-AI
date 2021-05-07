# Imports
from tkinter import *
from a_star import Astar
from ids import IDS

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


	def animate(self):

		master = Tk()
		master.title(self.title)
		master.resizable(0, 0)

		# Tk properties
		size = 50
		width = len(self.matrix[0]) * size
		height = len(self.matrix) * size

		canvas = Canvas(master = master, width = width, height = height)

		for i, row in enumerate(self.matrix):
			for j, col in enumerate(row):

				fill = None

				if self.matrix[i][j] == 1:
					fill = '#833d0b'
				elif self.matrix[i][j] == 2:
					fill = '#f94141'
				else:
					fill = '#4d2307'

				# Draw node
				canvas.create_rectangle(
					size * j,
					size * i,
					size * (j + 1),
					size * (i +  1),
					fill = fill,
					outline = 'black'
				)

				text = None
				if (i, j) in self.butters:				# Butter
					text, fill = 'B', '#ffff00'
				elif (i, j) in self.goals:				# Goal
					text, fill = 'P', '#ffff00'
				elif (i, j) == self.robot:				# Robot
					text, fill = 'R', '#ffff00'
				elif self.matrix[i][j] == '-1':			# Obstacle
					text, fill = 'X', '#bfbfbd'

				if text is not None:
					canvas.create_text(
						size * j + (size // 2),
						size * i + (size // 2),
						text = text,
						fill = fill,
						font = ('freemono', 10, 'bold')
					)

		canvas.pack()
		canvas.mainloop()