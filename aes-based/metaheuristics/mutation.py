# Author: Ivica Nikolic (cube444@gmail.com)


import random

def mutate_permutation( p ):

	k1 = k2 = 0
	while k1 == k2:
		k1 = random.randint(0,len(p)-1)
		k2 = random.randint(0,len(p)-1)

	p[k1],p[k2] = p[k2],p[k1]
