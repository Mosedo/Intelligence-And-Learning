import math
import random
import numpy
from numpy.random import randint
from numpy.random import rand


problem=[0,1,1,0,1,1,0,0,1,1,0,0,1,0,1,1,0]
population=[]


def crossover(p1, p2, r_cross):
	c1, c2 = p1.copy(), p2.copy()
	if rand() < r_cross:
		pt = randint(1, len(p1)-2)
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]

def mutation(genome):

    genome[random.randint(0,len(genome)-1)]=random.randint(0,1)

    return genome

            

            
#print(len(problem))
            
        


#initialize population
for p in range(1000):
    population.append([random.randint(0,1) for g in range(len(problem))])


def fitnessFunction(genome):
    fitness=0
    for index,value in enumerate(genome):
        if problem[index]==genome[index]:
            fitness+=1
    return fitness

for gen in range(10000):
    rankedGenomes=[]
    for chromosome in population:
        rankedGenomes.append((fitnessFunction(chromosome),chromosome))
    rankedGenomes.sort(reverse=True)

    if rankedGenomes[0][0] > len(problem)-2:
        print(rankedGenomes[0])
        break

    pool=rankedGenomes[:100]

    crossed=crossover(pool[0][1],pool[1][1],1)

    nextGen=[]

    for n in range(1000):
        nextGen.append(
            mutation(random.choice(crossed))
        )
            

    population=nextGen

    print(f"======= GEN {gen} =======")
    print(rankedGenomes[0])


#print(fitnessFunction([0,1,1,0,1,1,0,0]))