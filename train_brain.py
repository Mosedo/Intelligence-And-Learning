import math
import random
import numpy as np
import genetic_brain as brain


population=[]

for p in range(1000):
    population.append(brain.Brain(2,2,1))

def fitness(br):
    inputs=[[0,1],[0,0],[1,0],[1,1]]
    targets=[[1],[0],[1],[0]]
    brain_fitness=0
    errors=[]

    for index,input in enumerate(inputs):
        output=br.feedFoward(input)[0][0][0]
        error=output-targets[index][0]
        errors.append(error)
    
    mean_error=sum(errors)/len(errors)
    if mean_error==0:
        return 99999
    else:
        return abs(1/mean_error)
    

weights_ihidd=np.array([[2.37004549, 4.94034828],
                        [2.38451919, 5.04085224]])

weights_hout=np.array([[-5.34496779],
                        [ 5.35608423]])

bias_hidden=np.array([[-3.50020761, -1.62119614]])

bias_out=np.array([[-2.40216604]])

b=brain.Brain(2,2,1)
b.wh=weights_ihidd
b.wout=weights_hout
b.bh=bias_hidden
b.wout=bias_out

print(fitness(b))

# for gen in range(10000):
#     rankedBrains=[]
#     for bra in population:
#         rankedBrains.append((fitness(bra),bra))
#     sort_by=lambda ranked:ranked[0]
#     rankedBrains.sort(key=sort_by,reverse=True)
#     pool=rankedBrains[:400]


#     elements=[]

#     for element in pool:
#         el=element[1]
#         elements.append(el)
    
#     newGen=[]

#     for n in range(1000):
#         child_brain=brain.Brain(2,2,1)
#         chosen=random.choice(elements)
#         new_brain=chosen.mutate()
#         child_brain.wh=new_brain[0]
#         child_brain.wout=new_brain[1]
#         child_brain.bh=new_brain[2]
#         child_brain.bout=new_brain[3]
#         newGen.append(child_brain)
        

    
#     population=newGen



#     print(f"======== GEN {gen} =========")
#     print((rankedBrains[0],rankedBrains[0][1].wh,rankedBrains[0][1].wout,rankedBrains[0][1].bh,rankedBrains[0][1].bout))



