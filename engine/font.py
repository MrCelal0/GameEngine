import pygame,sys,random
from pygame.locals import *

def load_img(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0))
    return img

def crop(img,crop_rect):
    surf = pygame.Surface((crop_rect.w,crop_rect.h))
    surf.set_colorkey((0,0,0))
    surf.blit(img,(0,0),crop_rect)
    return surf

def swap_color(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy

class Font():
    def __init__(self,path,timer=False,color=(255,255,254)):
        self.space = 1
        self.path = path
        self.font_images = {}
        if not timer:
            self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        if timer:
            self.font_order = ['0','1','2','3','4','5','6','7','8','9']
        font_img = load_img(path)
        if color != (255,0,0):
            font_img = swap_color(font_img,(255,0,0),color)
        self.current_char = 0
        self.char_size = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x,0))
            c = (c[0],c[1],c[2])
            if c == (255,255,255): #Found a Char
                char_img = crop(font_img,pygame.Rect(x - self.char_size ,0,self.char_size,font_img.get_height()))
                self.font_images[self.font_order[self.current_char]] = char_img
                self.current_char += 1
                self.char_size = 0
            else:
                self.char_size += 1

        self.space_size = self.font_images['0'].get_width()

    def get_font_width(self,text):
        width = 0
        if text != '':
            for char in text:
                if char != ' ':
                    width += self.font_images[char].get_width() + self.space
                else:
                    width += self.space_size + self.space
        return width
        
    def render(self,display,text,pos,outline=False):
        x_offset = 0
        if text != '':
            for char in text:
                if char != ' ':
                    if not outline:
                        display.blit(self.font_images[char],(pos[0] + x_offset,pos[1]))
                        x_offset += self.font_images[char].get_width() + self.space
                    else:
                        mask = pygame.mask.from_surface(self.font_images[char])
                        mask_img = mask.to_surface()
                        mask_img.fill((0,0,0))
                        #mask_img.set_colorkey((0,0,0))
                        for position in ([((pos[0] + x_offset)+1,pos[1]),((pos[0] + x_offset)-1,pos[1]),(pos[0] + x_offset,pos[1]+1),(pos[0] + x_offset,pos[1]-1)]):
                            display.blit(mask_img,position)
                        display.blit(self.font_images[char],(pos[0] + x_offset,pos[1]))
                        x_offset += self.font_images[char].get_width() + self.space

                else:
                    x_offset += self.space_size + self.space
                
