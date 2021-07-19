from tkinter import *
import random

class GUI:

	def __init__(self, tables, n, size):
		''' Constructor '''
		
		self.size = size
		self.n = n
		self.spacing = self.size // n
		self.tables = tables

		self.window = Tk()
		self.window.title("Project 3 GUI")

		self.canvas = Canvas(self.window, width = size, height = size)
		self.canvas.pack()		

		# Draw initials
		self.draw_lines()
		self.draw_numbers(tables[0])


	def draw_lines(self):
		''' Draws lines on the canvas '''

		spacing = self.spacing		

		for i in range(self.n):
			self.canvas.create_line(spacing * i, 0, spacing * i, self.size, fill="#476042", width = 1)
			self.canvas.create_line(0, spacing * i, self.size, spacing * i, fill="#476042", width = 1)


	def draw_numbers(self, table):
		''' Main update function '''

		spacing = self.spacing
		bias = spacing // 2

		for i in range(self.n):
			for j in range(self.n):
				self.canvas.create_text(spacing * j + bias, spacing * i + bias, text = table[i][j])


	def animate(self):
		''' Redraws on Canvas '''

		for table in self.tables:

			self.canvas.delete("all")
			self.draw_lines()
			self.draw_numbers(table)
			self.canvas.update()


def draw_gui(tables, row, size):

	gui = GUI(tables, row, size)
	gui.animate()
	gui.window.mainloop()


if __name__ == '__main__':

	tables = []
	for i in range(100):
		table = [[0 for y in range(4)] for x in range(4)]

		for j in range(4):
			for k in range(4):
				table[j][k] = random.choice([0, 1])
		tables.append(table)

	draw_gui(tables, 4, 400)