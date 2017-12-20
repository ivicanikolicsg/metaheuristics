# Author: Ivica Nikolic (cube444@gmail.com)

import argparse
import sys
sys.path.append('./metaheuristics')
from simulated_annealing import *
from genetic_algorithm import *



# Check dependencies
try:
	import gurobipy
except:
	print( 'The fitness function for SKINNY is implemented as ILP.\nThe code uses Intels Gurobi to solve ILP, however, gurobipy library cannot be imported. \nInstall Gurobi to proceed.\nExiting...')
	exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--search",        help="Print debug info", action='store')

args = parser.parse_args()
if args.search:

	if int(args.search) == 1:
		simmulated_annealing()
	elif int(args.search) == 2:
		genetic_algorithm()
	else:
		print('Syntax: \n\tpython main.py --search METHOD\nwhere \nMETHOD=1 for simulated annealing, \nMETHOD=2 for genetic algorithm')			

else:
	print('Syntax: \n\tpython main.py --search METHOD\nwhere \nMETHOD=1 for simulated annealing, \nMETHOD=2 for genetic algorithm')			

