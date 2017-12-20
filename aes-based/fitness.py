# Author: Ivica Nikolic (cube444@gmail.com)

from gurobipy import *
import random, copy
from parameters import params
from fitness_milpaes import *




############################################ 
# MILP parameters for the fitness function implemented in gurobi.
# OUTPUT_GUROBI can be set to output the gurobi output.
# USE_CORES is the number of cores gurobi will use to solve the model.
# 
OUTPUT_GUROBI  = 0
THREADS  = 30
ROUNDS =  30				# max length the trail. can increase to more, but only when needed to double check that the result is correct



def fitness_function(message_masks, aes_masks, feedforward_masks):

	nextvar  = 0;
	dummy = 0;


	try:

		model = Model('milp')

		model.params.OutputFlag = OUTPUT_GUROBI 
		model.params.Threads = THREADS

		sbox_inputs = LinExpr()
		first_round_message = LinExpr()


		# Set the initial state
		state = []
		for i in range(params.SIZE):
			l2 = []
			for j in range(4):
				l = []
				for k in range(4):
					l.append( model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name = "x"+str(nextvar)) )
					nextvar += 1
				l2.append(l)
			state.append(l2)

		model.update();

		# No difference in the intial state
		for  l in range(params.SIZE):
		    for i in range(4):
		        for j in range(4):
		            model.addConstr(state[l][i][j]  == 0)



		# Go throught the rounds
		for r_big in range(ROUNDS/params.DIFFERENT_ROUNDS):

		    for r_small in range(params.DIFFERENT_ROUNDS):


				# Go one round (below temp is a temporary state)

				# Apply the AES rounds according to the aes masks
				temp = [ [[0] * 4 for st1 in range(4)] for st2 in range(params.SIZE) ]
				for i in range(params.SIZE):
				    for j in range(4): 
				    	for k in range(4):
				        	temp[(i+1)%params.SIZE][j][k] = state[i][j][k]
				    if aes_masks[r_small][i] :
				        nextvar,dummy = AES_ROUND(model, temp[(i+1)%params.SIZE], sbox_inputs, nextvar, dummy )


				# Apply the XOR feedforward according to the masks
				for i in range(params.SIZE):
				    if feedforward_masks[r_small][i] :
				        nextvar,dummy = State_XOR(model, temp[i], state[i], dummy, nextvar)


				# XOR the message words according to the message masks

				# First assign new variables for the message bytes
				message_vars = [ [[0] * 4 for st1 in range(4)] for st2 in range(params.SIZE) ]

				for i in range(params.SIZE):

				    used = 0
				    for j in range(params.SIZE):
				        if message_masks[r_small][j][i] :
				            used = 1

				    if used:
				        for j in range(4):
				            for k in range(4):
				                message_vars[i][j][k] = model.addVar(0.0, 1.0, 0.0, vtype=GRB.BINARY, name="x"+str(nextvar));
				                nextvar += 1
				model.update();


				# Xor the variables according to the masks
				for i in range(params.SIZE):			#For each word of the state
				    for j in range(params.SIZE):		#For each message state

				        if message_masks[r_small][i][j] :
				            nextvar,dummy = State_XOR( model, temp[i], message_vars[j], dummy, nextvar );
				            if 0 == r_big :
				                for k in range(4):
				                    for l in range(4):
				                        first_round_message += message_vars[j][k][l] ;


				# Store back from temp to state
				for i in range(params.SIZE):
					for j in range(4):
						for k in range(4):
							state[i][j][k] = temp[i][j][k]



		#No difference in the state after all ROUNDS
		for l in range(params.SIZE):
		    for i in range(4):
		        for j in range(4):
		            model.addConstr(state[l][i][j]  == 0)


		#At least one message byte in the first round has a difference
		model.addConstr( first_round_message >= 1 )




		# Set objective function
		model.setObjective(sbox_inputs, GRB.MINIMIZE)
		model.optimize()


		return model.objVal


	except GurobiError as e:
		print('Error code ' + str(e.errno) + ' : ' + str(e))
		return 0



	return 0



