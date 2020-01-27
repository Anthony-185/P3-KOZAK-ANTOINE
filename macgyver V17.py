from grid_module import *
from tkinter_module import *
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
path_button = tkinter.Button(
    game.canvas2, command=game.restart_tk,
    text='regenerate_path',
    activebackground='black', activeforeground='white')
game.canvas2.create_window(10, HEIGHT-50, anchor='nw', window=path_button)
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