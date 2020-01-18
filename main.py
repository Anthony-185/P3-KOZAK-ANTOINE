from grid_module import *
from pygame_module import *
# _____________________________________________________________________________
# MUST BE THE MAIN MODULE
# [ ] ALL class Game --- run the game, with or wthout tkinter or pygame
# [ ] Add Pygame module
# [ ] Add Tkinter module
# [ ] Redefine Case and Path, outside Grid
# _____________________________________________________________________________

CONSOLE = False
TKINTER = False
PYGAME = False
if not TKINTER and not PYGAME: CONSOLE = True
MODE = 'pygame' * PYGAME or 'tkinter' * TKINTER or 'console' * CONSOLE


def V(func=None, i = [0], *args):
    i[0] += 1
    i.append((i[0], func, args))
    return func    

class Mode_tkinter:
    pass
    
class Mode_pygame:
    pass
    
class Mode_console:
    def __init__(self):
        pass
    
    def run(self):
        print(4 * "\n" + 80 * "_" + "\n\n")
        for y in range(1, Grid.column + 1):
            for x in range(1, Grid.row + 1):
                if (x,y) == Mac.pos:                  symbol="|."
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
        elif command == 'z' : Mac.move((0, -1))
        elif command == 'd' : Mac.move((+1, 0))
        elif command == 's' : Mac.move((0, +1))
        elif command == 'q' : Mac.move((-1, 0))
    

class Game:
    def __init__(self):
        path = Path()
        path.by_path_generator()
        self.playing = True
    
    def run(self):
        while self.playing:
            if CONSOLE: 
                self.console.run()
                self.console.handle()

    
if __name__ == '__main__':

    game = Game()
    Mac = Hero('Mac Gyver', Grid.dic['start'])
    game.console = Mode_console()    
    game.run()
    