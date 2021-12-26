import math
import random
import numpy
from numpy.random import randint
from numpy.random import rand

from population import convertToList, generatePopulation, randomChar,convertToSentense


problem="Barack Hussein Obama II is an American politician, lawyer, and author who served as a president of the United States. A member of the Democratic Party, Obama was the first African-American president of the United States"
problem=convertToList(problem)

#problem=[0,1,1,0,1,1,0,0,1,1,0,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,0,0,1]
population=[]

#buffer=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

population=generatePopulation(problem)

buffer=[b for b in range(2,len(population))]

print(len(problem))


def crossover(p1, p2, r_cross):
	c1, c2 = p1.copy(), p2.copy()
	if rand() < r_cross:
		pt = randint(1, len(p1)-2)
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]

def mutation(genome):
    found=False
    idx=0
    solved=False

    for i,v in enumerate(genome):
        if not found:
            if genome[i] == problem[i]:
                found=False
            elif genome[i] != problem[i]:
                idx=buffer.index(buffer[i])
                found=True
    
    if not found:
        return genome
    else:
        # genome[idx]=random.randint(0,1)
        genome[idx]=randomChar()
        return genome

            

        
for p in range(5):
    population.append([random.randint(0,1) for g in range(len(problem))])


def fitnessFunction(genome):
    fitness=0
    for index,value in enumerate(genome):
        if problem[index]==genome[index]:
            fitness+=1
    return fitness

for gen in range(20000):
    rankedGenomes=[]
    for chromosome in population:
        rankedGenomes.append((fitnessFunction(chromosome),chromosome))
    
    sort_by=lambda ranked:ranked[0]
    rankedGenomes.sort(key=sort_by,reverse=True)

    if rankedGenomes[0][0] > len(problem)-1:
        print(f"Solution: {convertToSentense(rankedGenomes[0][1])}")
        break

    pool=rankedGenomes[:100]

    crossed=crossover(pool[0][1],pool[1][1],2)

    nextGen=[]

    for n in range(1000):
        nextGen.append(
            mutation(random.choice(crossed))
        )
            

    population=nextGen

    print(f"======= GEN {gen} =======")
    print(rankedGenomes[0])

