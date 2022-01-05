import random
import numpy as np
import math
from population import convertToSentense,convertToList,generatePopulation,randomChar
from numpy.random import randint
from numpy.random import rand

population_size=1000
mutation_rate=0.01

problem="My name is Ibrahim Its a holiday. I am a bit tired today?"

problem=convertToList(problem)

population=generatePopulation(problem)

def fitnessFunction(chromosome):
    fitness=0
    for index,letter in enumerate(problem):
        if problem[index]==chromosome[index]:
            fitness+=1
    return fitness


def mutation(rate,chromosome):
    new_chromosome=chromosome.copy()
    for idx,letter in enumerate(chromosome):
        if np.random.uniform(0,1) < rate:
            new_chromosome[idx]=randomChar()
    return new_chromosome
    

def crossover(p1, p2, r_cross):
    c1, c2 = p1.copy(), p2.copy()
    if rand() < r_cross:
        pt = randint(1, len(p1)-2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

print(len(problem))

for gen in range(10000):
    rankedSent=[]
    for chromosome in population:
        rankedSent.append((fitnessFunction(chromosome),chromosome))
    rankedSent.sort(reverse=True)

    pool=rankedSent[:100]

    if rankedSent[0][0] > len(problem)-1:
        print(f"Solution: {convertToSentense(rankedSent[0][1])}")
        break

    parents=[pool[0][1],pool[random.randint(1,len(pool)-1)][1]]

    crossed=crossover(parents[0],parents[1],1)

    newGen=[]
    
    for n in range(1000):
        if n < 500:
            newGen.append(
                mutation(mutation_rate,crossed[0])
            )
        else:
            newGen.append(
                mutation(mutation_rate,crossed[1])
            )
    
    population=newGen


    print(f"========== GEN {gen} ===========")
    print(rankedSent[0])