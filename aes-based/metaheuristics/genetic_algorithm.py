# Author: Ivica Nikolic (cube444@gmail.com)

from __future__ import print_function
from instance import *
from parameters import params


def genetic_algorithm():

	N = params.N

	# The working generation
	G = []

	# 
	# Populate the generation
	#
	print('Populating the initial generation')
	for i in range(N):
		G.append( Instance() )
		G[i].print_instance()


	generation_no = 0
	while True:

		#
		# Make sure the number of iterations does not exceed some predefined value
		#
		if params.calls_to_fitness >  params.CALL_LIMIT:
			break


		print('\n'+'='*100 + '\nGeneration: %4d   :  Fitness calls:  %d\n' % (generation_no,params.calls_to_fitness) + '='*100)
		generation_no += 1

		#
		#   Compute fitness for the entire population
		# 
		best = 0
		for i in range(N):
		    if G[i].fit < 0: G[i].compute_fitness()
		    if G[i].fit > G[best].fit: best = i
		    print("[%3d]: " %  i, end='') 
		    G[i].print_instance()
		print("\t\x1b[32mBest fitnes: %.0f \x1b[0m  " % ( G[best].fit ) , end='\n\t' )
		G[best].print_instance( );


        #
        #   Sort the population by fitness (this is required for some of the selection functions)
        # 
		for i in range(N):
			for j in range(0,i):
			    if G[j].fit >= G[i].fit:
			    	G[j],G[i] = G[i],G[j]


		# 
		# Determine ranges for the selection function.
		# ranges determine the probability 
		#
		ranges = {}
		if params.SELECTION_ROULETTE_WHEEL or params.SELECTION_STOCHASTIC_SAMPLING:
			tot_fit = float(0);
			for i in range(N): tot_fit += G[i].fit
			left_range = float(0)
			for i in range(N):
			    ranges[i] = (left_range , left_range + (  (G[i].fit/ tot_fit ) if (tot_fit > 0) else  (1.0/N) ) )
			    left_range = ranges[i][1];
		else:
			tot_fit = float(0)
			left_range = float(0)
			pos = 1 
			count = 0
			for i in range(N):
			    tot_fit += pos
			    count +=1
			    ranges[i] = ( left_range , left_range + pos)
			    left_range += pos
			    if i+1< N and G[i].fit < G[i+1].fit:
			        pos+= count
			        count = 0

			for i in range(N): 
				ranges[i] = (ranges[i][0] / tot_fit , ranges[i][1] / tot_fit )



		#
		# Select indices for crossover, 
		# i.e. select pairs of parents for reproduction
		#
		best_p1 = {}
		best_p2 = {}
		if params.SELECTION_ROULETTE_WHEEL or params.SELECTION_RANK_BASED:
			for j in range(int(0.01*params.CROSSOVER_PERCENTAGE/2*N)):
				best_p1[j] = best_p2[j] = 0
		        while best_p1[j] == best_p2[j] :
		            ch1 = random.random()
		            ch2 = random.random()
		            best_p1[j] = best_p2[j] = 0
		            for i in range(N):
		                if ranges[i][0] <= ch1 and ranges[i][1] > ch1 : best_p1[j] = i
		                if ranges[i][0] <= ch2 and ranges[i][1] > ch2 : best_p2[j] = i

		elif params.SELECTION_STOCHASTIC_SAMPLING:
			ch1 = random.random()
			ch2 = random.random()
			for j in range(int(0.01*params.CROSSOVER_PERCENTAGE/2*N)):
				best_p1[j] = best_p2[j] = 0
				for i in range(N):
				    if ranges[i][0] <= ch1 and ranges[i][1] > ch1 : best_p1[j] = i
				    if ranges[i][0] <= ch2 and ranges[i][1] > ch2 : best_p2[j] = i

				if best_p1[j] == best_p2[j] : 
					best_p2[j] = (best_p2[j] + 1) % N

				ch1 += 1/(0.01*params.CROSSOVER_PERCENTAGE/2*N); ch1 = (ch1-1) if ch1 > 1 else ch1
				ch2 += 1/(0.01*params.CROSSOVER_PERCENTAGE/2*N); ch2 = (ch2-1) if ch2 > 1 else ch2

			# random shuffle of the second parent indices (so two parent will not maintain the same distance all the time)
			for j in range(100*N):
			    k1 = random.randint(0,int((0.01*params.CROSSOVER_PERCENTAGE/2*N ))-1);
			    temp = best_p2[ j % int((0.01*params.CROSSOVER_PERCENTAGE/2*N)) ];
			    best_p2[j % int((0.01*params.CROSSOVER_PERCENTAGE/2*N )) ] = best_p2[k1];
			    best_p2[k1] = temp;
			for j in range(int(0.01*params.CROSSOVER_PERCENTAGE/2*N)):
			    if best_p1[j] == best_p2[j]: 
			    	best_p2[j] = (best_p2[j] + 1) % N;
		    

		elif params.SELECTION_TOURNAMENT:
			# Binary tournament selection
			tsize = 2;
			for j in range(int(0.01*params.CROSSOVER_PERCENTAGE/2*N)):
				best_p1[j] = best_p2[j] = 0
				while  best_p1[j] == best_p2[j] :
				    best_p1[j] = random.randint(0,int((0.01*params.CROSSOVER_PERCENTAGE/2*N ))-1)
				    for i in range(tsize - 1):
				        temp = random.randint(0, int((0.01*params.CROSSOVER_PERCENTAGE/2*N ))-1)
				        if G[temp].fit > G[best_p1[j]].fit : 
				        	best_p1[j] = temp;
				    best_p2[j] = random.randint(0,int((0.01*params.CROSSOVER_PERCENTAGE/2*N))-1)
				    for i in range(tsize - 1):
				        temp = random.randint(0,int((0.01*params.CROSSOVER_PERCENTAGE/2*N ))-1)
				        if G[temp].fit > G[best_p2[j]].fit:
				        	best_p2[j] = temp



        #
        # Crossover
        #
		top_new_m = 0
		temp_G = {}
		for j in range(int(0.01*params.CROSSOVER_PERCENTAGE/2*N)):

			temp_G[top_new_m + 0 ] = Instance()
			temp_G[top_new_m + 1 ] = Instance()

			G[best_p1[j]].crossover ( G[best_p2[j]], temp_G[top_new_m], temp_G[top_new_m+1] )

			temp_G[top_new_m].no_parents = 2;
			temp_G[top_new_m].parents_id[0] = best_p1[j];
			temp_G[top_new_m].parents_id[1] = best_p2[j];
			temp_G[top_new_m].parents_fit[0] = G[best_p1[j]].fit;
			temp_G[top_new_m].parents_fit[1] = G[best_p2[j]].fit;

			temp_G[top_new_m+1].no_parents = 2;
			temp_G[top_new_m+1].parents_id[0] = best_p1[j];
			temp_G[top_new_m+1].parents_id[1] = best_p2[j];
			temp_G[top_new_m+1].parents_fit[0] = G[best_p1[j]].fit;
			temp_G[top_new_m+1].parents_fit[1] = G[best_p2[j]].fit;

			top_new_m += 2;


		for i in range(top_new_m):
			G[i] = temp_G[i]


		# 
		#  Mutation
		# 
		for i in range(top_new_m):
			if 100*random.random() <= params.MUTATION_PERCENTAGE :
				G[i].mutate()		        	

		# 
		#  Removal of duplicates
		# 
		for i in range(N):
		    for j in range(0,i):
		    	if G[i].is_equal(G[j]):
		    		G[j] = Instance()



