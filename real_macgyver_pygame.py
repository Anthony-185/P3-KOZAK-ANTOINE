import pygame
from pygame.locals import *

import random

RESOLUTION = (400,300)
white, black, red = (255,255,255), (0,0,0), (255,0,0)
screen = pygame.display.set_mode(RESOLUTION)

ROW = 15 ; COLUMN = 15

class Object: # Great name, yeah i know ^^

    def __init__(self, name, pos):
        self.name = name
        self.pos  = pos
        
    def draw(self, surface):
        self.x , self.y = int(self.x), int(self.y)
        pygame.draw.circle(surface, black, (self.x, self.y), self.radius)


class Hero(Object): # only for MacGyver

    def update(self): # OLD VERSION =======
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 0 or self.x >= RESOLUTION[0]): self.dx *= -1
        if (self.y <= 0 or self.y >= RESOLUTION[1]): self.dy *= -1

        
class Grid:
    '''
    self.all = set with all position of the grid
    self.path = set with all position clear (!= wall)
    self.dict_obj_pos = dict with all items
    >>> dict_obj_pos in path in all '''

    def __init__():
        self.all = {(x+1, y+1) for x in range(ROW) for y in range(COLUMN)}
        self.path = set()
        self.dict_obj_pos = {x: 0
            for x in "start item_1 item_2 item_3 foe".split() }
        self.init_Path()

    def init_Path(self) # can be improve: obj = iter(dict) ; dict(next(obj))
        x = random.randrange(ROW) + 1 
        y = random.randrange(COLUMN) + 1
        self.dict_obj_pos['start'] = actual_position = (x, y)
        self.path.add( actual_position )
        road_finish = False ; i_some_path = 0

        while not road_finish:
            x, y = actual_position

            future_postion = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            future_postion = [i for i in future_postion
                if not i in self.path and i in self.all]

            if not future_postion:
                actual_position = random.sample(self.path, 1)[0]
                continue

            actual_position = random.choice(future_postion)
            self.path.add(actual_position)
            i_some_path += 1

            if i_some_path > 17 and random.randrange(117) > 77:
                i_some_path = 0
                for i in self.dict_obj_pos.keys():
                    if 'item' in i and not self.dict_obj_pos[i]:
                        self.dict_obj_pos[i] = actual_position
                        break
                    else: 
                        self.dict_obj_pos['final_goal'] = actual_position
                        assert all(self.dict_obj_pos.values())
                        road_finish = True

class game():

    def __init__(self):
    
        pygame.init() # Pygame init =======
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        
        self.grid = Grid()
        self.gameObjects = []
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit()
        pressed_keys = pygame.key.get_pressed()
        if   pressed_keys[K_LEFT]:  self.move('left')
        elif pressed_keys[K_RIGHT]: self.move('right')
        elif pressed_keys[K_UP]:    self.move('up')
        elif pressed_keys[K_DOWN]:  self.move('down')
        
    def move(self, direction):
        ''' call the Hero class '''


    def run(self):
        while True:
            self.handleEvents()
            
            for gameObj in self.gameObjects: gameObj.update()
            self.screen.fill(black)                    
            for gameObj in self.gameObjects: gameObj.draw(self.screen)

            self.clock.tick(60)
            pygame.display.flip()

if __name__ == '__main__':
    game().run()