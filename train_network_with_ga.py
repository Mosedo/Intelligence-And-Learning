import random
import numpy as np
import math
from numpy.random import randint
from numpy.random import rand
import mybrain as brain

population_size=1000
# mutation_rate=0.1
# crossover_rate=0.95

mutation_rate=0.1
crossover_rate=0.5

inputs=[[1,0],[1,1],[0,1],[0,0]]
outputs=[[1],[0],[1],[0]]

population=[]

for p in range(population_size):
    population.append(brain.Brain(2,5,1))

def fitnessFunction(genome):
    errors=[]
    for index,input in enumerate(inputs):
        guess=genome.feedFoward(input)[0]
        error=abs(guess-outputs[index])
        errors.append(error[0])
    mean_error=sum(errors)/len(errors)

    if mean_error==0:
        return 99999
    else:
        return abs(1/mean_error)

def mutation(rate,chromosome):
    new_chromosome=chromosome.copy()
    for idx,letter in enumerate(chromosome):
        if np.random.uniform(0,1) < rate:
            new_chromosome[idx]=random.uniform(-7,1)
    return new_chromosome

def crossover(p1, p2, r_cross):
    # c1, c2 = p1.copy(), p2.copy()
    # if rand() < r_cross:
    #     pt = randint(1, len(p1)-2)
    #     c1 = p1[:pt] + p2[pt:]
    #     c2 = p2[:pt] + p1[pt:]
    # return [c1, c2]

    for c in range(2):
        if random.uniform(0,1) > crossover_rate:
            c1, c2 = p1.copy(), p2.copy()
            if rand() < r_cross:
                pt = randint(1, len(p1)-2)
                c1 = p1[:pt] + p2[pt:]
                c2 = p2[:pt] + p1[pt:]
            return [c1, c2]
        else:
            return [p1,p2]

for gen in range(10000):
    rankedGenomes=[]
    for genome in population:
        rankedGenomes.append((fitnessFunction(genome),genome))
    sort_by=lambda ranked:ranked[0]
    rankedGenomes.sort(key=sort_by,reverse=True)

    pool=rankedGenomes[:100]

    if rankedGenomes[0][0] > 50:
        print(f"Solution for [1,0] {rankedGenomes[0][1].feedFoward([1,0])}")
        print(f"Solution for [0,1] {rankedGenomes[0][1].feedFoward([0,1])}")
        print(f"Solution for [1,1] {rankedGenomes[0][1].feedFoward([1,1])}")
        print(f"Solution for [0,0] {rankedGenomes[0][1].feedFoward([0,0])}")
        break

    # parents=[pool[0][1],pool[random.randint(1,len(pool)-1)][1]]
    parents=[pool[0][1],pool[1][1]]

    parent1_wh=parents[0].wh.flatten().tolist()
    parent1_wout=parents[0].wout.flatten().tolist()
    parent2_wh=parents[1].wh.flatten().tolist()
    parent2_wout=parents[1].wout.flatten().tolist()

    #Do crossover of parents
    crossed_wh=crossover(parent1_wh,parent2_wh,1)
    crossed_wout=crossover(parent1_wout,parent2_wout,1)

    #make new parents
    new_parent1_wh=np.array(crossed_wh[0]).reshape(parents[0].wh.shape)
    new_parent2_wh=np.array(crossed_wh[1]).reshape(parents[0].wh.shape)
    new_parent1_wout=np.array(crossed_wout[0]).reshape(parents[0].wout.shape)
    new_parent2_wout=np.array(crossed_wout[1]).reshape(parents[0].wout.shape)

    #make new networks from the new parents with new weights and biasis
    parent1=brain.Brain(2,5,1)
    parent1.wh=new_parent1_wh
    parent1.wout=new_parent1_wout
    parent1.bh=np.array(mutation(mutation_rate,parents[0].bh.flatten().tolist())).reshape(population[0].bh.shape)
    parent1.bout=np.array(mutation(mutation_rate,parents[0].bout.flatten().tolist())).reshape(population[0].bout.shape)

    parent2=brain.Brain(2,5,1)
    parent2.wh=new_parent2_wh
    parent2.wout=new_parent2_wout
    parent2.bh=np.array(mutation(mutation_rate,parents[1].bh.flatten().tolist())).reshape(population[0].bh.shape)
    parent2.bout=np.array(mutation(mutation_rate,parents[1].bout.flatten().tolist())).reshape(population[0].bout.shape)




    #create new population
    newGen=[]

    for p in range(1000):
        if p < 500:
            new_brain=brain.Brain(2,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent1.wh.flatten().tolist())).reshape(population[0].wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent1.wout.flatten().tolist())).reshape(population[0].wout.shape)
            newGen.append(new_brain)
        else:
            new_brain=brain.Brain(2,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent2.wh.flatten().tolist())).reshape(population[0].wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent2.wout.flatten().tolist())).reshape(population[0].wout.shape)
            newGen.append(new_brain)
        
    population=newGen


    print(f"======== GEN {gen} =========")
    print(rankedGenomes[0])

        
