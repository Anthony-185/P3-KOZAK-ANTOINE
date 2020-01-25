import tkinter
from grid_module import *

# _____________________________________________________________________________
# [ ] the area on the right as a useful verbose mode !!!!
# [ ] log function
# [X] lag with 100x100 cases : escape funny_color if Gird > 1117
# _____________________________________________________________________________
class Game:

    @V.for_vendetta
    def __init__(self):
        WIDTH = 550 ; HEIGHT = 400 # ----------------------------> CANVAS SIZE
        Game.DX = WIDTH // Grid.row # ------+--------------------> case lenght
        Game.DY = HEIGHT // Grid.column # --+
        Game.CX = WIDTH % Grid.row // 2 # ------+-------------> removing marge
        Game.CY = HEIGHT % Grid.column // 2 # --+
        self.tk = tkinter.Tk()
        self.tk.geometry('958x404+0-100') # ---------------------> Window size
        self.tk.title("MacGyver's Game")
        self.canvas = tkinter.Canvas(self.tk,
            width  = WIDTH,
            height = HEIGHT, bg='black')
        self.canvas.grid(row=0,column=0) # ---> place the canvas in the window
        for case in Grid.all:
            if   case == Grid.dic['start']:     color, TAG= 'green', 'start'
            elif case == Grid.dic['item_1']:    color, TAG= 'white', 'item'
            elif case == Grid.dic['item_2']:    color, TAG= 'white', 'item'
            elif case == Grid.dic['item_3']:    color, TAG= 'white', 'item'
            elif case == Grid.dic['final_goal']:color, TAG= 'red', 'final_goal'
            elif case in Grid.path:             color, TAG= 'blue', 'path'
            else:                               color, TAG= 'darkblue', 'wall'
            pos = self.calcul_canvas_position(case)
            case.tk = self.canvas.create_rectangle(pos, fill=color, tag = TAG)
            self.tk.update()
        pos = self.calcul_canvas_position(Hero.pos)
        Hero.tk = self.canvas.create_rectangle(pos, fill='lightblue')
        self.canvas.bind_all('<KeyPress-Left>',  self.move__left) # + 1
        self.canvas.bind_all('<KeyPress-Right>', self.move_right) # + 2
        self.canvas.bind_all('<KeyPress-Up>',    self.move____up) # + 3
        self.canvas.bind_all('<KeyPress-Down>',  self.move__down) # + 4
    # =============================== LINKED :        +-------------+
    #                                                 |
    @V.for_vendetta #                                 |
    def move__left(self, event): Hero.move((-1, 0)) # + 1
    @V.for_vendetta #                                 |
    def move_right(self, event): Hero.move((+1, 0)) # + 2
    @V.for_vendetta #                                 |
    def move____up(self, event): Hero.move((0, -1)) # + 3
    @V.for_vendetta #                                 |
    def move__down(self, event): Hero.move((0, +1)) # + 4

    @staticmethod
    @V.for_vendetta
    def calcul_canvas_position(case):
        pos  = [case[0] * Game.DX, case[1] * Game.DY] # ----> general position
        pos  = [pos[0] - Game.DX + 2 + Game.CX,  # pos - case corner up-left
                pos[1] - Game.DY + 2 + Game.CY]  # small space + window marge
        pos += [pos[0] + Game.DX - 1, pos[1] + Game.DY - 1] # -> add end coord
        return pos

    @V.for_vendetta
    def funny_color(self, i = [0]):
        i[0] = i[0] + 32 if i[0] < 16**3-2047 else -16**3+2048
        x = hex( abs( i[0]))[2:] ; x = f'{x:0>3}'
        self.canvas.itemconfig(Hero.tk, fill= '#' + x + '0' * 6)
        self.canvas.itemconfig('item', fill= '#' + x * 3)
        if Grid.row * Grid.column >= 1117: return
        # pass this if big Grid
        self.canvas.itemconfig('wall', fill= '#0ff0ff' + x)

    @V.for_vendetta
    def hero_move_in_canvas(self):
        pos = self.calcul_canvas_position(Hero.pos)
        self.canvas.coords(Hero.tk, pos)

    @V.for_vendetta
    def run(self):
        self.funny_color()
        self.hero_move_in_canvas()
        self.tk.update_idletasks()
        self.tk.update()
# ___________________________________________________________________________ #
if __name__ == '__main__':

    Path(50,50).by_path_generator()
    Hero.pos = Grid.dic['start']
    game = Game()
    while 1: game.run()