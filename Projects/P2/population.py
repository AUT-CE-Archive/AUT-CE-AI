# Imports
from dna import DNA
import random
import numpy as np
import matplotlib.pyplot as plt
import math

class Population:
	''' Population object '''

	def __init__(self, mutation_rate, generations_count, population_count, environment):
		''' Constructor '''

		self.mutation_rate = mutation_rate
		self.population = []		
		self.generations_count = generations_count
		self.population_count = population_count
		self.environment = environment
		self.mating_pool = []
		self.generation = 0
		self.best_fitness = 0
		self.fitness_mean = []
		self.fitness_best = []
		self.fitness_worst = []

		# create the Initial random population
		self.populate()
		self.calc_fitness()


	def improve(self, plot = False):
		''' Runs the methods of generic algortihm '''

		plt.title('Generic Algorithm Fitness function analysis\nFitness over generation')
		plt.xlabel('Generation')
		plt.ylabel('Fitness')

		for generation in range(self.generations_count):
			
			self.natural_selection()
			self.generate()
			self.calc_fitness()

			self.analyse_fitness()

			# Show generation info
			self.generation += 1		
			
			print(f'Genration #{self.generation} complete (Min-F: {self.fitness_worst[-1]}, MEAN-F: {self.fitness_mean[-1]}, MAX-F: {self.fitness_best[-1]})', end = '\t\t')
			if self.fitness_mean[-1] == self.fitness_best[-1]:
				print('Reached! - Overfit')
			else:
				print('Searching...')

			# plot
			if plot and generation % 2 == 0:
				plt.scatter(generation, self.fitness_mean[-1], c ='r', alpha = 0.4)
				plt.scatter(generation, self.fitness_best[-1], c ='b', alpha = 0.4)
				plt.scatter(generation, self.fitness_worst[-1], c ='g', alpha = 0.4)
				plt.pause(0.001)

		if plot:			
			plt.plot(range(self.generations_count), self.fitness_mean, c = 'r', label = 'Fitness Mean')
			plt.plot(range(self.generations_count), self.fitness_best, c = 'b', label = 'Best Fitness')
			plt.plot(range(self.generations_count), self.fitness_worst, c = 'g', label = 'Worst Fitness')
			plt.legend()
			plt.show()


	def analyse_fitness(self):
		''' Analyzes the fitness for the current population '''

		temp_best_fitness = None
		temp_worst_fitness = None
		fitness_sum = 0

		for dna in self.population:

			# Best firness
			if temp_best_fitness is None or dna.fitness > temp_best_fitness:
				temp_best_fitness = dna.fitness

			# Worst fitness
			if temp_worst_fitness is None or dna.fitness < temp_worst_fitness:
				temp_worst_fitness = dna.fitness

			# Average
			fitness_sum += dna.fitness

		self.fitness_best.append(temp_best_fitness)
		self.fitness_worst.append(temp_worst_fitness)
		self.fitness_mean.append(fitness_sum // len(self.population))


	def populate(self):
		''' Populates the population '''

		for i in range(self.population_count):

			# Construct a DNA
			dna = DNA(gene_len = len(self.environment))

			# Append DNA to population
			self.population.append(dna)


	def calc_fitness(self):
		''' Calculates the fitness over population '''

		for dna in self.population:
			dna.calc_fitness(environment = self.environment)


	def natural_selection(self):
		''' Naturally select parents for cross-over using mating pool '''

		# Clear the pool
		self.mating_pool = []

		# Find best fitness
		self.best_fitness = 0
		for dna in self.population:
			if dna.fitness > self.best_fitness:
				self.best_fitness = dna.fitness

		# Fill the mating pool
		for dna in self.population:
			self.mating_pool += [dna for f in range(round(dna.fitness))]

		# Randomize
		random.shuffle(self.mating_pool)


	def generate(self):
		''' Cross over for the mating pool '''

		new_population = []

		for i in range(len(self.population)):

			# Choose partners
			partner_1 = random.choice(self.mating_pool)
			partner_2 = random.choice(self.mating_pool)

			# Cross-over child
			child = partner_1.cross_over(partner_2)

			# Mutate child
			child.mutate(mutation_rate = self.mutation_rate)
			
			new_population.append(child)

		# Replace new generation
		self.population = new_population


	def get_chosens(self):
		''' Returns the DNAs meeting the ending condition '''

		chosens = [(dna.genes, dna.fitness) for dna in self.population if dna.fitness >= len(self.environment) - 1]
		chosens = sorted(chosens, key = lambda tup: tup[1])[::-1]
		return chosens