import random
import math
import numpy as np

class Gene:
    def __init__(self,innovation):
        self.innovation=innovation
        self.pointers=[]
        self.weight=np.random.uniform(-2,2)

hidden1=[i if i != 2 else " " for i in range(10)]
hidden2=[i if i != 4 else " " for i in range(7)]

def crossover(p1,p2,fitter):
    offspring=[]
    longer_genome=0
    if len(p1) >= len(p2):
        longer_genome=p1
    elif len(p2) >= len(p1):
        longer_genome=p2

    if fitter==1:
        for idx,gene in enumerate(longer_genome):
            pass



print(hidden1)
print(hidden2)