import numpy as np
import random
import math

from numpy.core.fromnumeric import size

population=[]

for pop in range(1000):
    population.append((np.random.normal(size=(2,2)),np.random.normal(size=(1,2))))


def problem(weights_hidden,weights_out):
    input=np.array([1,0])
    target=1
    hidden_input=np.dot(weights_hidden,input)
    output =np.dot(weights_out,hidden_input)
    return target-output[0]

def confirm(weights_hidden,weights_out):
    input=np.array([1,0])
    target=1
    hidden_input=np.dot(weights_hidden,input)
    output =np.dot(weights_out,hidden_input)
    return output

def fitness(weights_hidden,weights_out):
    ans=problem(weights_hidden,weights_out)
    if ans == 0:
        return 99999
    else:
        return abs(1/ans)


for gen in range(10000):
    rankedWeights=[]
    for w in population:
        rankedWeights.append((fitness(w[0],w[1]),w))
    rankedWeights.sort(reverse=True)

    pool=rankedWeights[:100]

    if rankedWeights[0][0] > 9999:
        print("***** Solution *******")
        print(confirm(rankedWeights[0][1][0],rankedWeights[0][1][1]))
        break

    elements=[]
    elements2=[]

    for element in pool:
        el1=element[1][0]
        el2=element[1][1]
        elements.append(el1)
        elements2.append(el2)
    
    newGen=[]

    for p in range(1000):
        w1=random.choice(elements)*np.random.uniform(0.99,1.01)
        w2=random.choice(elements2)*np.random.uniform(0.99,1.01)
        newGen.append((w1,w2))
    
    population=newGen
    


    print("========= GEN {gen} ==========")
    print(rankedWeights[0])



























# def problem(weights_hidden,weights_out,inputs):
#     outputs=[]
#     for x in inputs:
#         hidden_input=np.dot(weights_hidden,x)
#         output =np.dot(weights_out,hidden_input)
#         outputs.append(output)
#     return outputs

# weights_hidden=np.random.normal(size=(2,2))
# weights_out=np.random.normal(size=(1,2))

# inputs=np.array([[1,0],[0,1],[1,1],[0,0]])

# targets=np.array([[1],[1],[0],[0]])

# print(problem(weights_hidden,weights_out,inputs))