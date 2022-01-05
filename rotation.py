import pygame
import random
import math
import sys
import numpy as np
from pygame import mixer
import mybrain as brain
from numpy.random import randint
from numpy.random import rand
import time

vec = pygame.math.Vector2

HEIGHT=800
WIDTH=1500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 1.6
MAX_FORCE = 0.1
APPROACH_RADIUS = 120

targets_no=10

gunning_point=200


pygame.init()

win=pygame.display.set_mode((WIDTH,HEIGHT))

missile=pygame.image.load("./sprites/missile.png")
jet=pygame.image.load("./sprites/jet.png")
turret=pygame.image.load("./sprites/turret.png")

gunner=pygame.image.load("./sprites/gunner.png")

bullet=pygame.image.load("./sprites/missile.png")

missiles_list=[]
jets=[]
targets=[]

savedJets=[]

missiles_jets=[]

gunner_targets=[""]

fired_bullets=False

bullet_sound=mixer.Sound('./sprites/firing.wav')
missile_sound=mixer.Sound('./sprites/launch.mp3')
explode_sound=mixer.Sound('./sprites/explode.wav')

bg = pygame.image.load("./sprites/warbg.jpg")
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))


explotions=[]
        


def reorganizeList(index):
    for miss in missiles_list:
        if miss.ind > index:
            miss.ind-=1

def reorganizeJets(index):
    for jts in jets:
        if jts.index > index:
            jts.index-=1





class Turret:
    def __init__(self):
        self.turret_height=70
        self.turret_width=80
        self.turret=pygame.transform.scale(turret,(self.turret_width,self.turret_height))
        self.position=vec(WIDTH/2-6,HEIGHT-self.turret_height-3)
        self.angle=0
    
    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,self.angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    def draw(self):
        win.blit(self.turret,(self.position.x,self.position.y))


