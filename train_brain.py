import numpy as np
import math
import random
import genetic_brain
from numpy.random import randint
from numpy.random import rand

HEIGHT=600
WIDTH=900

training_data=[

]

population=[]

def crossover(p1, p2, r_cross):
    c1, c2 = p1.copy(), p2.copy()
    if rand() < r_cross:
        pt = randint(1, len(p1)-2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1,c2]
        

for p in range(100):
    population.append(genetic_brain.Brain(1,5,1))

for i in range(100):
    cords=(random.randint(10,WIDTH),random.randint(10,HEIGHT))
    if cords[0] < WIDTH/2:
        training_data.append(
            {
                "input":[cords[0]/WIDTH],
                "target":[0]
            }
        )
    else:
        training_data.append(
            {
                "input":[cords[0]/WIDTH],
                "target":[1]
            }
        )

def fitnessFunction(brain):
    for data in training_data:
        guess=brain.feedFoward(data["input"])
        if (guess[0] >= 0.5 and data["target"][0] >= 0.5) or (guess[0] < 0.5 and data["target"][0] < 0.5):
            brain.fitness+=1
        elif (guess[0] >= 0.5 and data["target"][0] < 0.5) or (guess[0] < 0.5 and data["target"][0] >= 0.5):
            brain.fitness-=1
    return brain.fitness

for gen in range(10000):


    # rankedBrains=[]
    # for brain in population:
    #     rankedBrains.append((fitnessFunction(brain),(brain.weights_ih,brain.weights_ho)))
    # sort_by=lambda ranked:ranked[0]
    # rankedBrains.sort(key=sort_by,reverse=True)

    # pool=rankedBrains[:100]

    rankedBrains=[]
    for brain in population:
        rankedBrains.append((fitnessFunction(brain),brain))
    sort_by=lambda ranked:ranked[0]
    rankedBrains.sort(key=sort_by,reverse=True)

    pool=rankedBrains[:100]

    agen_one_weights_ih=pool[0][1].weights_ih
    agen_one_weights_ho=pool[0][1].weights_ho

    agen_two_weights_ih=pool[1][1].weights_ih
    agen_two_weights_ho=pool[1][1].weights_ho


    input_hidden_flattened=agen_one_weights_ih.flatten().tolist()
    input_hidden_flattened2=agen_two_weights_ih.flatten().tolist()

    input_output_flattened=agen_one_weights_ho.flatten().tolist()
    input_output_flattened2=agen_two_weights_ho.flatten().tolist()

    crossed_ih=crossover(input_hidden_flattened,input_hidden_flattened2,2)
    crossed_ho=crossover(input_output_flattened,input_output_flattened2,2)

    parent1=genetic_brain.Brain(1,5,1)
    parent1.weights_ih=np.array(crossed_ih[0]).reshape(agen_one_weights_ih.shape)
    parent1.weights_ho=np.array(crossed_ho[0]).reshape(agen_one_weights_ho.shape)
    parent2=genetic_brain.Brain(1,5,1)
    parent2.weights_ih=np.array(crossed_ih[1]).reshape(agen_two_weights_ih.shape)
    parent2.weights_ho=np.array(crossed_ho[1]).reshape(agen_two_weights_ho.shape)

    parents=[parent1,parent2]

    nextGen=[]

    for n in range(100):
        chosen=random.choice(parents)
        chosen.weights_ih*np.random.uniform(0.1,0.99)
        chosen.weights_ho*np.random.uniform(0.1,0.99)
        nextGen.append(
            chosen
        )
    
    population=nextGen

    print(f"======== GEN {gen} =========")
    print(f"{rankedBrains[0]} --- {rankedBrains[0][1].weights_ih} --- {rankedBrains[0][1].weights_ho}")