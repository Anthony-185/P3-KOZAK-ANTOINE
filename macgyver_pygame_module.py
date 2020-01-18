from grid_module import *

# _____________________________________________________________________________
# MUST BE THE MAIN MODULE
# [ ] ALL class Game --- run the game, with or wthout tkinter or pygame
# [ ] Add Pygame module
# [ ] Add Tkinter module
# [ ] Redefine Case and Path, outside Grid
# _____________________________________________________________________________

def V(func=None, i = [0], *args):
    i[0] += 1
    i.append((i[0], func, args))
    return func    

class Game:
    def __init__(self):
        path = Path()
        path.by_path_generator()
        

if __name__ == '__main__':
    
    
    
    Game()