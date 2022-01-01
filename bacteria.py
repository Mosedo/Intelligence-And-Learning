import pygame
import math
import numpy as np
import sys
vec = pygame.math.Vector2
import genetic_brain as brain
import random
import genetic_brain as brain
from numpy.random import randint
from numpy.random import rand


HEIGHT=700
WIDTH=1200
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 3
MAX_FORCE = 0.1
APPROACH_RADIUS = 120

find_pool=True;

remove_list=[]

eaten=[]

pool=[]

new_agents=[]

mutation_rate=0.8

generation=1;

population_size=100

total_food=40


training_data=[

]

savedAgents=[]

fit_temp=0

win=pygame.display.set_mode((WIDTH,HEIGHT))

class Food:
    def __init__(self,index):
        self.position=vec(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
        self.color=(0,255,255)
        self.index=index
        self.code=random.uniform(0.5,1)
        self.removed=False
        self.size=4
    def draw(self):
        pygame.draw.circle(win, self.color, (self.position.x,self.position.y), self.size)

class Poison:
    def __init__(self,index):
        self.position=vec(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
        self.color=(255,0,0)
        self.index=index
        self.code=random.uniform(0,0.49)
        self.size=4
        self.removed=False
    def draw(self):
        pygame.draw.circle(win, self.color, (self.position.x,self.position.y), self.size)

foods=[]

for i in range(100):
    if i <= total_food:
        foods.append(Food(i))
    else:
       foods.append(Poison(i)) 

class Agent:
    def __init__(self,idx):
        self.position=vec(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
        self.vel=vec(0,0)
        self.acceleration=vec(0,0)
        self.color=(0,255,0)
        self.index=idx
        self.brain=brain.Brain(6,5,1)
        self.random_directions=[(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))]
        self.searching_food=True
        self.nearby_food=[]
        self.search_radius=100
        self.life=100
        self.not_food=[]
        self.fitness=0

    
    def mapFood(self,f):
        if ((f.position.x > self.position.x) and f.position.x <= self.position.x+self.search_radius) or ((f.position.y > self.position.y) and f.position.y <= self.position.y+self.search_radius):
            if f is not None:
                return f

    def drawAgent(self):


        if(len(self.not_food) > 2 and self.life > 0):
            self.life-=10
            self.fitness-=1
            self.not_food.clear()
            
        
        if self.life <= 0:
            temp_index=self.index
            try:
                addToPool(agents[self.index])
                removeAgent=agents.pop(self.index)
                savedAgents.append(removeAgent)
                #del agents[self.index]
                reorganizeList(temp_index)
            except IndexError:
                print("Passed")
                

        pygame.draw.circle(win, self.color, (self.position.x,self.position.y), 5)

        if self.life == 100:
            self.color=(0,255,255)
        elif self.life <= 75 and self.life >= 50:
            self.color=(255,165,0)
        elif self.life <= 50 and self.life >=25:
            self.color=(255,255,0)
        elif self.life <= 25 and self.life >=0:
            self.color=(255,0,0)
        elif self.life <= 0:
            foods.append(Food(len(foods)-1))
            self.color=(255,0,0)

    def follow_mouse(self):
        mpos = pygame.mouse.get_pos()
        self.acc = (mpos - self.pos).normalize() * 0.5
    
    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def seek_with_approach(self, target):
        self.desired = (target - self.position)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        
        return steer
    
    def seek_food(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.position += self.vel
    
    def seek_random(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.position += self.vel

        if len(self.nearby_food) < 1:
            if abs(self.random_directions[0][0]-self.position.x) < 3:
                self.random_directions[0]=(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
                found_food=list(map(self.mapFood,foods))
                found_food=[fd for fd in found_food if fd is not None and fd.removed is False]

                if len(found_food) > 0:
                    for ff in found_food:
                        self.nearby_food.append(ff)

                        if ff.code < 0.5:
                            self.nearby_food.append(ff)
                
        else:
            self.searching_food=False
        
        


        
    


            
        
        
    def search_food(self):
        

        global total_food
        
        if self.searching_food:
            self.seek_random(self.random_directions[0])
            
        else:
            if len(self.nearby_food) > 0:
                if abs(self.nearby_food[0].position.x-self.position.x) < 3:
                    try:
                        inputs=[
                            self.position.x/WIDTH,
                            self.position.y/HEIGHT,
                            self.nearby_food[0].code,
                            self.nearby_food[0].position.x/WIDTH,
                            self.nearby_food[0].position.y/HEIGHT,
                            self.life/100
                        ]

                        # print(inputs)
                        # print()

                        i_array=np.array(inputs)

                        o_array=i_array/np.max(i_array)

                        o_array=o_array.flatten()

                        inputs=o_array.tolist()

                        #pred=self.brain.feedFoward(inputs,self.nearby_food[0].code)[0]

                        # pred=self.brain.feedFoward(self.nearby_food[0].code,self.nearby_food[0].code)[0]

                        pred=self.brain.feedFoward(inputs)[0][0][0]
                        print(pred)

                        #print(pred)
                        

                        if pred >= 0.5:
                            foods[self.nearby_food[0].index].removed=True
                            foods[self.nearby_food[0].index].color=(0,0,0)
                            total_food-=1
                            foods[self.nearby_food[0].index].size=0

                            if pred >= 0.5 and foods[self.nearby_food[0].index].removed==False:
                                self.not_food.append(1)
                            if pred < 0.5 and foods[self.nearby_food[0].index].removed==True:
                                self.not_food.append(1)
                            

                            if self.nearby_food[0].code < 0.5:
                                if self.life > 0:
                                    self.life-=20
                                    self.fitness-=5
                                    if self.life < 40:
                                        foods.append(Food(len(foods)-1))
                            
                            if self.nearby_food[0].code < 0.5:
                                self.not_food.append(1)
                            else:
                                if self.life < 100:
                                    self.life+=2
                                    self.fitness+=10
                        elif pred < 0.5:
                            if self.nearby_food[0].code >= 0.5:
                                if self.life > 0:
                                    self.life-=20
                                    self.fitness-=5
                                    if self.life < 40:
                                        #foods.append(Poison(len(foods)-1))
                                        foods.append(Poison(len(foods)-1))
                        
                    except IndexError:
                        pass

                    
                        
                    del self.nearby_food[0]
                    


                else:
                    self.seek_food(self.nearby_food[0].position)
                    # if self.brain.feedFoward(self.nearby_food[0].code)[0][0]>=0.5: 
                    #     self.seek_food(self.nearby_food[0].position) 
                    # else:
                    #     del self.nearby_food[0]
                    #     self.random_directions[0]=(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
                    
            else:
                if len(self.nearby_food) > 0:
                    self.seek_food(self.nearby_food[0].position)
                else:
                    self.random_directions[0]=(random.randint(10,WIDTH-10),random.randint(10,HEIGHT-10))
                    self.searching_food=True
                    eaten.append(1)
            
        


    

agents=[Agent(i) for i in range(population_size)]

def addMoreFood():
    rnum=random.randint(0,1)
    if rnum == 0:
        for i in range(100):
            if i <= 30:
                foods.append(Food(i))
            else:
                foods.append(Poison(i)) 
    else:
        for i in range(100):
            if i <= 30:
                foods.append(Poison(i))
            else:
                foods.append(Food(i)) 


win=pygame.display.set_mode((WIDTH,HEIGHT))

testing=True

def deleteAllFoods():
    sum=0
    for food in foods:
        if food.removed is True:
            sum+=1
    
    if sum == len(foods):
        foods.clear()
        remove_list.clear()
        addMoreFood()
    
def addAFood():
    idx=foods[len(foods)-1].index+1
    foods.append(Food(idx))
    idx2=foods[len(foods)-1].index+1
    foods.append(Food(idx2))
    idx3=foods[len(foods)-1].index+1
    foods.append(Food(idx3))
    idx4=foods[len(foods)-1].index+1
    foods.append(Food(idx4))
    idx5=foods[len(foods)-1].index+1
    foods.append(Food(idx5))
    idx6=foods[len(foods)-1].index+1
    foods.append(Food(idx6))
    idx7=foods[len(foods)-1].index+1
    foods.append(Food(idx7))
    idx8=foods[len(foods)-1].index+1
    foods.append(Food(idx8))
    idx9=foods[len(foods)-1].index+1
    foods.append(Food(idx9))
    idx10=foods[len(foods)-1].index+1
    foods.append(Food(idx10))

    idx11=foods[len(foods)-1].index+1
    foods.append(Poison(idx11))
    idx12=foods[len(foods)-1].index+1
    foods.append(Poison(idx12))
    idx13=foods[len(foods)-1].index+1
    foods.append(Poison(idx13))
    idx14=foods[len(foods)-1].index+1
    foods.append(Poison(idx14))
    idx15=foods[len(foods)-1].index+1
    foods.append(Poison(idx15))
    idx16=foods[len(foods)-1].index+1
    foods.append(Poison(idx16))

    idx17=foods[len(foods)-1].index+1
    foods.append(Poison(idx17))
    idx18=foods[len(foods)-1].index+1
    foods.append(Poison(idx18))
    idx19=foods[len(foods)-1].index+1
    foods.append(Poison(idx19))
    idx20=foods[len(foods)-1].index+1
    foods.append(Poison(idx20))

def reorganizeList(index):
    for agent in agents:
        if agent.index > index:
            agent.index-=1



def addToPool(agent):
    pool.append(agent.brain) 

def mutation(rate,chromosome):
    new_chromosome=chromosome.copy()
    for idx,letter in enumerate(chromosome):
        if np.random.uniform(0,1) < rate:
            new_chromosome[idx]=random.uniform(-7,1)
    return new_chromosome

def crossover(p1, p2, r_cross):

    # for c in range(2):
    #     if random.uniform(0,1) > crossover_rate:
    #         c1, c2 = p1.copy(), p2.copy()
    #         if rand() < r_cross:
    #             pt = randint(1, len(p1)-2)
    #             c1 = p1[:pt] + p2[pt:]
    #             c2 = p2[:pt] + p1[pt:]
    #         return [c1, c2]
    #     else:
    #         return [p1,p2]

    c1, c2 = p1.copy(), p2.copy()
    if rand() < r_cross:
        pt = randint(1, len(p1)-2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]  

def doEvolution():
    global agents
    global generation
    global foods
    global pool
    rankedBrains=[]


    global birds
    global savedBirds
    rankedBirds=[]
    for savedagent in savedAgents:
        rankedBirds.append((savedagent.fitness,savedagent.brain))
    sort_by=lambda ranked:ranked[0]
    rankedBirds.sort(key=sort_by,reverse=True)
    pool=rankedBirds[:10]

    parents=[pool[0][1],pool[random.randint(1,len(pool)-1)][1]]


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
    parent1=brain.Brain(6,5,1)
    parent1.wh=new_parent1_wh
    parent1.wout=new_parent1_wout
    parent1.bh=np.array(mutation(mutation_rate,parents[0].bh.flatten().tolist())).reshape(savedAgents[0].brain.bh.shape)

    parent1.bout=np.array(mutation(mutation_rate,parents[0].bout.flatten().tolist())).reshape(savedAgents[0].brain.bout.shape)

    parent2=brain.Brain(6,5,1)
    parent2.wh=new_parent2_wh
    parent2.wout=new_parent2_wout
    parent2.bh=np.array(mutation(mutation_rate,parents[1].bh.flatten().tolist())).reshape(savedAgents[0].brain.bh.shape)
    parent2.bout=np.array(mutation(mutation_rate,parents[1].bout.flatten().tolist())).reshape(savedAgents[0].brain.bout.shape)

    #create new population
    newGen=[]

    for p in range(100):
        if p < 50:
            new_brain=brain.Brain(6,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent1.wh.flatten().tolist())).reshape(savedAgents[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent1.wout.flatten().tolist())).reshape(savedAgents[0].brain.wout.shape)
            new_bird=Agent(p)
            new_bird.brain=new_brain
            newGen.append(new_bird)
        else:
            new_brain=brain.Brain(6,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent2.wh.flatten().tolist())).reshape(savedAgents[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent2.wout.flatten().tolist())).reshape(savedAgents[0].brain.wout.shape)
            new_bird=Agent(p)
            new_bird.brain=new_brain
            newGen.append(new_bird)
        
    agents=newGen
    savedAgents.clear()

    
    

    generation+=1

    

    #print(ho[0])

pygame.font.init()
font = pygame.font.SysFont(None,25)

def write(msg):
    screen_text = font.render(msg, True, (255, 255, 255))
    win.blit(screen_text,(10,10))

clock = pygame.time.Clock()

while True:



    deleteAllFoods() 

    if len(agents) == 0:
        doEvolution()

    if len(eaten) ==2:
        # addAFood()
        eaten.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    win.fill((0,0,0))

    write("Generation "+str(generation))

    
    for agent in agents:
        agent.drawAgent()
        
        if len(foods) > 0:
            agent.search_food()
            
    for food in foods:
        food.draw()
    

    
    pygame.display.flip()
    #clock.tick(60)
pygame.quit()