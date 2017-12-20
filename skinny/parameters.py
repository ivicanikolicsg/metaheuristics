# Author: Ivica Nikolic (cube444@gmail.com)

class params:



	############################################ 
	# Limit parameters
	# CALL_LIMIT defines the maximal number of calls to the fitness (objective) function
	# calls_to_fitness is a variable that is increased after each call to the fitness function 
	CALL_LIMIT = 3000
	calls_to_fitness = 0


	############################################ 
	# Simulated annealing parameters 
	#
	INITIAL_TEMPERATURE = 1.5

	# BETA is used in the cooling schedule which is T <- T / (1 + beta * T)
	BETA = 0.002				


	############################################ 
	# Genetic algorithm parameters
	#

	# Population size
	N = 20 				

	# Selection functions
	SELECTION_ROULETTE_WHEEL 		= False
	SELECTION_STOCHASTIC_SAMPLING 	= True
	SELECTION_RANK_BASED 			= False
	SELECTION_TOURNAMENT 			= False

	# Crossover percentage
	# This means that the ELITISM percentage is 100 - CROSSOVER_PERCENTAGE
	CROSSOVER_PERCENTAGE = 80

	# Mutation
	MUTATION_PERCENTAGE = 1

