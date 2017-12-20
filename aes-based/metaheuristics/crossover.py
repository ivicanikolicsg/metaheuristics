# Author: Ivica Nikolic (cube444@gmail.com)

import random

def crossover_permutation( entries, p1, p2 ):


	c1 = list(range(entries))
	c2 = list(range(entries))

	k1 = k2 = 0
	while k1 == k2:
	    k1 = random.randint(0,entries-1)
	    k2 = random.randint(0,entries-1)

	if k2 < k1:
		k1,k2 = k1,k2


	used = [0] * entries
	u1 = [0] * entries
	u2 = [0] * entries

	for j in range(k1,k2):
	    c1[j] = p1[j]
	    u1[j] = 1;
	    for i in range(0,entries):
	        if p2[i] == p1[j]:
	            used[i] = 1

	last = entries-1
	for j in range(entries-1,-1,-1):
	    if not u1[j]:
	        while  last >=0 and used[last]:  last -= 1
	        c1[j] = p2[last];
	        last -= 1;

	used = [0] * entries
	for j in range(k1,k2):
	    c2[j] = p2[j]
	    u2[j] = 1
	    for i in range(entries):
	        if p1[i] == p2[j]:
	            used[i] = 1

	last = entries-1
	for j in range(entries-1,-1,-1):
	    if not u2[j]:
	        while last >=0 and used[last] :  last -= 1
	        c2[j] = p1[last]
	        last -=1

	return c1, c2


def crossover_permutation_3( entries, p1, p2 ):


	c1 = list(range(entries))
	c2 = list(range(entries))

	used1 = [0] * entries
	used2 = [0] * entries
	u1 = [0] * entries
	u2 = [0] * entries

	
	#
	#  Fill the children with parents from random positions (none consecutive !!!)
	#
	index = list(range(entries))
	random.shuffle(index)
	for k in range(entries):
		j = index[k]
		if random.randint(0,1):
		    if not used1[p1[j]]:
		    	c1[j] = p1[j]
		    	u1[j] = 1
		    	used1[p1[j]] = 1
		    if not used2[p2[j]]:
		    	c2[j] = p2[j]
		    	u2[j] = 1 
		    	used2[p2[j]] = 1
		else:
		    if not used1[p2[j]]:
		    	c1[j] = p2[j] 
		    	u1[j] = 1 
		    	used1[p2[j]] = 1
		    if not used2[p1[j]]:
		    	c2[j] = p1[j] 
		    	u2[j] = 1 
		    	used2[p1[j]] = 1

	#
	#  Try to get from the other parent
	# 
	for i in range(entries):
	    if not u1[i] and not used1[p1[i]] :
	    	c1[i] = p1[i] 
	    	u1[i] = 1 
	    	used1[p1[i]] = 1
	    if not u1[i] and not used1[p2[i]] :
	     	c1[i] = p2[i] 
	     	u1[i] = 1 
	     	used1[p2[i]] = 1
	    if not u2[i] and not used2[p1[i]] :
	    	c2[i] = p1[i]
	    	u2[i] = 1 
	    	used2[p1[i]] = 1
	    if not u2[i] and not used2[p2[i]] :
	    	c2[i] = p2[i] 
	    	u2[i] = 1 
	    	used2[p2[i]] = 1


	#
	#  Fill the rest in random order
	# 
	last = entries-1
	index = list(range(entries))
	random.shuffle(index)
	for k in range(entries):
	    j=index[k]
	    if not u1[j] :
	        while last >=0 and  used1[p2[last]] : last -=1
	        c1[j] = p2[last]
	        u1[j] = 1
	        used1[p2[last]] = 1
	        last -=1

	last = entries-1;
	index = list(range(entries))
	random.shuffle(index)
	for k in range(entries):
	    j=index[k]
	    if not u2[j] :
	        while last >=0 and  used2[p1[last]] : last -=1
	        c2[j] = p1[last]
	        u2[j] = 1
	        used2[p1[last]] = 1
	        last -=1


	return c1, c2

