import math
import random
import numpy as np

bag=[15,2,1,9,6,11,4,8,7,3]

target_weight=15
population_size=10

population=[]
fitnesses=[]


for p in range(population_size):
    population.append([random.randint(0,1) for i in range(len(bag))])

def fitnessFuction(chromosome):
    chosen_indexes=[]
    chosen_items=[]

    for index,weight in enumerate(chromosome):
        if weight == 1:
            chosen_indexes.append(index)
    
    for chosen in chosen_indexes:
        chosen_items.append(bag[chosen])

    weight_sum=sum(chosen_items)

    difference=abs(target_weight-weight_sum)

    if difference > 0:
        return target_weight/(difference+len(chosen_items))
    else:
        return 999/len(chosen_items)


def mutation(chromosome):
    new_chromosome=chromosome.copy()
    idx=random.randint(0,len(bag)-1)
    new_chromosome[idx]=random.randint(0,1)
    #print(f"Chromosome is {chromosome} new one is {new_chromosome}")
    return new_chromosome

    



for gen in range(10000):
    rankedBags=[]
    for item in population:
        rankedBags.append((fitnessFuction(item),item))
        fitnesses.append(fitnessFuction(item))
    sort_by=lambda ranked:ranked[0]
    rankedBags.sort(key=sort_by,reverse=True)
    pool=rankedBags[:100]
    elements=[]
    for element in pool:
        for gene in element[1]:
            elements.append(gene)
        
    if rankedBags[0][0] > 900:
        print(f"============= GEN {gen} ===============")
        print(f"Solution is {rankedBags[0][1]}")
        break
    
    newGen=[]


    for j  in range(population_size):
        s=[random.choice(elements) for e in range(0,len(bag))]
        newGen.append(
            mutation(s)
        )
    
    #print(newGen)

    
    population=newGen

    print(f"============= GEN {gen} ===============")
    print(rankedBags[0])

    
    

