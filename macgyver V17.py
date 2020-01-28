from grid_module import *
from tkinter_module import *
from pygame_module import *
# from collection
# _____________________________________________________________________________
# [ ] MUST BE COOL
# [ ] run the game, can restart
# [ ] Add Pygame module ?
# [X] Add Tkinter module
# [ ] a SHOWDOWN mode, played by random (autotest)
# [ ] external file for a lot of variable, parametrable 'settings.txt'
# [X] log function in V in other canvas (can be improved)
# [ ] a oblivion style, can be cool
# _____________________________________________________________________________
path = Path(50,50)
path.by_path_generator()
Hero.pos = Grid.dic['start']
game = Game()
game_py = Py_game_1()
# _____________________________________________________________________________
WIDTH = 400 ; HEIGHT = 400 # ------------------------------------> CANVAS SIZE
DX, DY = WIDTH // 15, HEIGHT // 15 # ----------------------------> case lenght
CX, CY = WIDTH % 15 // 2, HEIGHT % 15 // 2 # -----------------> removing marge
# _____________________________________________________________________________
game.canvas2 = tkinter.Canvas(game.tk,
            width  = WIDTH,
            height = HEIGHT, bg='black')
game.canvas2.grid(row=0, column=1)
# _____________________________________________________________________________
list_text_canvas = [] ;
for y_space in range(0, WIDTH ,20):
    list_text_canvas.append( \
        game.canvas2.create_text( 10, y_space + 10,
            text='', fill='cyan', anchor='nw', activefill='white',
            font = ('Terminal', -10), 
            ))
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
old_a = [] ; m = 0 ; limit = 100 ; all = []
# _____________________________________________________________________________
def restart_grid():
    Hero.bag = set()
    for case in Grid.all: game.canvas.delete(case.tk)
    Grid.path = set() # better ;)
    x = random.randrange(15,50)
    y = random.randrange(15,50)
    item = random.randrange(3,10)
    Path( x, y, item).by_path_generator()
    game.restart_tk()

def restart_grid_in_square():
    Hero.bag = set()
    for case in Grid.all: game.canvas.delete(case.tk)
    Grid.path = set() # better ;)
    x = y = 15
    Path( x, y).by_path_generator()
    game.restart_tk()

path_button = tkinter.Button(
    game.canvas2, command=restart_grid,
    text='random path',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(10, HEIGHT-60, anchor='nw', window=path_button)
path_button = tkinter.Button(
    game.canvas2, command=restart_grid_in_square,
    text='15*15 grid',
    background='cyan',
    activebackground='black', activeforeground='cyan')
game.canvas2.create_window(270, HEIGHT-60, anchor='nw', window=path_button)

while 1:

    
    m = m + 1 if m <= limit else 0 
    a = [] ; all = []
    for i,j in V.a.items(): # all messgages to show
        text = str(j[1])
        all += [str(j[0])]
        if len(text) > 50: # if msg > width canvas
            if m > len(text) - 50:  # to stop for 50 loop the msh show
                a.append(f'{i[:10]: <10} : {text[-50:]:.>50}')
            else: # to advance the msg
                a.append(f'{i[:10]: <10} : {text[m:m+50]:.>50}')
        # if msg < width canvas
        else: a.append(f'{i[:10]: <10} : {text[-50:]:.>50}')
        limit = max(limit, len(text)) # limit = bigger msg
    if a[1:] != old_a[1:]: # if all msg the same, don't update the canvas
        for i, j in zip(a, list_text_canvas):
            game.canvas2.itemconfig( j, text=i)
    old_a = a
    game.canvas2.itemconfig(end_canvas[0], text = ' '.join(all))
    
    # show progress of m
    loop_prog = m / limit * (WIDTH - 20)
    game.canvas2.coords(end_canvas[1],
        10, HEIGHT-10, 10 + loop_prog, HEIGHT-10)
    
    game.run()
    game_py.run()