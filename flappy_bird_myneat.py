import pygame
import numpy as np
import math
import random
import sys
import genetic_brain as brain

pygame.init()

WIDTH=900
HEIGHT=600

accelerate_by=0.001
jumping=False
pipe_gap=120
pipe_velocity=10
pipes=[]
win=pygame.display.set_mode((WIDTH,HEIGHT))

bird_images=[pygame.transform.scale(pygame.image.load("./sprites/upflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/midflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/downflap.png"),(25,25))]
flap=0
FTS=30

birds=[]

class Bird:
    def __init__(self):
        self.x=200
        self.y=HEIGHT/2
        self.velocity=0.1
        self.acceleration=0.001
        self.fitness=0
        self.size=15
        self.lift=-0.4
        self.alive=True
        self.betweenPipes=False
        self.height = self.y
        self.brain=brain.Brain(7,4,1)
        self.tick_count=0
    def drawBird(self):
        global flap
        #pygame.draw.circle(win, (255,255,255), (self.x,self.y), self.size)
        if flap >= len(bird_images):
            flap=0
        else:
            win.blit(bird_images[flap],(self.x,self.y))
            self.insidePipes()
            flap+=1
    
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
        self.width=60
    def draw(self):
        pygame.draw.rect(win, (255,255,255), pygame.Rect(self.x, self.y, self.width, self.height))
    def move(self):
        self.x-=pipe_velocity
        if self.x <= 0:
            pipes.clear()

birds.append(Bird())

def addPipes():
    if len(pipes) > 0:
        first_pipe_height=pipes[0].height
        remaining_space=HEIGHT-first_pipe_height
        pipe_height=remaining_space-pipe_gap
        pipes.append(Pipe(HEIGHT-pipe_height,pipe_height))
    else:
        pipes.append(Pipe(0,random.randint(100,400)))
    

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
    for idx,bird in enumerate(birds):
        if bird.alive:
            bird.drawBird()
            bird.collition()
            bird.move()

            if bird.brain.feedFoward([bird.x+bird.size/2,bird.y-bird.size/2,HEIGHT-bird.y,pipes[0].height,pipes[0].height+pipe_gap,pipes[0].x,bird.velocity]) >= 0.5:
                bird.jump()

        else:
            birds.pop(idx)

    for pipe in pipes:
        pipe.draw()
        pipe.move()

    pygame.display.flip()
pygame.quit()