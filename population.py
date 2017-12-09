#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:13:31 2017

@author: pesa
"""

import agent as ag
import numpy as np
import random
import copy as cp

class Population :
    """A container of agents for a genetic algorithm"""
   
#agent = ag.Agent(8) # initialise the agent object with a genotype lenght of 8
    length = 0
    members = []
    def fit_func(): return 0
    
    # =========================================================================

    def __init__(self, pop_len, ag_len, fitness_func) :
        self.fit_func = fitness_func
        self.length = pop_len
        self.members = np.empty(pop_len, dtype=object)
        for i in range(0, self.length) :
            self.members[i] = ag.Agent(ag_len, fitness_func)
            
    @classmethod
    def from_pop_list(self, list_of_agents, fitness_func):
        self = self(len(list_of_agents), len(list_of_agents[0]), fitness_func)
        self.members = np.empty(self.length, dtype=object)
        for i in range(0, self.length):
            self.members[i] = ag.Agent(list_of_agents[i], fitness_func)
        return self
            
            
    # =========================================================================        

    def crossover_one(self, agentX, agentY) :
        chromo_len = agentX.length # length of a valid chromosome
        # create a 2D list to store children's chromosomes
        child1_gen = np.empty(chromo_len)      
        child2_gen = np.empty(chromo_len) 
        
        # one-point middle crosss
        mid_index = int(chromo_len/2)
        
        for i in range(0, mid_index):
            child1_gen[i]=agentX.genotype[i]
            child2_gen[i]=agentY.genotype[i]
        for i in range(mid_index, chromo_len):
            child2_gen[i]=agentX.genotype[i]
            child1_gen[i]=agentY.genotype[i]
            
        ch1 = ag.Agent(child1_gen, agentX.fitness_func)
        ch2 = ag.Agent(child2_gen, agentX.fitness_func)
        
        return ch1, ch2
    
    def crossover_two(self, agentX, agentY):
        chromo_len = agentX.length # length of a valid chromosome
        # create a 2D list to store children's chromosomes
        child1_gen = np.empty(chromo_len)      
        child2_gen = np.empty(chromo_len) 
        
        # two-point "fixed" crossings
        q1 = int(chromo_len/4)
        q2 = chromo_len - q1
        
        for i in range(0, q1):
            child1_gen[i]=agentX.genotype[i]
            child2_gen[i]=agentY.genotype[i]
        for i in range(q1, q2):
            child2_gen[i]=agentX.genotype[i]
            child1_gen[i]=agentY.genotype[i]
        for i in range(q2, chromo_len):
            child1_gen[i]=agentX.genotype[i]
            child2_gen[i]=agentY.genotype[i]
        
        ch1 = ag.Agent(child1_gen, agentX.fitness_func)
        ch2 = ag.Agent(child2_gen, agentX.fitness_func)
        
        return ch1, ch2
    
    
    def crossover_uni(self, agentX, agentY):
        chromo_len = agentX.length # length of a valid chromosome
        # create a 2D list to store children's chromosomes
        child1_gen = np.empty(chromo_len)      
        child2_gen = np.empty(chromo_len) 
        
        # Uniform crossing with 50% probability
        p = 0.5
        
        for i in range(0, chromo_len):
            u = np.random.random()
            if(u<p):
                child1_gen[i]=agentX.genotype[i] 
                child2_gen[i]=agentY.genotype[i] 
            else:
                child1_gen[i]=agentY.genotype[i] 
                child2_gen[i]=agentX.genotype[i] 
    
        ch1 = ag.Agent(child1_gen, agentX.fitness_func)
        ch2 = ag.Agent(child2_gen, agentX.fitness_func)
        
        return ch1, ch2
    
    
    # =========================================================================
     
    # evaluate all the members of the population
    # and sort them in order of fitness
    def evaluate(self):
        temp = cp.copy(self.members)
        arr = np.zeros(self.length)
        for i in range(0,self.length):
            self.members[i].evaluate()
            arr[i]=self.members[i].fitness
        indx = np.argsort(arr)
        for i in range(0,self.length):
            self.members[self.length-1-i] = temp[indx[i]]
        return self.members
    
    
    # =========================================================================
    
    # go to the next generation:
    # Use one-point crossover to cross the best 2 chromosomes
    # Use two-point crossover to cross the 2nd and 3rd best individuals
    # Use uniform crossover to cross the 1st and 3rd best chromosomes
    def next_gen(self):
        for i in range(0,self.length):
            self.members[i].mutate()
            
        self.evaluate()

        temp_pop = cp.copy(self.members)
        self.members = np.empty(6, dtype=object)
        self.length = 6
        
        self.members[0], self.members[1]=\
            self.crossover_one(temp_pop[0],temp_pop[1])
        self.members[2], self.members[3]=\
            self.crossover_one(temp_pop[1],temp_pop[2])
        self.members[4], self.members[5]=\
            self.crossover_one(temp_pop[0],temp_pop[2])
            
'''    
    # =========================================================================
     
    # choose 1 or more pairs of parents (choosing amongst the fittest)
    def roulette_wheel(self, times = 1):
        prob = np.empty(self.length)
        parents_i = np.empty(times*2)        
        for i in range (0, times*2, 2): 
            
            def choose_parent():
                tot_fitness = 0
                for ind in self.members:
                    tot_fitness += ind.fitness
                prob[0] = self.members[0].fitness / tot_fitness
                for j in range (1, self.length):
                    prob[j] = self.members[j].fitness / tot_fitness + prob[j-1]
                fate = np.random.rand(1)
                p=0
                while fate > prob[p]:
                    p+=1
                return p

            parent_ind1 = choose_parent()
            parent_ind2 = choose_parent()
            
            # the commented lines would make parents never be the same
            # (that is each parent can only have a chance to procreate once)
            #while parent_ind1 in parents_i :
                #parent_ind1 = choose_parent()
            
            while (parent_ind1 == parent_ind2) : #| (parent_ind2 in parents_i):
                parent_ind2 = choose_parent()
            
            parents_i[i] = parent_ind1
            parents_i[i+1] = parent_ind2
            
        return parents_i
    
    # =========================================================================
    
    
    # go to the next generation:
    # 1 - do an evaluation and sorting of the population
    # 2 - use the roulette wheel of probabilities to see 
    ## which parents will procreate (number of couples passed in as argument)
    # 3 - make those parents procreate and have children
    # 4 - the parents perish and the children take their places
    def next_gen2(self, couples = 3):
        self.evaluate()
            
        parent_indeces = self.roulette_wheel(couples).astype(int)
        
        for i in range (0, len(parent_indeces), 2):
            p1 = self.members[parent_indeces[i]]
            p2 = self.members[parent_indeces[i+1]]
            c1, c2 = self.crossover(p1, p2)
            self.members[-(i+1)] = c1.try_mutate()
            self.members[-(i+2)] = c2.try_mutate()
            
        return self.members
    
'''  
             