class Missile:
    def __init__(self,i):
        self.ind=i
        self.missile_height=40
        self.missile_width=12
        self.position=vec(WIDTH/2,HEIGHT-self.missile_height+20)
        self.missile_image=pygame.transform.scale(missile,(self.missile_width,self.missile_height))
        self.missile=self.missile_image
        self.center=vec(self.position.x,self.position.y)
        self.missile_tip=vec(self.position.x,self.center[1]-self.missile_height/2)
        self.initial_angle=90
        self.angle=0
        self.vel=vec(0,0)
        self.rotation_vel = 10
        self.acceleration=vec(0,0)
        self.targets=[]
        self.life=100
        self.deleted=False
        self.destroyed=False
        self.launch=False

    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,self.angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    
    def draw(self):

        global jets

        if self.life <= 0:
            self.deleted=True


        for jet in jets:
            if jet.index == self.ind:
                self.targets.append(jet)


        
        if len(self.targets) > 0:
            self.seek_target(self.targets[0].position)


            # if abs(self.targets[0].position.x - self.position.x) and abs(self.targets[0].position.y - self.position.y) <= 1.5:
            #     self.targets[0].life-=100

        
        if self.life <= 0:
            tmp=self.ind
            try:
                missiles_list.pop(self.ind)
                self.targets[0].fitness+=200
                reorganizeList(tmp)
            except IndexError:
                #print(self.ind)
                reorganizeList(tmp)


        #update the missile tip position
        self.center=vec(self.position.x,self.position.y)
        self.missile_tip=vec(self.position.x,self.center[1]-self.missile_height/2)
        #draw the missile
        rotated_surface,rotated_rect=self.rotated(self.missile,self.angle)
        win.blit(rotated_surface,rotated_rect)

        try:
            distance=math.sqrt((self.position.x-self.targets[0].position.x)**2+(self.position.y-self.targets[0].position.y)**2)
            self.targets[0].fitness+=distance/100

            if distance <= 15:
                self.targets[0].life-=100
                #self.targets[0].fitness-=5
        except IndexError:
            pass


    
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
    
    def seek_target(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.turn(target)
        self.position += self.vel
    
    def reorganizeTargets(self,index):
        for tgts in self.targets:
            if tgts.index > index:
                tgts.index-=1
class Jet:
    def __init__(self,index):
        self.index=index
        self.jet_height=30
        self.jet_width=25
        self.position=vec(random.randint(10,WIDTH-self.jet_width),random.randint(10,HEIGHT/2-self.jet_height))
        self.jet_image=pygame.transform.scale(pygame.image.load("./sprites/jet.png"),(self.jet_width,self.jet_height))
        self.jet=self.jet_image
        self.center=vec(self.position.x,self.position.y)
        self.jet_tip=vec(self.position.x,self.center[1]-self.jet_height/2)
        self.initial_angle=90
        self.angle=0
        self.vel=vec(0,0)
        self.rotation_vel = 1.5
        self.MAX_SPEED=1.5
        self.MAX_FORCE=10
        self.acceleration=vec(0,0)
        self.destroyed=False
        self.life=100
        self.brain=brain.Brain(8,5,1)
        self.inrange=False
        self.was_in_range=False
        self.gunner_index=0
        self.in_persuit=vec()
        self.fitness=0
        self.destinations=[vec(random.randint(0,WIDTH-self.jet_width),random.randint(0,(HEIGHT/2)))]
        #self.destinations=[]
    
    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    
    def clamp(self,n, minn, maxn):
        return max(min(maxn, n), minn)
    
    def draw(self):

        if self.position.y > t.position.y - gunning_point:
            self.fitness-=2
        else:
            self.fitness+=0.005

        
        if self.inrange == False and self.was_in_range == True:
            gunner_targets.pop(self.gunner_index)
            self.was_in_range=False
            self.gunner_index=0
        
        if self.was_in_range and self.position.y < HEIGHT/2+gunning_point:
             self.was_in_range=False
             self.inrange=False
             gunner_targets.clear()
             gunner_targets.append("")
             self.fitness-=1


    
        tmp=self.index
        if self.life <= 0:
            coords=self.position
            try:
                savedJets.append(jets[tmp])
                removeJet=jets.pop(self.index)
                missiles_list.pop(self.index)
                #explotions.append(Explotion(coords,len(explotions)-1))
                explode_sound.play()
                reorganizeJets(tmp)
            except IndexError:
                pass

        #update the missile tip position
        self.center=vec(self.position.x,self.position.y)
        self.jet_tip=vec(self.position.x,self.center[1]-self.jet_height/2)

        #move jet
        self.seek_destination(self.destinations[0])

        #draw the missile
        rotated_surface,rotated_rect=self.rotated(self.jet,self.angle)
        win.blit(rotated_surface,rotated_rect)

        if abs(self.position.x-self.destinations[0].x) <=5:

            self.destinations[0]=vec(random.randint(20,WIDTH),random.randint(20,HEIGHT))

            # randomx=random.randint(10,WIDTH)
            # randomy=random.randint(10,HEIGHT)

            # prediction=self.brain.feedFoward([self.life/100,t.position.y-gunning_point/HEIGHT,randomx/WIDTH,randomy/HEIGHT,self.position.x/WIDTH,self.position.y/HEIGHT,self.in_persuit.x/WIDTH,self.in_persuit.y/HEIGHT])
            
            
            # if prediction[0] > 0.5:
            #     self.destinations[0]=vec(randomx,randomy)


        
            # prediction=self.brain.feedFoward([self.life/100,t.position.y-gunning_point/HEIGHT,self.position.x/WIDTH,self.position.y/HEIGHT,self.in_persuit.x/WIDTH,self.in_persuit.y/HEIGHT])
            
            
            # newx=self.clamp(prediction[0]*WIDTH,self.jet_width+10,WIDTH-(self.jet_width+10))
            # newy=self.clamp(prediction[1]*HEIGHT,self.jet_height+10,HEIGHT-(self.jet_height+10))

            # self.destinations[0]=vec(newx,newy)
    
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
    
    def seek_with_approach(self, target):
        self.desired = (target - self.position)
        dist = self.desired.length()
        try:
            self.desired.normalize_ip()
        except ValueError:
            pass
        if dist < APPROACH_RADIUS/1000:
            self.desired *= dist / APPROACH_RADIUS * self.MAX_SPEED
        else:
            self.desired *= self.MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > self.MAX_FORCE:
            steer.scale_to_length(self.MAX_FORCE)
        
        return steer
    
    def seek_destination(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > self.MAX_SPEED:
            self.vel.scale_to_length(self.MAX_SPEED)
        self.turn(target)
        self.position += self.vel

t=Turret()

class Gunner:
    def __init__(self):
        self.gunner_height=50
        self.gunner_width=20
        self.position=vec(t.position.x+60,t.position.y+20)
        self.gunner_image=pygame.transform.scale(gunner,(self.gunner_width,self.gunner_height))
        self.gunner=self.gunner_image
        self.center=vec(self.position.x,self.position.y)
        self.gunner_tip=vec(self.position.x,self.center[1]-self.gunner_height/2)
        self.initial_angle=90
        self.angle=0
        self.vel=vec(0,0)
        self.rotation_vel = 10
        self.MAX_SPEED=1.5
        self.MAX_FORCE=10
        self.acceleration=vec(0,0)
        self.shooting=False
        self.bullets=[Bullet(g) for g in range(100)]
    
    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    
    def reorganizeBullets(self,index):
        for bs in self.bullets:
            if bs.index > index:
                bs.index-=1
    
    def draw(self):

        if len(self.bullets) > 0:
            bullet_sound.fadeout(2000)
            for b in self.bullets:
                if b.life <= 0:
                    tmp=b.index
                    self.bullets.pop(b.index)
                    self.reorganizeBullets(tmp)
                    
                else:
                    b.draw()
        elif len(self.bullets) <= 0 and len(jets) > 0:
            bullet_sound.stop()
            self.bullets=[Bullet(g) for g in range(100)]

        if len(gunner_targets) > 0:
            try:
                self.turn(gunner_targets[0].position)
                self.gun_down(gunner_targets[0])
            except AttributeError:
                pass
        else:
            bullet_sound.stop()
            self.angle=0


        #update the missile tip position
        self.center=vec(self.position.x,self.position.y)
        self.jet_tip=vec(self.position.x,self.center[1]-self.gunner_height/2)

        #move jet
        #self.seek_targets(self.destinations[0])

        #draw the missile
        rotated_surface,rotated_rect=self.rotated(self.gunner,self.angle)
        win.blit(rotated_surface,rotated_rect)


    
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
    
    def gun_down(self,target):
        global fired_bullets
        self.shooting=True

        # if self.shooting:
        if len(self.bullets) > 0:
            bullet_sound.play()
        
        for idx,b in enumerate(self.bullets):
            b.move(target.position)
            distance=math.sqrt((self.bullets[-1].position.x-target.position.x)**2+(self.bullets[-1].position.y-target.position.y)**2)
            if distance < 2:
                target.life-=30
                target.fitness-=1
                self.bullets.clear()
        
        if target.life <= 0:
            gunner_targets.pop(0)
            gunner_targets.append("")

class Bullet:
    def __init__(self,index):
        self.index=index
        self.bullet_height=17
        self.bullet_width=5
        self.position=vec(t.position.x+60,t.position.y+20)
        self.bullet_image=pygame.transform.scale(bullet,(self.bullet_width,self.bullet_height))
        self.bullet=self.bullet_image
        self.center=vec(self.position.x,self.position.y)
        self.gunner_tip=vec(self.position.x,self.center[1]-self.bullet_height/2)
        self.initial_angle=90
        self.angle=0
        self.vel=vec(0,0)
        self.rotation_vel = 1.5
        self.MAX_SPEED=np.random.uniform(0.5,5.5)
        self.MAX_FORCE=10
        self.acceleration=vec(0,0)
        self.life=100
    
    def rotated(self,surface,angle):
        rotated_surface=pygame.transform.rotozoom(surface,angle,1)
        rotated_rect=rotated_surface.get_rect(center=(self.position.x,self.position.y))
        return rotated_surface,rotated_rect
    
    def draw(self):

        self.life-=0.8

        #update the missile tip position
        self.center=vec(self.position.x,self.position.y)
        self.jet_tip=vec(self.position.x,self.center[1]-self.bullet_height/2)

        #move jet
        #self.seek_targets(self.destinations[0])

        #draw the missile
        rotated_surface,rotated_rect=self.rotated(self.bullet,self.angle)
        win.blit(rotated_surface,rotated_rect)

    def move(self,target):
        self.seek_target(target)

    def seek_with_approach(self, target):
        self.desired = (target - self.position)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS/1000:
            self.desired *= dist / APPROACH_RADIUS * self.MAX_SPEED
        else:
            self.desired *= self.MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > self.MAX_FORCE:
            steer.scale_to_length(self.MAX_FORCE)
        
        return steer
    
    def seek_target(self,target):
        self.acceleration = self.seek_with_approach(target)
        self.vel += self.acceleration
        if self.vel.length() > self.MAX_SPEED:
            self.vel.scale_to_length(self.MAX_SPEED)
        self.turn(target)
        self.position += self.vel
        


    
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

class Explotion:
    def __init__(self,position,index):
        self.position=position
        self.index=index
        self.timer=0
        self.explotions=[pygame.image.load('./sprites/exp3.png'),pygame.image.load('./sprites/exp2.png'),pygame.image.load('./sprites/exp5.png')]
        self.image_index=0
    
    def reorganizeExp(self,index):
        for exp in explotions:
            if exp.index > index:
                exp.index-=1
    
    def drawExplotion(self):
        # if self.timer < 10:
        #     win.blit(pygame.image.load('./sprites/exp3.png'),(self.position.x,self.position.y))
        #     self.timer+=0.5
        if self.timer < 10:
            for explotion in self.explotions:
                win.blit(self.explotions[self.image_index],(self.position.x,self.position.y))
                self.timer+=0.01
                if self.image_index < len(self.explotions)-1 and self.timer > 5:
                    self.image_index+=1
        else:
            tmp=self.index
            explotions.pop(self.index)
            self.reorganizeExp(tmp)

        




gunner=Gunner()

missiles_list=[Missile(l) for l in range(targets_no)]

jets=[Jet(j) for j in range(targets_no)]

remaining_jets=len(jets)

launch=True

if launch:
    missile_sound.play()
    launch=False

mutation_rate=0.1
crossover_rate=0.5

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
    global jets
    global savedJets
    rankedJets=[]
    for savedbird in savedJets:
        rankedJets.append((savedbird.fitness,savedbird.brain))
    sort_by=lambda ranked:ranked[0]
    rankedJets.sort(key=sort_by,reverse=True)
    pool=rankedJets[:4]

    parents=[pool[0][1],pool[random.randint(1,len(pool)-1)][1]]
    #parents=[pool[0][1],pool[1][1]]


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
    parent1=brain.Brain(8,5,1)
    parent1.wh=new_parent1_wh
    parent1.wout=new_parent1_wout
    parent1.bh=np.array(mutation(mutation_rate,parents[0].bh.flatten().tolist())).reshape(savedJets[0].brain.bh.shape)

    parent1.bout=np.array(mutation(mutation_rate,parents[0].bout.flatten().tolist())).reshape(savedJets[0].brain.bout.shape)

    parent2=brain.Brain(8,5,1)
    parent2.wh=new_parent2_wh
    parent2.wout=new_parent2_wout
    parent2.bh=np.array(mutation(mutation_rate,parents[1].bh.flatten().tolist())).reshape(savedJets[0].brain.bh.shape)
    parent2.bout=np.array(mutation(mutation_rate,parents[1].bout.flatten().tolist())).reshape(savedJets[0].brain.bout.shape)

    #create new population
    newGen=[]

    for p in range(10):
        if p < 5:
            new_brain=brain.Brain(8,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent1.wh.flatten().tolist())).reshape(savedJets[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent1.wout.flatten().tolist())).reshape(savedJets[0].brain.wout.shape)
            new_jet=Jet(p)
            new_jet.brain=new_brain
            newGen.append(new_jet)
        else:
            new_brain=brain.Brain(8,5,1)
            new_brain.wh=np.array(mutation(mutation_rate,parent2.wh.flatten().tolist())).reshape(savedJets[0].brain.wh.shape)
            new_brain.wout=np.array(mutation(mutation_rate,parent2.wout.flatten().tolist())).reshape(savedJets[0].brain.wout.shape)
            new_jet=Jet(p)
            new_jet.brain=new_brain
            newGen.append(new_jet)
        
    jets=newGen
    savedJets.clear()

    remaining_jets=10

    addMoreMissiles()


def addMoreMissiles():
    for m in range(targets_no):
        missiles_list.append(Missile(m))
    # missiles_jets=list(zip(missiles_list,jets))


clock = pygame.time.Clock()

while True:


    if len(jets) == 0:
        jets=[Jet(j) for j in range(targets_no)]
        #neuroEvolution()

    remaining_jets=len(jets)


    if len(missiles_list) <= 0:
        for n in range(remaining_jets):
            missile_sound.play()
            missiles_list.append(Missile(n))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
                
    win.fill((0,0,0))

    #win.blit(bg,(0,0))

    for exp in explotions:
        exp.drawExplotion()

    missiles_jets=list(zip(missiles_list,jets))

    for miss_jets in missiles_jets:
        miss_jets[1].draw()
        miss_jets[1].in_persuit=miss_jets[0].position
        miss_jets[0].draw()
        #miss_jets[0].targets.append(miss_jets[1])
        miss_jets[0].life-=np.random.uniform(0.03,0.1)
        miss_jets[0].launch=True
    
    for g_index,jet in enumerate(jets):
        pygame.draw.line(win, (255,255,255), (0, t.position.y-gunning_point), (WIDTH, t.position.y-gunning_point),2)

        if jet.position.y > t.position.y-gunning_point:
            jet.inrange=True
            gunner_targets[0]=jet
            jet.was_in_range=True
            jet.gunner_index=g_index
            gunner.shooting=True
    
    for idx,msls in enumerate(missiles_list):
        if missiles_list[idx].deleted==True:
            missiles_list.pop(idx)
    



    gunner.draw()
    t.draw()

    pygame.display.flip()
pygame.quit()