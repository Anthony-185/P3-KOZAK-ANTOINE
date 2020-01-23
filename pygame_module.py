import pygame
from pygame.locals import *
from grid_module import *
# ___________________________________________________________________________ #
# [X] Bug: if one key maintain pressed and pressing others, doing mayhem !
# [ ] Ugly !!!!!
# [ ] use the near function to know the case to draw
#     so you dont have to draw all the grid, just the near cases
# ___________________________________________________________________________ #
white, black, red, blue = (255,)*3, (0,)*3, (255,0,0), (0,0,255)
class Py_game_1():
    def __init__(self):
        RESOLUTION = (400,300)
        self.DX = RESOLUTION[0] // Grid.row
        self.DY = RESOLUTION[1] // Grid.column
        self.CX = RESOLUTION[0] % Grid.row // 2 # -----+
        self.CY = RESOLUTION[1] % Grid.column // 2 # --+------> removing marge
        screen = pygame.display.set_mode(RESOLUTION)
        pygame.init() # Pygame init =======
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.update_screen()
            
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
        hold.pop() ; hold.append(pressed_keys)
        return pressed_keys

    def update_screen(self):
        ''' draw all objects, in reverse because all specials items
            are at the start of the list '''
        self.screen.fill(black)
        for pos in Grid.all:
            color = (128,128,128)
            if pos in Grid.object: color = white
            elif pos in Grid.path: color = (50,50,255)
            if pos == Hero.pos: color = (0,0,200)
            elif pos == Grid.dic['final_goal']: color = red
            elif pos == Grid.dic['start']: color = (0, 255, 0)            
            self.draw(pos[0] - 1, pos[1] - 1, color)
        pygame.display.flip()

    def draw(self, x, y, color):
        ''' just draw a rectangle, take x, y, and color 
            it's x - 1 and y - 1 already converted /!\ '''
        pos = (x * self.DX + self.CX + 1, 
               y * self.DY + self.CY + 1, 
               self.DX - 2, 
               self.DY - 2)
        pygame.draw.rect(self.screen, color, pos)
                    
    def run(self):
        ''' main function of the game,
            run everything in game '''
        self.key_pressed()
        self.handleEvents()
        self.update_screen()
        self.clock.tick(60)

if __name__ == '__main__':

    Path(25,25).by_path_generator()
    Hero.pos = Grid.dic['start']
    game = Py_game_1()            
    while 1:
        game.run()