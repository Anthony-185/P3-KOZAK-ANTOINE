import pygame
from pygame.locals import *
import random
import time

# _____________________________________________________________________________
'''
## comment :
  debug in print
  remove all ## to see function call order '''

RESOLUTION = (400,300)
ROW = 15 ; COLUMN = 15
DX = RESOLUTION[0] // ROW ; DY = RESOLUTION[1] // COLUMN

white, black, red = (255,255,255), (0,0,0), (255,0,0)
screen = pygame.display.set_mode(RESOLUTION)
## print('=== STARTING ===')

class Object: # Great name, yeah i know ^^
    def __init__(self, name, pos):
        self.name = name
        self.x , self.y = pos[0] -1, pos[1] -1
        self.pos = self.x * DX, self.y * DY, DX, DY
        ## print('init__Object = ', end='')

    def draw(self, surface):
        if   'path'  in self.name: color = (0,0,250)
        elif 'wall'  in self.name: color = (5,5,5)
        elif 'start' in self.name: color = (0,255,0)
        elif 'item'  in self.name: color = (255,255,255)
        elif 'foe'   in self.name: color = (200,0,0)
        else: # draw even if someting wrong
            pygame.draw.rect(surface, (255,127,127), self.pos)
            print("error in : ", self.pos,' name : ', self.name)
            return None
        pygame.draw.rect(surface, color, self.pos)
        ## print('draw = ', end='')
        # draw à l'infini
        # pensé à effacer sinon trace à l'infini

    def update(self):
        ## print('update = ', end='')
        if not 'start' in self.name: return None
        pass
        # self.x += self.dx
        # self.y += self.dy
        # if (self.x <= 0 or self.x >= RESOLUTION[0]): self.dx *= -1
        # if (self.y <= 0 or self.y >= RESOLUTION[1]): self.dy *= -1
    ## print('class object - ', end='')
    

class Hero(Object): # only for MacGyver
    def update(self): # OLD VERSION =======
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 0 or self.x >= RESOLUTION[0]): self.dx *= -1
        if (self.y <= 0 or self.y >= RESOLUTION[1]): self.dy *= -1


class Grid():
    '''
    self.all = set with all position of the grid
    self.path = set with all position clear (!= wall)
    self.dict_obj_pos = dict with all items
    - > see assert for the relation between the 3 objects '''
    def __init__(self):
        self.all = {(x+1, y+1) for x in range(ROW) for y in range(COLUMN)}
        self.path = set()
        self.dict_obj_pos = {x: 0
            for x in "start item_1 item_2 item_3 foe".split()}
        self.init_Path()
        assert set(self.dict_obj_pos.values()) < self.path < self.all
        ## print('init__Grid = ', end='')

    def init_Path(self): # can be improve: obj = iter(dict) ; dict(next(obj))
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
                    self.dict_obj_pos['foe'] = actual_position
                    road_finish = True
                    assert all(self.dict_obj_pos.values())
        ## print('init_path = ', end='')
    ## print('class grid - ', end='')
    

class game():
    def __init__(self):
        pygame.init() # Pygame init =======
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        
        self.grid = Grid()# .init_Path()
        self.gameObjects = []
        for name, pos in self.grid.dict_obj_pos.items():
            self.gameObjects.append(Object(name, pos))
        for i in self.grid.all:
            if i in self.grid.path: name = 'path '
            else: name = 'wall '
            self.gameObjects.append(Object(name+str(i), i))
        self.update_screen()
        ## print('init__game = ', end='')
            
    def handleEvents(self):
        ''' only handle quit pygame by the window red cross '''
        List_event = pygame.event.get()
        for event in List_event:
            if event.type == QUIT: pygame.quit()
        ## print('handleEvents = ', end='')
        return List_event
    
    def key_pressed(self, hold = [[]]):
        ''' hold is here to prevent multi case deplacement
            it's a list so it can be keep in memory inside the function '''
        pressed_keys = pygame.key.get_pressed()
        if not hold[0] == pressed_keys:
            if   pressed_keys[K_LEFT]:  self.move(x = -1)
            elif pressed_keys[K_RIGHT]: self.move(x = +1)
            elif pressed_keys[K_UP]:    self.move(y = -1)
            elif pressed_keys[K_DOWN]:  self.move(y = +1)
        hold.pop() ; hold.append(pressed_keys)
        ## print('key_pressed = ', end='')
        return pressed_keys

    def move(self, x=0, y=0):
        ''' move mac_gyver, called by self.key_pressed()
            move only if next position is in path '''
        if  (self.gameObjects[0].x + x + 1, \
             self.gameObjects[0].y + y + 1) in self.grid.path:
            self.gameObjects[0].x += x
            self.gameObjects[0].y += y
            X, Y = self.gameObjects[0].x, self.gameObjects[0].y
            self.gameObjects[0].pos = X * DX, Y * DY, DX, DY
        ## print('move = ', end='')

    def update_screen(self):
        ''' draw all objects, in reverse because all specials items
            are at the start of the list '''
        self.screen.fill(black)         
        for gameObj in self.gameObjects[::-1]:
            gameObj.update()
            gameObj.draw(self.screen)
            pygame.display.flip()
        ## print('update_screen = ', end='')
                    
    def run(self):
        ''' main function of the game,
            run everything in game '''
        old_key = new_key = self.key_pressed()
        while True:
            new_key = self.key_pressed()
            self.handleEvents()
            if any(new_key) and not any(old_key):
                self.update_screen()
            self.clock.tick(60)
            old_key = new_key
        ## print('run = ', end='')
    ## print('class game - ', end='')

if __name__ == '__main__':
    ## print('in main - ', end='')
    game().run()