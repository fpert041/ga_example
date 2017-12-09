#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genetica Algorithm that solves a simple mathematical formula

Created on Fri Dec 8 2017

@author: pesa
"""

from population import Population
import numpy as np
import pandas as pd

# This problem is a mathematical maximisation problem

# define custom fitness function:
#  f(ch) = (x0 + x1) − (x2 + x3) + (x4 + x5 ) − (x6 + x7)
def fit_func(chrom):
    fitness = (chrom[0] + chrom[1]) - (chrom[2] + chrom[3])\
                + (chrom[4] + chrom[5]) - (chrom[6] + chrom[7])
    return fitness

# initialise a pupulation with 100 agents,
# each with a genotype: ch = (x0, x1, x2, x3, x4, x5, x6, x7)
    # where x0-7 can be any digit between zero to nine. 
# then pass in the fitness function we've just defined
pop_list = [
        [6, 5, 4, 1, 3, 5, 3, 2],
        [8, 7, 1, 2, 6, 6, 0, 1],
        [2, 3, 9, 2, 1, 2, 8, 5],
        [4, 1, 8, 5, 2, 0, 9, 4]
        ]
p = Population.from_pop_list(pop_list, fit_func) 

# TEST TO SEE WHETHER THE FITNESS INCREASES (and the distance dicreases)

p.evaluate()

for ind in p.members:
    print(ind.genotype, ind.fitness)

print('--------')  
for i in range (0, 100):  
    p.next_gen()
    
p.evaluate()

for ind in p.members:
    print(ind.genotype, ind.fitness)
