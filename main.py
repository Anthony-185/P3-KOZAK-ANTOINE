from grid_module import *
from pygame_module import *
from tkinter_module import *
# _____________________________________________________________________________
# [X] MUST BE THE MAIN MODULE
# [ ] run the game, with or wthout tkinter or pygame
# [X] Add Pygame module
# [X] Add Tkinter module
# [X] Redefine Case and Path, outside Grid
# [ ] external file for variable
# [ ] log function
# _____________________________________________________________________________

def log(func=None, i = [0], *args):
    i[0] += 1
    i.append((i[0], func, args))
    return func    

class MAIN:
    def __init__(self):
        self.game1 = Py_game_1()
        self.game2 = Game()

    def run(self):
        self.game1.run()
        self.game2.run()
    
if __name__ == '__main__':
    
    path = Path()
    path.by_path_generator()
    Hero.pos = Grid.dic['start']
    
    game = MAIN()
    while 1:
        game.run()