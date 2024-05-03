import pygame,os

def load_img(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0))
    return img

# {'player': {'idle':[images,speed],'run':[images,speed]}}
global GLOBAL_IMAGES
GLOBAL_IMAGES = {}

def load_animations(path):
    global GLOBAL_IMAGES
    entity_types = [] #Names of Entities

    for e_name in os.listdir(path):
        entity_types.append(e_name) #['player','enemy']
        path_n = path + '/' + e_name

        entity_actions = {}
        for i,actions in enumerate(os.listdir(path_n)):
            path_nn = path + '/' + e_name + '/' + actions
            #entity_actions.append(actions)

            images = []
            for i2,frames in enumerate(os.listdir(path_nn)):
                images.append(load_img(path_nn + '/' + frames))
                entity_actions[actions] = images

            GLOBAL_IMAGES[e_name] = entity_actions
                

        
    
    
