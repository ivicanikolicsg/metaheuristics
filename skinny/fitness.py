# Author: Ivica Nikolic (cube444@gmail.com)

from gurobipy import *
import random, copy
from parameters import params
from fitness_milpaes import *


############################################ 
# Design parameters for SKINNY.
# TWEAKEY is the number of tweakey words
# ROUNDS is the target number of rounds for the related-tweakey characteristic
#
TWEAKEY = 3
ROUNDS =  11


############################################ 
# MILP parameters for the fitness function implemented in gurobi.
# OUTPUT_GUROBI can be set to output the gurobi output.
# USE_CORES is the number of cores gurobi will use to solve the model.
# 
OUTPUT_GUROBI  = 0
THREADS  = 30


def fitness_function( permute ):


	nextvar  = 0;
	dummy = 0;


	try:

		model = Model('milp')

		model.params.OutputFlag = OUTPUT_GUROBI 
		model.params.Threads = THREADS

		sbox_inputs = LinExpr()
		input_difference = LinExpr()
		tweakey_bytes = [ [LinExpr(),LinExpr(),LinExpr(),LinExpr() ],[LinExpr(),LinExpr(),LinExpr(),LinExpr() ],[LinExpr(),LinExpr(),LinExpr(),LinExpr() ],[LinExpr(),LinExpr(),LinExpr(),LinExpr() ]]


		# Set the initial state and tweakey state
		state = []
		tweakey = []
		for i in range(4):
			ls = []
			lt = []
			for j in range(4):
				ls.append( model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name = "x"+str(nextvar)) )
				nextvar += 1
				lt.append( model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name = "x"+str(nextvar)) )
				nextvar += 1
			state.append(ls)
			tweakey.append(lt)
		    
		model.update()

		# At least one byte of the input state or tweakey has a difference
		# Later will add the condition that perhaps some of the tweakey bytes have a difference
		for k in range(4):
		    for l in range(4):
		        input_difference += state[k][l] 



		# Positions of the tweakey bytes
		tpos = []
		for i in range(4):
			l = []
			for j in range(4):
				l.append( (i,j)) 
			tpos.append(l)


		# Go throught the rounds
		for r_big in range(ROUNDS):

			# Add the bytes of the tweakey
			for i in range(4):
			    for j in range(4):
					tweakey_bytes[i][j] += tweakey[tpos[i][j][0]][tpos[i][j][1]]


			SubBytes( state, sbox_inputs )
			nextvar, dummy = State_half_XOR( model, state, tweakey, dummy, nextvar);
			ShiftRows( state );
			nextvar, dummy = MixColumns( model, state, nextvar, dummy);
			
			# Permute the tweakey
			temp_tpos = copy.deepcopy(tpos)
			for i in range(4):
				for j in range(4):
					tweakey[i][j]  = model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name = "x"+str(nextvar)) 
					nextvar += 1
					temp_tpos[permute[4*i + j]/4][permute[4*i+j]%4] = ( tpos[i][j][0] ,  tpos[i][j][1] ) 

			model.update();

			tpos = copy.deepcopy(temp_tpos)
        


		# Input difference can be as well in the tweakey and has the be at least 1
		for i in range(4):
			for j in range(4):
			    input_difference += tweakey_bytes[i][j]
		model.addConstr( input_difference >= 1 );


		# Each tweakey byte has to be active certain number of times
		# either 0
		# or at least ROUNDS-(TWEAKEY-1)
		for i in range(4):
		    for j in range(4):
		        d = model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name = "d"+str(dummy))
		        dummy += 1
		        model.update()
		        model.addConstr( (ROUNDS-(TWEAKEY-1)) * d <= tweakey_bytes[i][j] )
		        model.addConstr( (ROUNDS            ) * d >= tweakey_bytes[i][j] )
		    

		# Set objective function
		model.setObjective(sbox_inputs, GRB.MINIMIZE)
		model.optimize()


		return model.objVal


	except GurobiError as e:
		print('Error code ' + str(e.errno) + ' : ' + str(e))
		return 0



	return 0



