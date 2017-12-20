# Author: Ivica Nikolic (cube444@gmail.com)

class params:


	############################################ 
	# Parameters of the design
	#

	# The number of 128-bit words in the state
	SIZE = 6

	# The rate of the design, i.e. how many AES-round (the AES-NI instruction aesenc ) calls are required to process one 128-bit message word
	RATE = 2.5

	# The min and max number of AES calls per round; set -1 to ignore
	MIN_AES_CALLS = 4
	MAX_AES_CALLS = -1

	# The number of different rounds that will be repeating
	DIFFERENT_ROUNDS = 1





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

