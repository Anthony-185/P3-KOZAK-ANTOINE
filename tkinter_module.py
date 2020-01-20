print('=== === starting first line === ===')
import tkinter
import random
import time
import string
from grid_module import *
print(' --- import done --- \n== enable grid ==')
# ___________________________________________________________________________ #
Path().by_path_generator()
Hero.pos = Grid.dic['start']
print(' --- grid enabled - Hero in place --- \n== init Tkinter ==')
# ___________________________________________________________________________ #
WIDTH = 550 ; HEIGHT = 400 # ------------------------------------> CANVAS SIZE
tk = tkinter.Tk()
tk.geometry('958x404+0-100') # ----------------------------------> Window size
tk.title("MacGyver's Game")
canvas = tkinter.Canvas(tk,
    width  = WIDTH,
    height = HEIGHT, bg='black')
canvas.grid(row=0,column=0) # ---------> where pacing the canvas in the window
tk.update()
print('-- Tkinter initied --\n== starting drawing grid ==')
# ___________________________________________________________________________ #
def calcul_canvas_position(case):
    pos  = [case[0] * DX, case[1] * DY] # ------------------> general position
    pos  = pos[0] - DX + 2 + CX, pos[1] - DY + 2 + CY # -------> center calcul
    pos += pos[0] + DX - 1, pos[1] + DY - 1 # -----> adding lenght of the case
    return pos

DX, DY = WIDTH // 15, HEIGHT // 15 # ----------------------------> case lenght
CX, CY = WIDTH % 15 // 2, HEIGHT % 15 // 2 # -----------------> removing marge
for case in Grid.all:
    if   case == Grid.dic['start']:      color = 'green'   ; TAG='start'
    elif case == Grid.dic['item_1']:     color = 'white'   ; TAG='item'
    elif case == Grid.dic['item_2']:     color = 'white'   ; TAG='item'
    elif case == Grid.dic['item_3']:     color = 'white'   ; TAG='item'
    elif case == Grid.dic['final_goal']: color = 'red'     ; TAG='final_goal'
    elif case in Grid.path:              color = 'blue'    ; TAG='path'
    else:                                color = 'darkblue'; TAG='wall'
    pos = calcul_canvas_position(case)
    case.tk = canvas.create_rectangle(pos, fill=color, tag = TAG)
    tk.update()
print('-- grid drown --\n== starting Hero function ==')
# ___________________________________________________________________________ #
pos = calcul_canvas_position(Hero.pos)
Hero.tk = canvas.create_rectangle(pos, fill='lightblue')

def hero_move_in_canvas(i = [0]):
    i[0] = i[0] + 128 if i[0] < 16**3-2047 else -16**3+2048
    canvas.itemconfig(Hero.tk, fill = '#'+f'{hex(abs(i[0]))[2:]:0>3}'*2+'000')
    canvas.itemconfig('wall', fill = '#0ff0ff'+f'{hex(abs(i[0]))[2:]:0>3}')
    pos = calcul_canvas_position(Hero.pos)
    canvas.coords(Hero.tk, pos)

def move_0xxx(event): Hero.move((-1, 0))
def move_x0xx(event): Hero.move((+1, 0))
def move_xx0x(event): Hero.move((0, -1))
def move_xxx0(event): Hero.move((0, +1))

canvas.bind_all('<KeyPress-Left>',  move_0xxx)
canvas.bind_all('<KeyPress-Right>', move_x0xx)
canvas.bind_all('<KeyPress-Up>',    move_xx0x)
canvas.bind_all('<KeyPress-Down>',  move_xxx0)
print('-- hero functions defines --\n== starting main loop ==')
# ___________________________________________________________________________ #
while True:
    hero_move_in_canvas()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.001)