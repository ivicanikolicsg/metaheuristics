# Author: Ivica Nikolic (cube444@gmail.com)

from gurobipy import *
import copy

def XOR_byte(model, x, y, nextvar, dummy):

	z = model.addVar(0.0, 1.0, 0.0, vtype = GRB.BINARY, name = "x"+str(nextvar) );
	d = model.addVar(0.0, 1.0, 0.0, vtype = GRB.BINARY, name = "d"+str(dummy) );
	model.update();

	model.addConstr(x + y + z - 2 * d >= 0, "c0");
	model.addConstr(d - x >= 0, "c1");
	model.addConstr(d - y >= 0, "c2");
	model.addConstr(d - z >= 0, "c3");

	nextvar += 1
	dummy += 1

	return z,nextvar,dummy


# State xor of type a = a + b 
def State_XOR(model, a, b, dummy, next):


	for i in range(4):
		for j in range(4):
			a[i][j],nextvar,dummy = XOR_byte( model, a[i][j], b[i][j], nextvar, dummy )

	return nextvar, dummy




def State_half_XOR(model, a, b, dummy, nextvar):

	for i in range(2):
		for j in range(4):
			a[i][j],nextvar,dummy = XOR_byte( model, a[i][j], b[i][j], nextvar, dummy )

	return nextvar, dummy


# The S-box Layer 
def SubBytes(a, sbox_inputs ):

	for i in range(4):
		for j in range(4):
			sbox_inputs += a[i][j]


# The Shift Rows Layer 
def ShiftRows(a): 
	tmp = list(range(4))
	for i in range(1,4):
	    for j in range(4):
	    	tmp[(j + i) % 4] = a[i][j]
	    for j in range(4):
	    	a[i][j] = tmp[j]



# The Mix Columns Layer 
def MixColumns(model, a, nextvar, dummy): 


	for j in range(4):

		z = {}
		z[3], nextvar, dummy = XOR_byte( model, a[0][j], a[2][j], nextvar, dummy )
		z[0], nextvar, dummy = XOR_byte( model, z[3], a[3][j], nextvar, dummy )
		z[2], nextvar, dummy = XOR_byte( model, a[1][j], a[2][j], nextvar, dummy )
		z[1] = a[0][j]

		a[0][j] = z[0]
		a[1][j] = z[1]
		a[2][j] = z[2]
		a[3][j] = z[3]


		model.update()

	return nextvar, dummy

