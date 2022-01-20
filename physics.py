import pygame
import math
import numpy as np
import random
import sys

vec=pygame.math.Vector2

WIDTH=900
HEIGHT=600

win=pygame.display.set_mode((WIDTH,HEIGHT))

pygame.init()

FPS=30

class Ball:
    def __init__(self):
        self.mass=100
        self.velocity=vec(0,0)
        self.acceleration=vec(0,0.07)
        self.opposite_force=vec()
        self.position=vec(WIDTH/2,HEIGHT/2)
        self.radius=20
    
    def drawCircle(self):
        pygame.draw.circle(win, (255,255,255), (self.position.x,self.position.y), self.radius,2)
    
    def gravity(self):
        self.velocity+=self.acceleration
    
    def move(self):
        self.gravity()
        self.position+=self.velocity

        distance_from_ground=math.sqrt((self.position.x-WIDTH/2)**2+(self.position.y+self.radius-HEIGHT)**2)
        if distance_from_ground < 1:
            force=self.mass*-self.acceleration.y
            self.acceleration=vec(0,0)
            self.velocity=vec(0,0)
            self.velocity.y+=force
        elif distance_from_ground > 300:
            self.velocity=vec(0,0)
            self.acceleration=vec(0,0.1)
            self.velocity+=self.acceleration
            self.position+=self.velocity
            # self.velocity=vec(0,0)
            # self.velocity.y+=10



ball=Ball()
clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    win.fill((0,0,0))
    ball.drawCircle()
    ball.move()
    pygame.display.flip()

pygame.quit()
