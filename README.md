# Metaheuristics for design of symmetric-key crypto primitives

The repository contains Python implementation of metaheuritics (simulated annearling and genetic algorithms) to design of two types of symmetric-key primitives (tweaked [SKINNY](https://link.springer.com/chapter/10.1007%2F978-3-662-53008-5_5) lightweight block cipher and the [fastest AES-round based constructions](https://link.springer.com/chapter/10.1007%2F978-3-662-52993-5_17]) ).



## Quick Start

To run the metaheuristics, go the the appropriate directory (skinny or aes-based) and run

`python main.py --search 1` for search based on simulated annealing 

`python main.py --search 2` for search based on genetic algorithm 

## Benchmarks

The code can run for very long time. To speed things up, you can change some of the parameters specified in parameters.py and in fitness.py. In particular, you can make the search easier (more feasible) by:
1. Target lighter versions of the primitives, i.e. smaller state size. Check parameters.py for more details.
2. Target lower security levels. Check parameters.py for more details.
3. Use more cores: THREAD count in defined in fitness.py.


## Dependencies

1. Intel's Gurobi

## Paper

The paper explaining the approach can be found [here](https://eprint.iacr.org/2016/1162.pdf)
