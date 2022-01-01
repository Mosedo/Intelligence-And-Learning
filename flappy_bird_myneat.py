import pygame
import numpy as np
import math
import random
import sys
import mybrain as brain
from numpy.random import randint
from numpy.random import rand

pygame.init()

WIDTH=900
HEIGHT=600

accelerate_by=0.001
jumping=False
pipe_gap=150
pipe_velocity=40
pipes=[]
win=pygame.display.set_mode((WIDTH,HEIGHT))

bird_images=[pygame.transform.scale(pygame.image.load("./sprites/upflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/midflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/downflap.png"),(25,25))]
flap=0
FTS=30

birds=[]
savedBirds=[]

mutation_rate=0.1
crossover_rate=0.95

pipe_image=pygame.image.load("./sprites/pipe.png")
bg = pygame.image.load("./sprites/space.jpg")
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))

class Bird:
    def __init__(self):
        self.x=100
        self.y=HEIGHT/2
        self.velocity=0.1
        self.acceleration=0.001
        self.fitness=0
        self.size=25
        self.lift=-0.4
        self.alive=True
        self.betweenPipes=False
        self.height = self.y
        self.brain=brain.Brain(7,4,1)
        self.tick_count=0
    def drawBird(self):
        #global flap
        #pygame.draw.circle(win, (255,255,255), (self.x,self.y), self.size)
        # if flap >= len(bird_images):
        #     flap=0
        # else:
        #     win.blit(bird_images[flap],(self.x,self.y))
        #     self.insidePipes()
        #     flap+=1
        win.blit(bird_images[1],(self.x,self.y))
        self.insidePipes()

        if self.x-self.size/2 > pipes[0].x+pipes[0].width/2:
            self.fitness+=10
        
        if self.betweenPipes:
            self.fitness+=5
    
    def applyGravity(self):

        if self.y > HEIGHT-self.size:
            self.velocity=0
        else:
            acceleration_due_to_gravity=self.acceleration
            self.velocity+=acceleration_due_to_gravity
            self.y+=self.velocity
        
    def collition(self):
        global pipes
        if len(pipes) > 1:
            if (self.x+self.size >= pipes[0].x-pipes[0].width/2 and self.y <= pipes[0].height) or (self.x+self.size >= pipes[1].x-pipes[1].width/2 and self.y >= pipes[0].height+pipe_gap):
                self.alive=False
            if (self.y-self.size <= pipes[0].height and self.betweenPipes) or (self.y+self.size >= pipes[0].height+pipe_gap and self.betweenPipes):
                self.alive=False
           
    def jump(self):
        #self.velocity+=self.lift
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):


        if self.y > HEIGHT-self.size:
            self.velocity=0
            self.alive=False
        elif self.y <= 0:
            self.alive=False

        self.tick_count += 1

        displacement = self.velocity*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement
    
    def insidePipes(self):
        if len(pipes) > 1:
            position_pipe_front=pipes[0].x-pipes[0].width/2
            position_pipe_back=pipes[0].x+pipes[0].width/2
            if self.x+self.size > position_pipe_front and self.x-self.size <position_pipe_back and self.y > pipes[0].height and self.y < pipes[0].height+pipe_gap:
                self.betweenPipes=True
            else:
                self.betweenPipes=False


class Pipe:
    def __init__(self,y,height):
        self.x=WIDTH-100
        self.y=y
        self.height=height
        self.width=50
        self.image=pipe_image
    def draw(self,win):
        win.blit(drawPipe(self.image,self.width,self.height),(self.x, self.y))
        #pygame.draw.rect(win, (255,255,255), pygame.Rect(self.x, self.y, self.width, self.height))
    def move(self):
        self.x-=pipe_velocity
        if self.x <= 0:
            pipes.clear()

for b in range(300):
    birds.append(Bird())
    
def addPipes():
    if len(pipes) > 0:
        first_pipe_height=pipes[0].height
        remaining_space=HEIGHT-first_pipe_height
        pipe_height=remaining_space-pipe_gap
        pipes.append(Pipe(HEIGHT-pipe_height,pipe_height))
    else:
        pipes.append(Pipe(0,random.randint(100,400)))

def drawPipe(image,width,height):
    p=pygame.transform.scale(image,(abs(width),abs(height)))
    return p


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

    # c1, c2 = p1.copy(), p2.copy()
    # if rand() < r_cross:
    #     pt = randint(1, len(p1)-2)
    #     c1 = p1[:pt] + p2[pt:]
    #     c2 = p2[:pt] + p1[pt:]
    # return [c1, c2]

def neuroEvolution():
    global birds
    global savedBirds
    rankedBirds=[]
    for savedbird in savedBirds:
        rankedBirds.append((savedbird.fitness,savedbird.brain))
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
    parent1=brain.Brain(7,4,1)
    parent1.wh=new_parent1_wh
    parent1.wout=new_parent1_wout
    parent1.bh=np.array(mutation(mutation_rate,parents[0].bh.flatten().tolist())).reshape(savedBirds[0].brain.bh.shape)

    parent1.bout=np.array(mutation(mutation_rate,parents[0].bout.flatten().tolist())).reshape(savedBirds[0].brain.bout.shape)

    parent2=brain.Brain(7,4,1)
    parent2.wh=new_parent2_wh
    parent2.wout=new_parent2_wout
    parent2.bh=np.array(mutation(mutation_rate,parents[1].bh.flatten().tolist())).reshape(savedBirds[0].brain.bh.shape)
    parent2.bout=np.array(mutation(mutation_rate,parents[1].bout.flatten().tolist())).reshape(savedBirds[0].brain.bout.shape)

    #create new population
    newGen=[]

    for p in range(300):
        if p < 150:
            new_brain=brain.Brain(7,4,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent1.wh.flatten().tolist())).reshape(savedBirds[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent1.wout.flatten().tolist())).reshape(savedBirds[0].brain.wout.shape)
            new_bird=Bird()
            new_bird.brain=new_brain
            newGen.append(new_bird)
        else:
            new_brain=brain.Brain(7,4,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent2.wh.flatten().tolist())).reshape(savedBirds[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent2.wout.flatten().tolist())).reshape(savedBirds[0].brain.wout.shape)
            new_bird=Bird()
            new_bird.brain=new_brain
            newGen.append(new_bird)
        
    birds=newGen
    savedBirds.clear()
    

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    if len(pipes) < 2:
        addPipes()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    win.fill((0,0,0))
    win.blit(bg,(0,0))
    for idx,bird in enumerate(birds):
        if bird.alive:
            bird.drawBird()
            bird.collition()
            bird.move()
            bird.fitness+=3
            # brain_input=[bird.velocity,bird.y/HEIGHT,pipes[0].height+pipe_gap/2,pipes[0].x,pipes[0].x-50]
            #brain_input=[bird.velocity,bird.y/HEIGHT,pipes[0].height+(HEIGHT-pipes[0].height),pipes[0].x,pipes[0].x]
            brain_input=[bird.x+bird.size/2,bird.y-bird.size/2,HEIGHT-bird.y,pipes[0].height,pipes[0].height+pipe_gap,pipes[0].x,bird.velocity,]
            brain_output=bird.brain.feedFoward(brain_input)
            if  brain_output[0] > 0.5:
                bird.jump()

        else:
            removeBird=birds.pop(idx)
            savedBirds.append(removeBird)

            if len(birds) < 1:
                # for b in range(100):
                #     birds.append(Bird())
                neuroEvolution()

    for pipe in pipes:
        pipe.draw(win)
        pipe.move()

    pygame.display.flip()
pygame.quit()