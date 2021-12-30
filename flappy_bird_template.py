import pygame
import numpy as np
import math
import random
import sys

pygame.init()

WIDTH=900
HEIGHT=600

accelerate_by=0.001
jumping=False
pipe_gap=120
pipe_velocity=0.5

win=pygame.display.set_mode((WIDTH,HEIGHT))

class Bird:
    def __init__(self):
        self.x=200
        self.y=HEIGHT/2
        self.velocity=0.1
        self.acceleration=0.001
        self.fitness=0
        self.size=15
        self.lift=-0.4
    def drawBird(self):
        pygame.draw.circle(win, (255,255,255), (self.x,self.y), self.size)
    
    def applyGravity(self):

        if self.y > HEIGHT-self.size:
            self.velocity=0
        else:
            acceleration_due_to_gravity=self.acceleration
            self.velocity+=acceleration_due_to_gravity
            self.y+=self.velocity
           
    def jump(self):
        self.velocity+=self.lift

pipes=[]

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

bird=Bird()

def addPipes():
    if len(pipes) > 0:
        first_pipe_height=pipes[0].height
        remaining_space=HEIGHT-first_pipe_height
        pipe_height=remaining_space-pipe_gap
        pipes.append(Pipe(HEIGHT-pipe_height,pipe_height))
    else:
        pipes.append(Pipe(0,random.randint(100,400)))



while True:
    if len(pipes) < 2:
        addPipes()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    win.fill((0,0,0))
    bird.drawBird()
    bird.applyGravity()

    for pipe in pipes:
        pipe.draw()
        pipe.move()

    pygame.display.flip()
pygame.quit()