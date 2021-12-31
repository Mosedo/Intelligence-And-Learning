import numpy as np
import random
import math
import pygame
vec = pygame.math.Vector2

HEIGHT=600
WIDTH=900

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

pygame.init()

win=pygame.display.set_mode((WIDTH,HEIGHT))

agents=[]

cities=[
    {
        "name":"N",
        "coords":(50,50),
        "color":(255,255,0),
        "connections":[1,4],
        "connected":[],
        "index":0
    },
    {
        "name":"K",
        "coords":(700,100),
        "color":(0,255,0),
        "connections":[0,2],
        "connected":[],
        "index":1
    },
    {
        "name":"E",
        "coords":(300,250),
        "color":(0,255,255),
        "connections":[1,3],
        "connected":[],
        "index":2
    },
    {
        "name":"G",
        "coords":(600,400),
        "color":(255,255,255),
        "connections":[2,4],
        "connected":[],
        "index":3
    },
    {
        "name":"M",
        "coords":(100,500),
        "color":(0,255,0),
        "connections":[0,3],
        "connected":[],
        "index":4
    }
]

def drawCircle(color,x,y):
    pygame.draw.circle(win, color, (x,y), 30)

def drawLine(x1,y1,x2,y2):
    pygame.draw.line(win, (255,255,255), (x1, y1), (x2, y2),20)



class Agent:
    def __init__(self):
        self.position=vec(cities[4]["coords"][0],cities[4]["coords"][1])
        self.velocity=vec(0,0)
        self.acceleration=vec(0,0)
        self.dest=[vec(600,400),vec(300,250),vec(700,100)]
        self.fitness=0
    def drawAgent(self):
        pygame.draw.circle(win, (255,0,0), (self.position.x,self.position.y), 15)
    
    
    def seek(self, target):
        self.desired = (target - self.position).normalize() * MAX_SPEED
        steer = (self.desired - self.velocity)
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
        steer = (self.desired - self.velocity)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        
        return steer
    def move(self):
        if len(self.dest) > 0:
            target=self.dest[0]
            self.acceleration = self.seek_with_approach(target)
            self.velocity += self.acceleration
            if self.velocity.length() > MAX_SPEED:
                self.velocity.scale_to_length(MAX_SPEED)
            self.position += self.velocity

            if abs(self.position.x - target.x) < 2:
                self.dest.pop(0)
        else:
            self.fitness+=1

agents.append(Agent())

def main():
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
        win.fill((0,0,0))
        for city in cities:
            drawCircle(city["color"],city["coords"][0],city["coords"][1])
            for connection in city["connections"]:
                drawLine(city["coords"][0],city["coords"][1],cities[connection]["coords"][0],cities[connection]["coords"][1])
        for agent in agents:
            agent.drawAgent()
            agent.move()
        pygame.display.flip()


if __name__ == '__main__':
    main()