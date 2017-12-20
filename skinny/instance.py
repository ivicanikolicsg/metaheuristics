# Author: Ivica Nikolic (cube444@gmail.com)

from __future__ import print_function
import sys
sys.path.append('./metaheuristics')

from misc import *
import copy
from parameters import params
from fitness import *
from crossover import *
from mutation import *

class Instance:




	def __init__(self):

		# In the case of SKINNY, the Instance is defined by a single permutation
		# For easier implementation, besides the 16-element permutation 'permute',
		# we define two  8-element permutations, 'perm1' and 'perm2' that define the left and right parts of 'permute'
		self.perm1 = generate_random_permutation(8)
		self.perm2 = generate_random_permutation(8)
		self.permute = self.compose_from_smaller( self.perm1, self.perm2 )


		#
		# The below attributes are universal, i.e. the exist in all Instances
		#

		# The value of the fitness function
		self.fit = -1

		# Infor about parents (used for debugging purposes)
		self.no_parents = 0
		self.parents_id = [-1,-1]
		self.parents_fit =[-1,-1]




	def print_instance(self):
		print("[Fitness: %3.0f] :  Permutation: " %  self.fit, end = '')
		for j in range(16):
			print('%2d ' % self.permute[j],end='')
		if self.no_parents > 0:
		    print("   Parents : ids( %2d : %2d ) : fitness(%3.0f : %3.0f) " % ( self.parents_id[0], self.parents_id[1] , self.parents_fit[0], self.parents_fit[1]), end = '' )
		print('')


	# Create a neighbour for a given instance
	# In case of SKINNY, is is produced with a swap in the left and the right side of the permutation
	def get_neighbour(self):
		new_m = copy.deepcopy(self)
		k2 = k3 = 0
		t2 = t3 = 0
		while k2 == k3 and t2 == t3:
			k2 = random.randint(0,7)
			k3 = random.randint(0,7)
			t2 = random.randint(0,7)
			t3 = random.randint(0,7)
		new_m.perm1[k2], new_m.perm1[k3] = new_m.perm1[k3], new_m.perm1[k2]
		new_m.perm2[t2], new_m.perm2[t3] = new_m.perm2[t3], new_m.perm2[t2]
		new_m.permute = new_m.compose_from_smaller( new_m.perm1, new_m.perm2 )

		return new_m


	# Calculate the fitness function for the instance
	def compute_fitness(self):

		global calls_to_fitness
		params.calls_to_fitness += 1

		# obviously this has to be replaced later
		self.fit = fitness_function( self.permute ) 


	# Given two parents (self and p2), create two children (c1,c2) with the use of the crosssover operators
	def crossover(self, p2, c1, c2):
		p1 = self
		
		c1.perm1, c2.perm1 = crossover_permutation_3( 8, p1.perm1, p2.perm1 )		
		c1.perm2, c2.perm2 = crossover_permutation_3( 8, p1.perm2, p2.perm2 )	

		c1.compose_from_smaller(c1.perm1, c1.perm2)	
		c2.compose_from_smaller(c2.perm1, c2.perm2)	


	# Mutate the instance
	def mutate(self):
		mutate_permutation( self.perm1 )
		mutate_permutation( self.perm2 )
		self.compose_from_smaller( self.perm1, self.perm2 )
		self.fit = -1;
		self.no_parents = 0;

	# Check if two instance are equal
	def is_equal(self,p2):

		return self.permute == p2.permute

	# This function is specific only to SKINNY
	# It takes two 8-element permutations and create one 16-element permutation
	def compose_from_smaller( self, p1, p2 ):
		p = list(range(16))
		for i in range(8):
			p[i] = p1[i] + 8
			p[i+8] = p2[i]
		return p
