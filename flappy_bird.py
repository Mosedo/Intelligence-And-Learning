import pygame
import numpy as np
import math
import random
import sys
import bird_brain as brain

pygame.init()

WIDTH=900
HEIGHT=600

accelerate_by=0.001
jumping=False
pipe_gap=120
pipe_velocity=0.4
pipes=[]
birds=[]
deadbirds=[]
win=pygame.display.set_mode((WIDTH,HEIGHT))

class Bird:
    def __init__(self,index):
        self.x=100
        self.y=HEIGHT/2
        self.velocity=0.1
        self.acceleration=random.uniform(0.001,0.0015)
        self.fitness=0
        self.size=15
        self.lift=-0.4
        self.alive=True
        self.betweenPipes=False
        self.index=index
        self.brain=brain.Brain(4,2,1)
    def drawBird(self):
        pygame.draw.circle(win, (255,255,255), (self.x,self.y), self.size)
        self.insidePipes()
        inputs=[self.x/WIDTH,self.y/HEIGHT,pipes[0].height/HEIGHT,pipes[0].height+pipe_gap/HEIGHT]
        toJump=self.brain.feedFoward(inputs)[0][0][0]
        if toJump >= 0.5:
            self.jump()
    
    
    def applyGravity(self):

        if self.y > HEIGHT-self.size:
            self.velocity=0
            temp_idx=self.index
            del birds[self.index]
            reorganizeList(temp_idx)
        elif self.y <= 0:
            temp_idx=self.index
            del birds[self.index]
            reorganizeList(temp_idx)
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
        self.velocity+=self.lift
            
    
    def insidePipes(self):
        if len(pipes) > 1:
            position_pipe_front=pipes[0].x-pipes[0].width/2
            position_pipe_back=pipes[0].x+pipes[0].width/2
            if self.x+self.size > position_pipe_front and self.x-self.size <position_pipe_back and self.y > pipes[0].height and self.y < pipes[0].height+pipe_gap:
                self.betweenPipes=True
            else:
                self.betweenPipes=False

def createBirds():
    for b in range(10):
        birds.append(Bird(b))

createBirds()

class Pipe:
    def __init__(self,y,height):
        self.x=WIDTH-100
        self.y=y
        self.height=height
        self.width=60
    def draw(self):
        pygame.draw.rect(win, (255,255,255), pygame.Rect(self.x, self.y, self.width, self.height))
    def move(self):
        self.x-=pipe_velocity
        if self.x <= 0:
            pipes.clear()


def addPipes():
    if len(pipes) > 0:
        first_pipe_height=pipes[0].height
        remaining_space=HEIGHT-first_pipe_height
        pipe_height=remaining_space-pipe_gap
        pipes.append(Pipe(HEIGHT-pipe_height,pipe_height))
    else:
        pipes.append(Pipe(0,random.randint(100,400)))


def reorganizeList(index):
    for bird in birds:
        if bird.index > index:
            bird.index-=1

    



while True:

    if len(pipes) < 2:
        addPipes()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(birds) > 0:
                    bird.jump()
    win.fill((0,0,0))
    
    for bird in birds:
        if bird.alive:
            bird.drawBird()
            bird.collition()
            bird.applyGravity()
        else:
            temp_index=bird.index
            deadbirds.append(bird)
            del birds[bird.index]
            reorganizeList(temp_index)
            if len(birds) == 0:
                createBirds()

    for pipe in pipes:
        pipe.draw()
        pipe.move()

    pygame.display.flip()
pygame.quit()