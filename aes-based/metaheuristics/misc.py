# Author: Ivica Nikolic (cube444@gmail.com)

import random 

random.seed()

def generate_random_permutation(length):

	# Identity permutation
	p = list(range(length))

	# Random shuffle
	random.shuffle(p)

	return p
