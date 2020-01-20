from grid_module import *
from pygame_module import *
from tkinter_module import *
# _____________________________________________________________________________
# [X] MUST BE THE MAIN MODULE
# [ ] run the game, with or wthout tkinter or pygame
# [X] Add Pygame module
# [ ] Add Tkinter module
# [X] Redefine Case and Path, outside Grid
# [ ] external file for variable
# [ ] log function
# _____________________________________________________________________________

CONSOLE = True
TKINTER = True
PYGAME = True

def V(func=None, i = [0], *args):
    i[0] += 1
    i.append((i[0], func, args))
    return func    

class Mode_tkinter:
    pass

class Mode_pygame:
    def __init__(self):
        self.game1 = Py_game_1()
        self.game2 = Game()

    def run(self):
        self.game1.run()
        self.game2.funny_color()
        self.game2.hero_move_in_canvas()
        self.game2.tk.update_idletasks()
        self.game2.tk.update()
        
class Mode_console:
    def __init__(self):
        pass
    
    def run(self):
        print(4 * "\n" + 80 * "_" + "\n\n")
        for y in range(1, Grid.column + 1):
            for x in range(1, Grid.row + 1):
                if (x,y) == Hero.pos:                  symbol="|."
                elif (x,y) == Grid.dic['start']:      symbol="|S"
                elif (x,y) == Grid.dic['item_1']:     symbol="|o"
                elif (x,y) == Grid.dic['item_2']:     symbol="|o"
                elif (x,y) == Grid.dic['item_3']:     symbol="|o"
                elif (x,y) == Grid.dic['final_goal']: symbol="|X"
                elif (x,y) in Grid.path:              symbol="| "
                elif (x,y) not in Grid.path:          symbol="|~"
                print(symbol, end="")
            print("|")
                
    def handle(self):
        print(79*'_')
        command = input("z: up, d: right, s: down, q: left, exit to quit\n> ")
    
        if command == 'exit': playing = False
        elif command == 'z' : Hero.move((0, -1))
        elif command == 'd' : Hero.move((+1, 0))
        elif command == 's' : Hero.move((0, +1))
        elif command == 'q' : Hero.move((-1, 0))
    
if __name__ == '__main__':

    print(' - in Main - ')
    
    path = Path()
    path.by_path_generator()
    Hero.pos = Grid.dic['start']
    
    console = Mode_console()
    
    console.run()
    # console.handle()
    print('\n --- console initiated - trying pygame --- ')
    print('Grid in main ', Grid)
    
    
    pygame1 = Mode_pygame()
    while 1:
        pygame1.run()