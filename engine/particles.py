import pygame,random,os
from pygame.locals import *

def load_img(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0))
    return img

def blit_offset(display,image,pos,offset,centered=False):
    if centered:
        x = int(image.get_width()/2)
        y = int(image.get_height()/2)
    else:
        x = offset[0]
        y = offset[1]

    display.blit(image,(pos[0]-x,pos[1]-y))

def swap_color(surf,old_c,new_c):
    surf.set_colorkey(old_c)
    s = surf.copy()
    s.set_colorkey((0,0,0))
    s.fill(new_c)
    s.blit(surf,(0,0))
    return s

global particle_images
particle_images = {}

def load_particles(path):
    global particle_images
    img_names = os.listdir(path) #p,leaves or etc.
    for name in img_names:
        frame_names = os.listdir(path + '/' + name)
        images = []
        for name2 in frame_names:
            images.append(load_img(path + '/' + name + '/' + name2))
            #p_0,p_1
            particle_images[name] = images.copy()

class Particle:
    def __init__(self,x,y,motion,lifetime,type,gravity=False,custom_color=(255,255,255)):
        self.pos = [x,y]
        self.motion = motion
        self.lifetime = lifetime
        self.type = type
        self.grv = gravity
        self.clr = custom_color
        self.target_vel = [0,0]

        self.kill = False
        self.frame = 0

    def update(self,anim_speed,randomness=False):
        if not randomness:
            self.frame += anim_speed
        else:
            self.frame += random.random() * anim_speed
        if self.frame >= len(particle_images[self.type])-1:
            self.kill = True
        self.pos[0]+=self.motion[0]
        self.pos[1]+=self.motion[1]
    def draw(self,display,camera):
        if not self.clr == (255,255,255):
            particle_images[self.type][int(self.frame)] = swap_color(particle_images[self.type][int(self.frame)],(255,255,255),self.clr)
        blit_offset(display,particle_images[self.type][int(self.frame)],(self.pos[0]-camera[0],self.pos[1]-camera[1]),[0,0],centered=True)
        
