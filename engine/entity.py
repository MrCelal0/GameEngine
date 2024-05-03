#Entity Engine
import pygame,random

def blit_center(display,surface,pos):
    x = int(pos[0]-surface.get_width()/2)
    y = int(pos[1]-surface.get_height()/2)
    display.blit(surface,(x,y))

class Entity(object):
    def __init__(self, pos, r_size, name):
        self.pos = pos
        self.r_size = r_size
        self.name = name
        
        self.velocity = [0,0]
        
        self.action = 'idle'
        self.frame = 0

        self.movement = [False,False,False,False]

        self.rot = 0
        self.scale = [1,1]
        self.opacity = 255
        self.flip = False

        self.collisions = {'up':False,'down':False,'right':False,'left':False}

        self.image = pygame.Surface((r_size[0],r_size[1]))
        self.rect = pygame.FRect((self.pos[0],self.pos[1],self.r_size[0],self.r_size[1]))
        
    def init_img(self,GLOBAL_IMAGES,config):
        for name in config:
            if self.action == name:
                self.frame += config[name]
        if self.frame >= len(GLOBAL_IMAGES[self.name][self.action]):
            self.frame = 0
        self.image = GLOBAL_IMAGES[self.name][self.action][int(self.frame)]
        self.image.set_colorkey((0,0,0))

        if self.rot != 0:
            self.image = pygame.transform.rotate(self.image,self.rot)
        if self.scale != [1,1]:
            new_scale = (self.image.get_width()*self.scale[0],self.image.get_height()*self.scale[1])
            self.image = pygame.transform.scale(self.image,new_scale)
        if self.opacity != 255:
            self.image.set_alpha(self.opacity)

    def collision_list(self,tile_rects):
        collisions = []
        for rect in tile_rects:
            if self.rect.colliderect(rect):
                collisions.append(rect)
        return collisions
        
    def tile_collision(self,tiles):
        movement = self.velocity.copy()
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x += movement[0]
        hit_list = self.collision_list(tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += movement[1]
        hit_list = self.collision_list(tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types 
        

    def change_action(self,n_act):
        if n_act != self.action:
            self.action = n_act
            self.frame = 0

    def draw(self,display,camera=[0,0]):
        display.blit(pygame.transform.flip(self.image,self.flip,False),(self.rect.centerx-self.r_size[0]/2-camera[0],self.rect.centery-self.r_size[1]/2-camera[1]))
        #blit_center(display,pygame.transform.flip(self.image,self.flip,False),(self.rect.x - camera[0], self.rect.y - camera[1]))
        
