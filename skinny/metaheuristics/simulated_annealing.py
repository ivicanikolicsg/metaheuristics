# Author: Ivica Nikolic (cube444@gmail.com)

from __future__ import print_function
import math
from instance import *
from parameters import params


def simmulated_annealing():


    instance = Instance()
    instance.compute_fitness()

    T = params.INITIAL_TEMPERATURE;
    alltime_best_fitness = -1
    alltime_best = list(range(16))
    while True:

        #
        # Make sure the number of iterations does not exceed some predefined value
        #
        if params.calls_to_fitness >  params.CALL_LIMIT:
            break


        #
        # Pick a neighbour and compute its fitness
        # 
        neighbour = instance.get_neighbour()
        neighbour.compute_fitness()


        #
        # Change current instance if
        #  1) the new has a better fitness, or
        #  2) the probability is higher
        #
        transition_probability = math.exp( (float)( neighbour.fit-instance.fit)/ T );
        better = neighbour.fit >= instance.fit;
        change = 0;
        if better or ( random.random() < transition_probability ) :
            change = neighbour.fit - instance.fit;
            instance = neighbour

        #
        #  Print current member
        # 
        print('='*100)
        if not better: print("Fitness calls: %5ld  Temperature: %6.3f  Probability:  %.3f " % (params.calls_to_fitness, T, transition_probability)  )
        else:          print("Fitness calls: %5ld  Temperature: %6.3f  " % (params.calls_to_fitness, T ) )

        if change != 0: 
            print(("\x1b[31m" if (change<0) else "\x1b[32m"), end="")

        instance.print_instance()
        print("\x1b[0m", end='')
        if alltime_best_fitness >= 0:
            print('\tBest found fitness: %d' % alltime_best.fit)


        #
        # Cooling schedule
        #
        T = T / ( 1 + params.BETA * T )

        if instance.fit > alltime_best_fitness:
            alltime_best_fitness = instance.fit
            alltime_best = copy.deepcopy(instance)


    if alltime_best_fitness >= 0:
        print('Best found')
        alltime_best.print_instance()

