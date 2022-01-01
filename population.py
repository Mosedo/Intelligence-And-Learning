import math
import numpy as np
import random
import string



chars=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','!',' '," ",'_','.','\'','?',',','-']
random.shuffle(chars)

temp_chars=chars.copy()

chosen_list=[False for i in range(len(chars))]

population_size=1000


# def sentenseList(sent):
#     sentence=[]
#     for letter in s:
#         sentence.append(letter)
#     return sentence

def randomChar():
   global temp_chars
   chosen=random.choice(temp_chars)
   idx=temp_chars.index(chosen)

   if chosen_list[idx]:
       return chosen
   else:
       chosen_list[idx]=True
       return chosen

def randomCharTest(letter):
   global temp_chars
   chosen=letter
   idx=temp_chars.index(chosen)

   if chosen_list[idx]:
       print("Running again")
   else:
       chosen_list[idx]=True
       return chosen

   

def randomCharStart():
   return random.choice(chars)

def clearTemp():
    global chosen_list
    chosen_list=[False for i in range(len(chars))]




def generatePopulation(s):
    population=[]
    for p in range(population_size):
        population.append([randomCharStart() for i in range(len(s))])
    return population

def generateASentence(s):
    return [randomChar() for r in range(s)]

def calculateFitness(chromosome,actual):
    fitness=0
    for index,value in enumerate(actual):
        if actual[index]==chromosome[index]:
            fitness+=1
            
    return fitness

def calculateHalf(array):
    arr=len(array)

    if arr%2==0:
        return int(len(array)/2)
    else:
        return int(len(array)/2+0.5)

def doCrossOver(x,y):
    x_middle=calculateHalf(x)
    y_middle=calculateHalf(y)

    for i in range(int(x_middle),len(x)):
        temp=x[i]
        x[i]=y[i]
        y[i]=temp

    return [x,y]

def randomMutation(chromosome):
    random_char=randomChar()
    random_position=random.randint(0,len(chromosome)-1)
    new_chromosome=chromosome
    new_chromosome[random_position]=random_char
    return new_chromosome

def getFittest(fitnesses):
    fitness=fitnesses
    first_max=max(fitness)
    max_one=fitness.index(first_max)
    fitness[max_one]=0
    second_max=max(fitness)
    max_two=fitness.index(second_max)
    return (max_one,max_two)

def convertToSentense(chromosome):
    result=""
    for gene in chromosome:
        result+=gene
    return result

def howManyToMutate(lst,mutation_rate):
    return math.ceil(len(lst)*mutation_rate)

def pointsMutation(chromosome,mutation_rate):
    num_mutate=round(mutation_rate*len(chromosome))
    new_chromosome=chromosome
    for m in range(num_mutate):
        new_chromosome[random.randint(0,len(chromosome)-1)]=random.choice(string.ascii_letters)
    
    return new_chromosome

def convertToList(s):
    problem=[]
    for l in s:
        problem.append(l)
    return problem


#print(pointMutation([1,2,3,4,4,3,6,8,5,4,6,3,5,2,6,3,7,2,5,3,2],0.1))

