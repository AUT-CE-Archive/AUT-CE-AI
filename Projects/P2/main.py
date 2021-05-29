# Imports
from population import Population

# Driver function
if __name__ == '__main__':

	population = Population(
		mutation_rate = 0.1,
		generations_count = 150,
		population_count = 200,
		environment = '_G___M_____LL_____G__G______L_____G____MM',
	)

	population.populate()
	population.calc_fitness()
	population.improve(plot = False)

	chosens = population.get_chosens()
	if len(chosens) == 0:
		print('We didn\'t make it ):')
	else:
		print('Chosen paths:')	
		for chosen in chosens[:5]:
			print(chosen[1], ''.join([str(gene) for gene in chosen[0]]))