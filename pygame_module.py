print('importing')
import pygame
from pygame.locals import *
from grid_module import *


RESOLUTION = (400,300)
ROW = 15 ; COLUMN = 15
DX = RESOLUTION[0] // ROW ; DY = RESOLUTION[1] // COLUMN
white, black, red = (255,255,255), (0,0,0), (255,0,0)
screen = pygame.display.set_mode(RESOLUTION)

class Py_game_1():
    def __init__(self):
        print('py_game_1_init')
        print('Grid in init ', Grid)
        pygame.init() # Pygame init =======
        print('pygame_initiated')
        self.screen = pygame.display.set_mode(RESOLUTION)
        print('screen_initiated')
        self.clock = pygame.time.Clock()
        print('clock_initied')
        self.update_screen()
        print('init done')
            
    def handleEvents(self):
        ''' only handle quit pygame, not working well... '''
        List_event = pygame.event.get()
        for event in List_event:
            if event.type == QUIT: pygame.quit()
        return List_event
    
    def key_pressed(self, hold = [[]]):
        ''' hold is here to prevent multi case deplacement
            it's a list so it can be keep in memory inside the function '''
        pressed_keys = pygame.key.get_pressed()
        if not hold[0] == pressed_keys:
            if   pressed_keys[K_LEFT]:  Hero.move((-1, 0))
            elif pressed_keys[K_RIGHT]: Hero.move((+1, 0))
            elif pressed_keys[K_UP]:    Hero.move((0, -1))
            elif pressed_keys[K_DOWN]:  Hero.move((0, +1))
            print('key_pressed - ', end = '')
        hold.pop() ; hold.append(pressed_keys)
        return pressed_keys

    def update_screen(self):
        ''' draw all objects, in reverse because all specials items
            are at the start of the list '''
        self.screen.fill(black)
        for pos in Grid.all:
            color = black
            if pos in Grid.path: color = red
            if pos in Grid.object: color = white
            if pos == Hero.pos: color = (0,128,128)
            if pos == Grid.dic['final_goal']: color = (0,0,255)
            self.draw(pos[0] - 1, pos[1] - 1, color)
            pygame.display.flip()
        print('screen update - ', end = '')

    def draw(self, x, y, color):
        ''' just draw a rectangle, take x, y, and color 
            it's x - 1 and y - 1 already converted /!\ '''
        pygame.draw.rect(self.screen, color,(x * DX, y * DY, DX, DY))
        print('*', end = '')
                    
    def run(self, running = [1]):
        ''' main function of the game,
            run everything in game '''
        old_key = new_key = self.key_pressed()
        i = 0
        while running[0]:
            new_key = self.key_pressed()
            self.handleEvents()
            if any(new_key) and not any(old_key):
                self.update_screen()
                C.console_print()
                print('loop executed '+str(i))
            i += 1
            self.clock.tick(60)
            old_key = new_key
            if running[0] == 2 : running[0] = 0

if __name__ == '__main__':
    print('- - in main - -')
    import random
    import time
    
    
    print('=== starting ===')
    path = Path()
    path.by_path_generator()
    Hero.pos = Grid.dic['start']
    print('GRID ENABLE = STARTING MAIN LOOP')
    Py_game_1().run()