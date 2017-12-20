# Author: Ivica Nikolic (cube444@gmail.com)

from __future__ import print_function
import sys
sys.path.append('./metaheuristics')

from misc import *
import copy,random
from parameters import params
from fitness import *
from crossover import *
from mutation import *


random.seed()

class Instance:


	def __init__(self):

		# In the case of AES-based constructions, the Instance is defined by several parameters

		# The masks 
		self.message_masks = [[[0] * params.SIZE for v1 in range(params.SIZE )] for v2 in range(params.DIFFERENT_ROUNDS)]
		self.aes_masks = params.DIFFERENT_ROUNDS * [ params.SIZE * [0]]
		self.feedforward_masks = params.DIFFERENT_ROUNDS * [ params.SIZE * [0]]

		# The number of AES calls per round
		self.aes_rounds = 0

		# The number of message words per round
		self.non_zero_message_words = 0

		# The rate of the construction, i.e. #AES_CALLS per 16-byte message words
		self.rate = 0


		self.generate_random_instance()



		#
		# The below attributes are universal, i.e. the exist in all Instances
		#

		# The value of the fitness function
		self.fit = -1

		# Infor about parents (used for debugging purposes)
		self.no_parents = 0
		self.parents_id = [-1,-1]
		self.parents_fit =[-1,-1]




	# Print the instance
	def print_instance(self):
		for i in range(params.DIFFERENT_ROUNDS):
		    print(" r[ %d ]  Fitness=%3.0f : Rate= %.2f  #AES=%2d #M=%2d    :  " % ( i, self.fit, self.rate, self.aes_rounds, self.non_zero_message_words), end='' );
		    print(" am: ",end='') 
		    for j in range(params.SIZE): print("%d" %  self.aes_masks[i][j], end='') 
		    print("  fm: ", end='') 
		    for j in range(params.SIZE):print("%d" % self.feedforward_masks[i][j], end='') 
		    print("  mm: ", end='')
		    for j in range(params.SIZE):
		        print("m[", end='')
		        for k in range(params.SIZE):
		            if self.message_masks[i][j][k] : print("%d" % k, end='')
		        print("] ",end='')
		    print("")



	# Create a neighbour for a given instance
	def get_neighbour(self):

		tr = 0
		while 0 == tr or (tr < 1000 and not new_m.has_good_rate() ):

			new_m = copy.deepcopy(self)


			first = True
			while first or (not aes_mask_flip and  not feedforward_mask_flip and not message_mask_flip):
				first = False
				aes_mask_flip = random.randint(0,1)
				feedforward_mask_flip = random.randint(0,1)
				message_mask_flip = random.randint(0,1)


			# flip in aes mask (change one 1 to 0, and one 0 to 1)
			exist_0 = 0
			exist_1 = 0
			for ij in range(params.DIFFERENT_ROUNDS):
			    for jk in range(params.SIZE):
			        if not new_m.aes_masks[ij][jk]: exist_0 = 1
			        if new_m.aes_masks[ij][jk]: exist_1 = 1

			if aes_mask_flip and exist_0 and exist_1:
			    # find 1 to change to 0
			    first = True
			    pos = 0
			    round = 0
			    while first or not new_m.aes_masks[round][pos]:
			    	first = False
			        round = random.randint(0,params.DIFFERENT_ROUNDS-1)
			        pos = random.randint(0,params.SIZE-1)
			    new_m.aes_masks[round][pos] = 0;

			    # find 0 to change to 1
			    first = True
			    pos2 = 0
			    round2 = 0
			    while first or ( new_m.aes_masks[round2][pos2] or (pos==pos2 and round==round2) ) :
					first = False
					round2 = random.randint(0,params.DIFFERENT_ROUNDS-1);
					pos2 = random.randint(0,params.SIZE-1)
			    new_m.aes_masks[round2][pos2] = 1;



			# Flip random feedforward mask bit
			if feedforward_mask_flip:
			    for i in range(params.DIFFERENT_ROUNDS):
					new_m.feedforward_masks[i][ random.randint(0,params.SIZE-1) ] ^= 1


			# Change message mask
			if message_mask_flip:

			    # assing random message word in the message mask
			    in1 = in2 = in3 = 0
			    first = True
			    while first or ( self.message_masks[in1][in2] == new_m.message_masks[in1][in2] ):
			    	first = False
			        in1 = random.randint(0,params.DIFFERENT_ROUNDS-1)

			        # Find max message index
			        max_mess_index = 0;
			        for  j in range(params.SIZE):
			            for  k in range(params.SIZE):
			                if new_m.message_masks[in1][j][k] and k > max_mess_index : 
			                	max_mess_index = k;

			        in2 = random.randint(0,params.SIZE-1)
			        for st in range(params.SIZE):
			        	new_m.message_masks[in1][in2][st] = 0
			        if random.randint(0,1):
			            new_m.message_masks[in1][in2][random.randint(0,max_mess_index+1)] = 1


			tr += 1

		if tr >= 10: 
			print("Could not find")

		return new_m


	# Calculate the fitness function for the instance
	def compute_fitness(self):

		global calls_to_fitness
		params.calls_to_fitness += 1

		self.fit = fitness_function( self.message_masks, self.aes_masks, self.feedforward_masks ) 


	# Given two parents (self and p2), create two children (c1,c2) with the use of the crosssover operators
	def crossover(self, p2, c1, c2):

		p1 = self
		c1 = Instance()
		c2 = Instance()
		trials = 0
		first = True
		while first or (trials < 10000 and ( not c1.has_good_rate() or  not c2.has_good_rate()) ):

			first = False
			trials += 1

			# Byte by byte message crossover
			for i in range(params.DIFFERENT_ROUNDS):
			    for j in range(params.SIZE):
			        if random.randint(0,2):
			            c1.message_masks[i][j] = copy.deepcopy(p1.message_masks[i][j])
			            c2.message_masks[i][j] = copy.deepcopy(p2.message_masks[i][j])
			        else:
			            c1.message_masks[i][j] = copy.deepcopy(p2.message_masks[i][j])
			            c2.message_masks[i][j] = copy.deepcopy(p1.message_masks[i][j])

			for i in range(params.DIFFERENT_ROUNDS):
			    for j in range(params.SIZE):
			        if random.randint(0,2):
			            c1.aes_masks[i][j] = p1.aes_masks[i][j]
			            c2.aes_masks[i][j] = p2.aes_masks[i][j]
			        else:
			            c1.aes_masks[i][j] = p2.aes_masks[i][j]
			            c2.aes_masks[i][j] = p1.aes_masks[i][j]

			for i in range(params.DIFFERENT_ROUNDS):
			    for j in range(params.SIZE):
			        if random.randint(0,2):
			            c1.feedforward_masks[i][j] = p1.feedforward_masks[i][j]
			            c2.feedforward_masks[i][j] = p2.feedforward_masks[i][j]
			        else:
			            c1.feedforward_masks[i][j] = p2.feedforward_masks[i][j]
			            c2.feedforward_masks[i][j] = p1.feedforward_masks[i][j]



		if trials >= 10000:
		    printf("cannot perform crossver. will generated random instances")
		    c1.generate_random_instance()
		    c2.generate_random_instance()

		c1.fit = -1;
		c2.fit = -1;




	# Mutate the instance
	def mutate(self):

		new_t = self.get_neighbour()

		self = copy.deepcopy(new_t)
		self.fit = -1;
		self.no_parents = 0;


	# Check if two instance are equal
	def is_equal(self,p2):

		return self.message_masks == p2.message_masks and self.aes_masks == p2.aes_masks and self.feedforward_masks == p2.feedforward_masks


	# Check if instance has a good rate,
	# i.e. around aes_round/non_zero_message_words is approximately equal to RATE
	def has_good_rate(self):


	    aes_rounds = 0
	    non_zero_message_words = 0

	    for i in range(params.DIFFERENT_ROUNDS):
	        for j in range(params.SIZE):
	            nz = 0;
	            for k in range(params.SIZE):
	                if  self.message_masks[i][k][j]: nz = 1
	            non_zero_message_words += nz
	        for j in range(params.SIZE):
	            aes_rounds += self.aes_masks[i][j];

	    # additional requirements on the contruction
	    if params.MIN_AES_CALLS > 0 and aes_rounds < params.MIN_AES_CALLS: return False
	    if params.MAX_AES_CALLS > 0 and aes_rounds > params.MAX_AES_CALLS: return False

	    self.rate = 0
	    self.non_zero_message_words = non_zero_message_words
	    self.aes_rounds = aes_rounds

	    if 0 == non_zero_message_words: return False
	    if 0 == aes_rounds:  return False

	    self.rate = float(aes_rounds) / non_zero_message_words 
	    return  ( float(aes_rounds) / non_zero_message_words <= 1.01 * params.RATE ) and ( float(aes_rounds) / non_zero_message_words >= 0.99*params.RATE ) 
	


	# Generate random instance
	def generate_random_instance( self ):


		first = True
		while first or not self.has_good_rate():

			first = False

			# feedforward masks
			self.feedforward_masks = params.DIFFERENT_ROUNDS * [ params.SIZE * [0]]
			for i in range(params.DIFFERENT_ROUNDS):
				for j in range(params.SIZE): 
					self.feedforward_masks[i][j] = random.randint(0,1)

			# aes masks
			count = 0
			message_words = 0
			while  0==count or not( message_words*params.RATE / count >= 0.99and message_words*params.RATE/count <= 1.01 ):
				count = 0
				self.aes_masks = params.DIFFERENT_ROUNDS * [ params.SIZE * [0]]
				for i in range(params.DIFFERENT_ROUNDS):
				    for j in range(params.SIZE):
				        v = random.randint(0,1)
				        count += v
				        self.aes_masks[i][j] = v
				message_words = int(count / params.RATE)


			# message masks
			rmw = [0] * params.DIFFERENT_ROUNDS  
			sum = 0
			for i in range(params.DIFFERENT_ROUNDS-1):
			    rmw[i] = random.randint(0,message_words - sum-1)
			    sum += rmw[i]
			rmw[params.DIFFERENT_ROUNDS-1] = message_words - sum;

			for i in range(params.DIFFERENT_ROUNDS):
				mask = 0
				first = True
				while first or ( mask != (((1<<rmw[i]) - 1) if (rmw[i]>0) else 0)):
					first = False
					self.message_masks = [[[0] * params.SIZE for v1 in range(params.SIZE )] for v2 in range(params.DIFFERENT_ROUNDS)]
					mask = 0;
					for j in range(params.SIZE):
						which = random.randint(0,rmw[i])
						if which >= 1:
							mask |= 1<<(which-1)
							self.message_masks[i][j][which-1] = 1

			self.fit = -1
			self.rate = 0
			self.non_zero_message_words = 0
			self.aes_rounds = 0

