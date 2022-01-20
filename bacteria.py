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
import string
from population import convertToSentense
import vehicle_brain as brain


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
MAX_SPEED = 4
MAX_FORCE = 0.1
APPROACH_RADIUS = 120

population_size=4


pygame.init()

win=pygame.display.set_mode((WIDTH,HEIGHT))

pygame.font.init()
font = pygame.font.SysFont(None,25)

def write(msg,x,y):
    screen_text = font.render(msg, True, (255, 255, 255))
    win.blit(screen_text,(x,y))

generation=0

mutation_rate=0.01
crossover_rate=0.99


foods=[]
agents=[]
savedAgents=[]

food_count=0
poison_count=0



def reorganizeList(self,index):
    for bs in self.bullets:
        if bs.index > index:
            bs.index-=1


class Agent:
    def __init__(self):
        self.agent_width=10
        self.agent_height=15
        self.position=vec(random.randint(10,WIDTH),random.randint(10,HEIGHT))
        self.angle=90
        self.vel=vec(0,0)
        self.rotation_vel = 1.5
        self.MAX_SPEED=1.5
        self.MAX_FORCE=10
        self.acceleration=vec(0,0)
        self.image=pygame.image.load('./sprites/triangle.png')
        self.vehicle=pygame.transform.scale(self.image,(self.agent_width,self.agent_height))
        self.surface=pygame.Surface([self.agent_width,self.agent_height])
        self.color=(0,255,0)
        self.radar_color=(0,255,0)
        self.points = [[100, 100],  [100, 150], [180, 125]]
        self.search_radius=200
        self.life=100
        self.fitness=0
        self.targets=[]
        self.random_locations=[vec(random.randint(self.agent_width,WIDTH),random.randint(self.agent_height,HEIGHT))]
        self.brain=brain.Brain(3,4,1)
        self.removed=False
        self.distance=[]
    
    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    
    def pointer(self):
        if len(self.targets) > 0:
            if self.targets[0].code < 0.5:
                pygame.draw.line(win, (255,0,0), (self.position.x,self.position.y), (self.targets[0].position.x, self.targets[0].position.y),2)
            else:
                pygame.draw.line(win, (0,255,0), (self.position.x,self.position.y), (self.targets[0].position.x, self.targets[0].position.y),2)
    

    def drawAgent(self):

        #self.surface.fill((29, 31, 30))

        self.life-=0.05
        
        pygame.draw.polygon(surface=self.surface, color=self.color, points=[(self.surface.get_rect().bottomleft[0],self.surface.get_rect().bottomleft[1]), (self.surface.get_rect().topright[0]-self.agent_width/2,0), (self.surface.get_rect().bottomright[0],self.surface.get_rect().bottomright[1])])
        rotated_surface,rotated_rect=self.rotated(self.surface,self.angle)
        win.blit(rotated_surface,rotated_rect)
        #self.pointer()
        #self.radar()
        self.findTargetFoods()
        self.removeEaten()
        self.checkCollition()
        self.colorLabelling()

    def colorLabelling(self):
        if self.life == 100:
            self.color=(0,255,0)
        elif self.life <= 75 and self.life >= 50:
            self.color=(255,165,0)
        elif self.life <= 50 and self.life >=25:
            self.color=(255,255,0)
        elif self.life <= 25 and self.life >=0:
            self.color=(255,0,0)
        elif self.life <= 0:
            self.removed=True
    
    def move(self):
        #print(self.life)
        if len(self.targets) > 0:

            if self.targets[0].code < 0.5:
                self.radar_color=(255,0,0)
            else:
                self.radar_color=(0,255,0)

            #self.seek(self.targets[0].position)

            #start here
            prediction=self.brain.feedFoward([self.distance[0],self.targets[0].code,self.life/100])


            if prediction[0] >= 0.5:

                self.seek(self.targets[0].position)

                
            else:
                self.targets.append(foods[random.randint(0,len(foods)-1)])
                self.targets.pop(0)
                

            #end here

 
        elif len(self.targets) < 1:
            self.seek(self.random_locations[0])

    def checkCollition(self):
        global food_count
        global poison_count
        if len(self.targets) > 0:
            distance=math.sqrt((self.targets[0].position.x - self.position.x)**2+(self.targets[0].position.y - self.position.y)**2)
            if distance <= self.agent_width/2:

                if self.targets[0].code >= 0.5:
                    #self.fitness+=500
                    self.fitness+=(1/self.distance[0])
                    if self.life < 100:
                        self.life+=40
                else:
                    self.life-=1000
                    self.fitness-=10
                    #self.fitness-=300


                if len(self.targets) > 1:
                    
                    srl=self.targets[0].serial_number
                    self.targets.pop(0)
                    for idx,food in enumerate(foods):
                        if food.serial_number==srl:
                            foods.pop(idx)

                elif len(self.targets) == 1:
                    srl=self.targets[0].serial_number
                    self.targets.pop(0)

                    for idx,food in enumerate(foods):
                        if food.serial_number==srl:
                            foods.pop(idx)
                    
        else:
            distance=math.sqrt((self.random_locations[0].x - self.position.x)**2+(self.random_locations[0].y - self.position.y)**2)
            if distance <= self.agent_width/2:
                self.random_locations[0]=vec(random.randint(10,WIDTH),random.randint(10,HEIGHT))
    
    def findTargetFoods(self):
        if len(self.targets) < 1:
            self.targets.append(foods[random.randint(0,len(foods)-1)])
            distance=math.sqrt((self.targets[0].position.x - self.position.x)**2+(self.targets[0].position.y - self.position.y)**2)
            self.distance.append(distance)
        #if len(foods) > 0:
            #for food in foods:
                # if ((food.position.x >= self.position.x and food.position.x <= self.position.x+self.search_radius) or (food.position.x <= self.position.x and food.position.x >= self.position.x-self.search_radius)) and ((food.position.y >= self.position.y and food.position.y <= self.position.y+self.search_radius) or (food.position.y <= self.position.y and food.position.y >= self.position.y-self.search_radius)):
                #     f_list=[]
                #     for f in self.targets:
                #         if f.serial_number== food.serial_number:
                #             f_list.append(food)
                #     if len(f_list) ==0:
                #         self.targets.append(food)
    def removeEaten(self):
        for idx,target in enumerate(self.targets):
            still_available=[]
            for food in foods:
                if food.serial_number == target.serial_number:
                    still_available.append(food)
                    break
            if len(still_available) < 1:
                self.targets.pop(idx)

    
    def turn(self,target):
        target_x, target_y = target.x,target.y
        x_diff = target_x - self.position.x
        y_diff = target_y - self.position.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.position.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
    
    def radar(self):
        pygame.draw.circle(win, self.radar_color, (self.position.x,self.position.y), self.search_radius,2)

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
    
    def seek(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.turn(target)
        self.position += self.vel

class Food:
    def __init__(self):
        self.position=vec(random.randint(10,WIDTH),random.randint(10,HEIGHT))
        self.code=np.random.uniform(0.5,1)
        self.color=(0,255,0)
        self.eaten=False
        self.size=3
        self.serial_number=self.generateSerialNumber()
        self.surface=pygame.Surface([self.size,self.size])
    def drawFood(self):
        # pygame.draw.circle(self.surface, self.color, (surface_x,surface_y), self.size)
        # win.blit(self.surface,(self.position.x,self.position.y))

        pygame.draw.circle(win, self.color, (self.position.x,self.position.y), self.size)
    
    def generateSerialNumber(self):
        serial=[random.choice(string.ascii_letters) for a in range(10)]
        return convertToSentense(serial)

class Poison:
    def __init__(self):
        self.position=vec(random.randint(10,WIDTH),random.randint(10,HEIGHT))
        self.code=np.random.uniform(0,0.49)
        self.color=(255,0,0)
        self.eaten=False
        self.size=3
        self.serial_number=self.generateSerialNumber()
        self.surface=pygame.Surface([self.size,self.size])
    def drawFood(self):
        # pygame.draw.circle(self.surface, self.color, (surface_x,surface_y), self.size)
        # win.blit(self.surface,(self.position.x,self.position.y))

        pygame.draw.circle(win, self.color, (self.position.x,self.position.y), self.size)
    
    def generateSerialNumber(self):
        serial=[random.choice(string.ascii_letters) for a in range(10)]
        return convertToSentense(serial)


def mutation(rate,chromosome):
    new_chromosome=chromosome.copy()
    for idx,letter in enumerate(chromosome):
        if np.random.uniform(0,1) < rate:
            new_chromosome[idx]=random.uniform(-7,1)
    return new_chromosome

def crossover(p1, p2, r_cross):

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

def neuroEvolution():
    global agents
    global savedAgents
    global generation
    rankedAgents=[]
    for savedagent in savedAgents:
        rankedAgents.append((savedagent.fitness,savedagent.brain))
    sort_by=lambda ranked:ranked[0]
    rankedAgents.sort(key=sort_by,reverse=True)
    pool=rankedAgents[:50]

    #parents=[pool[0][1],pool[random.randint(1,len(pool)-1)][1]]
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
    parent1=brain.Brain(3,4,1)
    parent1.wh=new_parent1_wh
    parent1.wout=new_parent1_wout
    parent1.bh=np.array(mutation(mutation_rate,parents[0].bh.flatten().tolist())).reshape(savedAgents[0].brain.bh.shape)

    parent1.bout=np.array(mutation(mutation_rate,parents[0].bout.flatten().tolist())).reshape(savedAgents[0].brain.bout.shape)

    parent2=brain.Brain(3,4,1)
    parent2.wh=new_parent2_wh
    parent2.wout=new_parent2_wout
    parent2.bh=np.array(mutation(mutation_rate,parents[1].bh.flatten().tolist())).reshape(savedAgents[0].brain.bh.shape)
    parent2.bout=np.array(mutation(mutation_rate,parents[1].bout.flatten().tolist())).reshape(savedAgents[0].brain.bout.shape)

    #create new population
    newGen=[]

    for p in range(population_size):
        if p < population_size/2:
            new_brain=brain.Brain(3,4,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent1.wh.flatten().tolist())).reshape(savedAgents[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent1.wout.flatten().tolist())).reshape(savedAgents[0].brain.wout.shape)
            new_agent=Agent()
            new_agent.brain=new_brain
            newGen.append(new_agent)
        else:
            new_brain=brain.Brain(3,4,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent2.wh.flatten().tolist())).reshape(savedAgents[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent2.wout.flatten().tolist())).reshape(savedAgents[0].brain.wout.shape)
            new_agent=Agent()
            new_agent.brain=new_brain
            newGen.append(new_agent)
        
    agents=newGen
    savedAgents.clear()
    generation+=1


for f in range(150):
    if f <=85:
        food_count+=1
        foods.append(Food())
    else:
        poison_count+=1
        foods.append(Poison())

for a in range(population_size):
    agents.append(Agent())

FPS=240

clock = pygame.time.Clock()

while True:

    clock.tick(FPS)

    if np.random.randint(0,1) > 0.95:
        foods.append(Food())



    if len(agents) == 0:
        neuroEvolution()

    
    if len(foods) < 30:
        for l in range(50):
            foods.append(Food())
            foods.append(Poison())
    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # win.fill((29, 31, 30))
    win.fill((0, 0, 0))

    for idx,agent in enumerate(agents):
        agent.drawAgent()
        agent.move()

        if agent.removed:
            new_food=Food()
            new_food.position=agent.position
            foods.append(new_food)
            food_count+=1
            poison_count+=1
            savedAgents.append(agent)
            agents.pop(idx)
        

    

    for food in foods:
        food.drawFood()

    pygame.display.flip()
pygame.quit()
