# Imports
from tkinter import *


def animate(title, matrix, butters, goals, robot, routes):

	master = Tk()
	master.title(title)
	master.resizable(0, 0)

	# Tk properties
	size = 50
	width = len(matrix[0]) * size
	height = len(matrix) * size

	canvas = Canvas(master = master, width = width, height = height)

	for i, row in enumerate(matrix):
		for j, col in enumerate(row):

			if matrix[i][j] == '1':
				fill = '#833d0b'
			elif matrix[i][j] == '2':
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

			if (i, j) in butters:				# Butter
				text, fill = 'B', '#ffff00'
			elif (i, j) in goals:				# Goal
				text, fill = 'P', '#ffff00'
			elif (i, j) == robot:				# Robot
				text, fill = 'R', '#ffff00'
			elif matrix[i][j] == '-1':			# Obstacle
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