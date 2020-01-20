print('=== === starting first line === ===')
import tkinter
import random
import time
import string
from grid_module import *
print(' --- import done --- \n== enable tkinter ==')
WIDTH = 550 ; HEIGHT = 400 # ------------------------------------> CANVAS SIZE
DX, DY = WIDTH // 15, HEIGHT // 15 # ----------------------------> case lenght
CX, CY = WIDTH % 15 // 2, HEIGHT % 15 // 2 # -----------------> removing marge
# ___________________________________________________________________________ #
class Game:
    def __init__(self):
        Path().by_path_generator()
        Hero.pos = Grid.dic['start']
        self.tk = tkinter.Tk()
        self.tk.geometry('958x404+0-100') # --------------------------> Window size
        self.tk.title("MacGyver's Game")
        self.canvas = tkinter.Canvas(self.tk,
            width  = WIDTH,
            height = HEIGHT, bg='black')
        self.canvas.grid(row=0,column=0) # --------> place the canvas in the window
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
        self.canvas.bind_all('<KeyPress-Left>',  self.move_0xxx)
        self.canvas.bind_all('<KeyPress-Right>', self.move_x0xx)
        self.canvas.bind_all('<KeyPress-Up>',    self.move_xx0x)
        self.canvas.bind_all('<KeyPress-Down>',  self.move_xxx0)

    @staticmethod
    def calcul_canvas_position(case):
        pos  = [case[0] * DX, case[1] * DY] # ------------------> general position
        pos  = pos[0] - DX + 2 + CX, pos[1] - DY + 2 + CY # -------> center calcul
        pos += pos[0] + DX - 1, pos[1] + DY - 1 # -----> adding lenght of the case
        return pos

    def funny_color(self, i = [0]):
        i[0] = i[0] + 128 if i[0] < 16**3-2047 else -16**3+2048
        x = hex( abs( i[0])) [2:] ; x = f'{x:0>3}'
        self.canvas.itemconfig(Hero.tk, fill= '#' + x + '0' * 6)
        self.canvas.itemconfig('wall', fill= '#0ff0ff' + x)
        self.canvas.itemconfig('item', fill= '#' + x * 3)

    def hero_move_in_canvas(self):
        pos = self.calcul_canvas_position(Hero.pos)
        self.canvas.coords(Hero.tk, pos)

    def move_0xxx(self, event): Hero.move((-1, 0))
    def move_x0xx(self, event): Hero.move((+1, 0))
    def move_xx0x(self, event): Hero.move((0, -1))
    def move_xxx0(self, event): Hero.move((0, +1))

print('-- every function defines --\n== starting main loop ==')
# ___________________________________________________________________________ #
if __name__ == '__main__':
    game = Game()
    while True:
        game.funny_color()
        game.hero_move_in_canvas()
        game.tk.update_idletasks()
        game.tk.update()
        time.sleep(0.001)