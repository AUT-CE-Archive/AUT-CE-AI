# Imports
import random


class DNA:
	''' DNA object '''

	def __init__(self, gene_len):
		''' Constructor '''

		# DNA properties
		self.genes = [random.choice([0, 1, 2]) for i in range(gene_len)]
		self.fitness = None


	def cross_over(self, partner):
		''' Cross over the gene with a DNA partner '''

		# Random seperation point for parent DNAs
		mid_point = random.randint(0, len(self.genes) - 1)

		# Create a child DNA
		child = DNA(len(self.genes))

		# Cross over (Randomly)
		child.genes = self.genes[:mid_point] + partner.genes[mid_point:]

		return child


	def mutate(self, mutation_rate):
		''' Mutate the DNA with a rate '''

		for gene in self.genes:
			chance = random.random()

			# Choose a random gene
			if chance < mutation_rate:
				gene = random.choice([0, 1, 2])


	def calc_fitness(self, environment):
		''' Calculates the fitness over the DNA '''

		max_len = 0
		temp_len = 0

		negative_score = 0
		mushrooms_score = 0
		jump_score = 0
		win_score = 0
		kill_score = 0

		for i in range(len(self.genes) - 1):

			# Ground threat!
			if environment[i + 1] == 'G' and self.genes[i] != 1:
				if temp_len > max_len:
					max_len = temp_len
					temp_len = 0
					
			# Air threat!
			elif environment[i + 1] == 'L' and self.genes[i] != 2:
				if temp_len > max_len:
					max_len = temp_len
					temp_len = 0

			# Collect mushrooms!
			elif environment[i] == 'M' and self.genes[i] != 0:
				if temp_len > max_len:
					max_len = temp_len
					temp_len = 0

				temp_len += 1
			else:

				# Mushroom score
				if environment[i] == 'M' and self.genes[i] == 0:
					mushrooms_score += 2

				# Negative score
				if environment[i] not in ['G', 'L'] and self.genes[i] in [1, 2]:
					negative_score += 0.25

				temp_len += 1

		if temp_len == len(environment) or max_len == len(environment):
			win_score = 2

		# Add engative scores
		temp_len -= negative_score

		# Add mushroom scores
		temp_len += mushrooms_score

		# Add jump score
		if self.genes[-1] == 1:
			jump_score += 1
		temp_len += jump_score

		# Add win score
		temp_len += win_score
		
		self.fitness = max_len if (max_len > temp_len) else temp_len