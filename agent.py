#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:37:23 2017

@author: pesa
"""

import numpy as np
import random
import numbers
import copy as cop

class Agent :
    """A simple agent class for a genetic algorithm"""
    
    # declare the variables that we want for this class
    genotype = []
    length = 0
    fitness = 0
    def fitness_func():
        return 0
    
    def __init__(self, length_or_genotype, fitness_func) :  # initialiser == constructor
        # initialise genotype array with an array of
        # randomly permutated numbers from 0 to length-1
        if isinstance(length_or_genotype, numbers.Number) :
            self.length = length_or_genotype
            self.genotype = np.random.permutation(length_or_genotype)
        # or directly with an externally passed genotype 
        else:
            self.genotype = length_or_genotype
            self.length = len(length_or_genotype)
        # then set the fitness function by passing it in
        self.fitness_func = fitness_func 
            
    def copy(self) :
        return cop.copy(self)
    
    def set_genotype(self, genotype):
        self.genotype = genotype
        self.length = len(genotype)
        return self.genotype
        
    def evaluate(self):
        self.fitness = self.fitness_func(self.genotype)
        return self
        
    def mutate(self, chance_as_n_between_0_and_1=0.05):
        for i in range(0, self.length):
            self.genotype[i] = int(random.uniform(0, 10)) if \
                (random.uniform(0, 1) < chance_as_n_between_0_and_1) else self.genotype[i]
            
            
'''    
    # let's define a way to mutate by chance: 
    def try_mutate(self, chance_as_n_between_0_and_1=0.1) :
        if random.uniform(0, 1) < chance_as_n_between_0_and_1:
            element1 = 0
            element2 = 0
            while element1 == element2 :
                element1 = random.randrange(self.length)
                element2 = random.randrange(self.length)
            temp = self.genotype[element1]
            self.genotype[element1] = self.genotype[element2]
            self.genotype[element2] = temp
        return self   
        
'''