import pygame
import numpy as np
import math
import random
import sys
import bird_brain as brain
import os
import neat



WIDTH=900
HEIGHT=600

accelerate_by=0.001
jumping=False
pipe_gap=180
pipe_velocity=20
pipes=[]

bird_images=[pygame.transform.scale(pygame.image.load("./sprites/upflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/midflap.png"),(25,25)),pygame.transform.scale(pygame.image.load("./sprites/downflap.png"),(25,25))]
flap=0

pipe_image=pygame.image.load("./sprites/pipe.png")
bg = pygame.image.load("./sprites/space.jpg")
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))


class Bird:
    def __init__(self):
        self.x=100
        self.y=HEIGHT/2
        self.velocity=0.05
        self.acceleration=0.001
        self.resistance=0.00001
        self.fitness=0
        self.size=25
        self.lift=-0.4
        self.image=pygame.transform.scale(pygame.image.load("./sprites/midflap.png"),(25,25))
        self.alive=True
        self.betweenPipes=False
        self.brain=brain.Brain(4,2,1)
        self.height = self.y
        self.tick_count=0
        self.score=0
    def drawBird(self,win):
        # pygame.draw.circle(win, (255,255,255), (self.x,self.y), self.size)
        # self.insidePipes()

        # global flap
        # if flap >= len(bird_images):
        #     flap=0
        # else:
        #     win.blit(bird_images[flap],(self.x,self.y))
        #     self.insidePipes()
        #     flap+=1

        win.blit(self.image,(self.x,self.y))
        self.insidePipes()

        if self.x-self.size/2 > pipes[0].x+pipes[0].width/2:
            print("Rewared")
            self.fitness+=10
        
        if self.betweenPipes:
            self.fitness+=10
    
    
    def applyGravity(self):

        if self.y > HEIGHT-self.size:
            self.velocity=0
            self.alive=False
        elif self.y <= 0:
            self.alive=False
        else:
            acceleration_due_to_gravity=self.acceleration
            self.velocity+=acceleration_due_to_gravity
            self.velocity+=self.resistance
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
    
    def drawLine(self,x1,y1,x2,y2,win):
        pygame.draw.line(win, (255,255,255), (x1, y1), (x2, y2),1)
            
    
    def insidePipes(self):
        if len(pipes) > 1:
            position_pipe_front=pipes[0].x-pipes[0].width/2
            position_pipe_back=pipes[0].x+pipes[0].width/2
            if self.x+self.size > position_pipe_front and self.x-self.size <position_pipe_back and self.y > pipes[0].height and self.y < pipes[0].height+pipe_gap:
                self.betweenPipes=True
            else:
                self.betweenPipes=False

def drawPipe(image,width,height):
    p=pygame.transform.scale(image,(width,height))
    return p

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


def addPipes():
    if len(pipes) > 0:
        first_pipe_height=pipes[0].height
        remaining_space=HEIGHT-first_pipe_height
        pipe_height=remaining_space-pipe_gap
        pipes.append(Pipe(HEIGHT-pipe_height,pipe_height))
    else:
        pipes.append(Pipe(0,random.randint(100,400)))


def eval_genomes(genomes, config):
    global pipe_velocity

    pygame.init()
    win=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("AI playing flappy bird")

    nets=[]
    birds=[]
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        pipes.clear()
        birds.append(Bird())
        ge.append(genome)
    run = True
    clock = pygame.time.Clock()
    while run and len(birds) > 0:
        clock.tick(30)
    
        if len(pipes) < 2:
            addPipes()
            for bird in birds:
                bird.fitness+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        win.fill((0,0,0))

        win.blit(bg,(0,0))
        
        for idx,bird in enumerate(birds):
            if bird.alive:
                bird.drawBird(win)
                bird.collition()
                # bird.applyGravity()
                #bird.drawLine(bird.x,bird.y,pipes[0].image.get_rect().bottom,pipes[0].image.get_rect().bottom,win)
                bird.move()
                if len(pipes) > 0:
                    output = nets[idx].activate((bird.x+bird.size/2,bird.y-bird.size/2,HEIGHT-bird.y,pipes[0].height,pipes[0].height+pipe_gap,pipes[0].x,bird.velocity,))
                    ge[idx].fitness += 0.1
                    if output[0] > 0.5:
                        bird.jump()
                
                if bird.betweenPipes:
                    ge[idx].fitness += 9
                if bird.x-bird.size/2 > pipes[0].x+pipes[0].width/2:
                    ge[idx].fitness += 9
                    bird.score+=1
                
            else:
                birds.pop(idx)
                nets.pop(idx)
                ge.pop(idx)

        for pipe in pipes:
            pipe.draw(win)
            pipe.move()

        pygame.display.flip()


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


