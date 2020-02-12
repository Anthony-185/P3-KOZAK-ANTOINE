from grid_module import *
from tkinter_module import *
from pygame_module import *
import os

print('init')# to rm

# from collection
# _____________________________________________________________________________
# [ ] MUST BE COOL
# [ ] run the game, can restart
# [ ] //// //// Overide print() to print in main window tkinter label //// ////
# [X] Add Pygame module ?
# [X] Add Tkinter module
# [ ] a SHOWDOWN mode, played by random (autotest)
# [ ] external file for a lot of variable, parametrable 'settings.txt'
# [X] log function in V in other canvas (can be improved)
# [ ] a oblivion style, can be cool
# _____________________________________________________________________________

path = Path(42,42)
path.by_path_generator()
Hero.pos = Grid.dic['start']
game = Game()
# _____________________________________________________________________________
game.tk.geometry('958x704+10+10')
game.tk.config(background='darkblue')
game.canvas.grid(row=0, column=0, sticky='nwe')
# _____________________________________________________________________________
frame_tk_for_pygame = tkinter.Frame(
    game.tk, width=300, height=300,
    background='yellow', borderwidth=4, relief=None)
frame_tk_for_pygame.grid(row=1, column=1, sticky='nswe')
os.environ['SDL_WINDOWID'] = str(frame_tk_for_pygame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# _____________________________________________________________________________
game_py = Py_game_1()
# _____________________________________________________________________________
WIDTH = 400 ; HEIGHT = 400 # ------------------------------------> CANVAS SIZE
DX, DY = WIDTH // 15, HEIGHT // 15 # ----------------------------> case lenght
CX, CY = WIDTH % 15 // 2, HEIGHT % 15 // 2 # -----------------> removing marge
# _____________________________________________________________________________
game.canvas2 = tkinter.Canvas(game.tk,
            width  = WIDTH,
            height = HEIGHT, bg='black')
game.canvas2.grid(row=0, column=1, sticky='w')
# _____________________________________________________________________________
list_text_canvas = [] ;
for y_space in range(0, WIDTH - 70 ,20):
    list_text_canvas.append( \
        game.canvas2.create_text( 10, y_space + 10,
            text='', fill='cyan', anchor='nw', activefill='white',
            font = ('Terminal', -10), ))
# _____________________________________________________________________________
end_canvas = [
    game.canvas2.create_text(
        10, HEIGHT - 30,
        text='', fill='cyan', anchor='nw', activefill='white',
        font = ('Terminal', -8)),
    game.canvas2.create_line(
        10, HEIGHT-10, WIDTH-10, HEIGHT-10,
        fill='cyan')
    ]
# _____________________________________________________________________________
def deleting_tk_grid():
    Hero.bag = set()
    game.canvas.delete(Hero.tk)
    for case in Grid.all: game.canvas.delete(case.tk)
    Grid.path = set() # better ;) else: infinite loop in map generator
# _____________________________________________________________________________
def de_activate(x): # de activate all buttons
    l = path_button_1, path_button_2, path_button_3
    for i in l:
        i['state'] = 'disabled'
        i['background'] = 'orange'

def re_activate(x): # re activate all buttons
    l = path_button_1, path_button_2, path_button_3
    for i in l:
        i['background'] = 'cyan'
        i['state'] = 'normal'
# _____________________________________________________________________________
def restart_grid():
    de_activate(path_button_1)
    deleting_tk_grid()
    x = random.randrange(15,50)
    y = random.randrange(15,50)
    item = random.randrange(3,11)
    Path( x, y, item).by_path_generator()
    game.restart_tk()
    re_activate(path_button_1)

def restart_grid_in_square():
    de_activate(path_button_2)
    deleting_tk_grid()
    x = y = 15
    Path( x, y).by_path_generator()
    game.restart_tk()
    re_activate(path_button_3)

def loading_defaut_map():
    de_activate(path_button_3)
    deleting_tk_grid()
    Path().by_load_defaut_map()
    game.restart_tk()
    re_activate(path_button_3)
# _____________________________________________________________________________
frame_info = tkinter.Canvas(game.tk,
    width = 500, height = 250, bg='orange')
frame_info.grid(row=1, column=0)
frame_info.grid_propagate(0)
canvas_info = tkinter.Canvas(frame_info,
    width = 480, height = 50, bg = 'black')
canvas_info.grid(row = 0, column = 0, columnspan = 10, sticky = '')
list_canvas_info = []
def init_show_bag():
    global list_canvas_info
    list_canvas_info = []
    x = len(Grid.dic) * 40 / 2
    x = 240 - x + 6
    for i, j in enumerate(Grid.dic):
        color = 'white' if 'item' in j else None
        if not color:
            color = 'green' if j == 'start' else 'red'
        list_canvas_info.append(
            canvas_info.create_rectangle(
                x + 40 * i     , 10,
                x + 40 * i + 30, 40, outline = color ) )
    return None
    
init_show_bag()
    
def f_canvas_info(old_bag = [None], deja_vu_grid = [None]):
    global list_canvas_info
    if old_bag[0] == None : old_bag[0] = {}  
    if deja_vu_grid[0] != Grid.dic: # if game has restart, re-initialize
        for i in list_canvas_info: canvas_info.delete(i)
        init_show_bag()
        l = 0
        for i in Hero.bag:
            l += 1
            canvas_info.itemconfig(list_canvas_info[l], fill = '')
        deja_vu_grid[0] = Grid.dic.copy()
        canvas_info.update()
        return None
    if old_bag[0] == Hero.bag:
        return None # if nothing change, pass
    l = 0
    for i in Hero.bag:
        l += 1
        canvas_info.itemconfig(list_canvas_info[l], fill = 'white')
    canvas_info.update()
    old_bag[0] = Hero.bag.copy()
    return None
# _____________________________________________________________________________
# button left
path_button_1 = tkinter.Button(
    game.canvas2, command=restart_grid,
    disabledforeground='white',
    text='random path',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(10, HEIGHT-60, anchor='nw', window=path_button_1)
# button right
path_button_2 = tkinter.Button(
    game.canvas2, command=restart_grid_in_square,
    disabledforeground='white',
    text='15*15 grid',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(330, HEIGHT-60, anchor='nw', window=path_button_2)
# middle button
path_button_3 = tkinter.Button(
    game.canvas2, command=loading_defaut_map,
    disabledforeground='white',
    text='load defaut map',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(97, HEIGHT-60, anchor='nw', window=path_button_3)
# _____________________________________________________________________________
def verbose_clean():
    if activate_verbose.get(): return None
    for i in list_text_canvas:
        game.canvas2.itemconfig( i, text='')
# _____________________________________________________________________________
activate_verbose = tkinter.IntVar()
activate_verbose.set(1)
check_verbose = tkinter.Checkbutton(
    game.canvas2, variable = activate_verbose, command = verbose_clean,
    text='activate verbose',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(202, HEIGHT-60, anchor='nw', window=check_verbose)
# _____________________________________________________________________________
old_a = [] ; m = 0 ; limit = 100 ; all = []
def print_log(intern_var = [None]):
    if intern_var[0] == None:
        intern_var[0] = {'m': 0, 'limit': 100, 'old_a': []}
    m, limit, old_a = \
        intern_var[0]['m'], intern_var[0]['limit'], intern_var[0]['old_a']
    m = m + 1 if m <= limit else 0 
    a = [] ; all = []
    
    if activate_verbose.get():
    
        for i,j in V.a.items(): # all messgages to show
            text = str(j[1]) # all text
            all += [str(j[0])] if len(all) < 17 else [] # all increment
            if len(text) > 50: # if msg > width canvas
                if m > len(text) - 50:  # to stop for 50 loop the msh show
                    a.append(f'{i[:10]: <10} : {text[-50:]:.>50}')
                else: # to advance the msg
                    a.append(f'{i[:10]: <10} : {text[m:m+50]:.>50}')
            # if msg < width canvas
            else: a.append(f'{i[:10]: <10} : {text[-50:]:.>50}')
            limit = max(limit, len(text)) # limit = bigger msg
        if a[1:] != old_a[1:]: # if all msg the same, don't update the canvas
            for i, j in zip([a[0]] + a[:1:-1], list_text_canvas):
                game.canvas2.itemconfig( j, text=i)
        old_a = a
    
    else:
        for i,j in V.a.items():
            all += [str(j[0])] if len(all) < 17 else [] # all increment

    
    game.canvas2.itemconfig(end_canvas[0], text = ' '.join(all))
    # show progress of m
    loop_prog = m / limit * (WIDTH - 20)
    game.canvas2.coords(end_canvas[1],
        10, HEIGHT-10, 10 + loop_prog, HEIGHT-10)
    c = 'cyan' if m < limit - 50 else 'orange'
    game.canvas2.itemconfig(end_canvas[1], fill = c)
    intern_var[0]['m'], intern_var[0]['limit'], intern_var[0]['old_a'] = \
        m, limit, old_a
    
    
while 1:

    print_log()
    f_canvas_info()
    game.run()
    game_py.run()