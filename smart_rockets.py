import numpy as np
import random
import pygame
import math
import sys
vec = pygame.math.Vector2
from population import randomChar,convertToList,convertToSentense,generateASentence

rankedWords=[]

while True:

    generated=generateASentence(10)
    print(convertToSentense(generated))

    fitness=int(input("Enter fitness: "))

    if fitness == -1:
        break
    else:
        rankedWords.append((fitness,generated))

sort_by=lambda ranked:ranked[0]

rankedWords.sort(key=sort_by,reverse=True)

print(rankedWords[:3])