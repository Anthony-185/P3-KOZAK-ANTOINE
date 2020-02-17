from tkinter_module import *
from pygame_module import *
import os

# _____________________________________________________________________________
# [X] //// //// Override print() in main window tkinter label //// ////
# [X] MUST BE COOL --> it is for me ;-)
# [X] run the game, can restart
# [X] Add Pygame module ?
# [X] Add Tkinter module
# [ ] a SHOWDOWN mode, played by random (auto-test) <<<<<< difficult, need time
# [ ] external file like 'settings.txt' <<<<<<<<<<<<<<<<<<<< medium, need time
# [X] log function in V in other canvas, printed
# [ ] a oblivion style, cool <<<<<<<<<<<<<<<< very difficult, need lot of time
# _____________________________________________________________________________

path = Path(42, 42)
path.by_path_generator()
Hero.pos = Grid.dic["start"]
game = Game()
WIDTH = 400
HEIGHT = 600
# _____________________________________________________________________________
game.tk.geometry("958x704+10+10")  # ============================== Main Window
game.tk.config(background="darkblue")
game.canvas.grid(row=0, column=0, sticky="nwe")
# _____________________________________________________________________________
frame_tk_for_pygame = tkinter.Frame(  # ================================ PYGAME
    game.tk,
    width=300,
    height=300,
    background="yellow",
    borderwidth=4,
    relief=None,
)
frame_tk_for_pygame.grid(row=1, column=1, sticky="nswe")
os.environ["SDL_WINDOWID"] = str(frame_tk_for_pygame.winfo_id())
os.environ["SDL_VIDEODRIVER"] = "windib"
game_py = Py_game_1(mode=2)
# _____________________________________________________________________________
DX, DY = WIDTH // 15, HEIGHT // 15  # ---------------------------> case length
CX, CY = WIDTH % 15 // 2, HEIGHT % 15 // 2  # ----------------> removing marge
WIDTH = 400
HEIGHT = 400  # -----------------------------------> CANVAS SIZE
# _____________________________________________________________________________
game.canvas2 = tkinter.Canvas(
    game.tk,  # ===================== canvas on right
    width=WIDTH,
    height=HEIGHT,
    bg="black",
)
game.canvas2.grid(row=0, column=1, sticky="w")
list_text_canvas = []
for y_space in range(0, WIDTH - 110, 20):  # ---> define number of line printed
    list_text_canvas.append(
        game.canvas2.create_text(
            10,
            y_space + 10,
            text="",
            fill="cyan",
            anchor="nw",
            activefill="white",
            font=("Terminal", -10),
        )
    )
# _____________________________________________________________________________
end_canvas = [  # ===================== the bottotm with called number function
    game.canvas2.create_text(
        10,
        HEIGHT - 30,
        text="",
        fill="cyan",
        anchor="nw",
        activefill="white",
        font=("Terminal", -8),
    ),
    game.canvas2.create_line(
        10, HEIGHT - 10, WIDTH - 10, HEIGHT - 10, fill="cyan"
    ),
]


def deleting_tk_grid():
    Hero.bag = set()
    game.canvas.delete(Hero.tk)
    for case in Grid.all:
        game.canvas.delete(case.tk)
    Grid.path = set()  # better ;) else: infinite loop in map generator


def de_activate():  # ================================ de activate all buttons
    list_button = path_button_1, path_button_2, path_button_3
    for button in list_button:
        button["state"] = "disabled"
        button["background"] = "orange"


def re_activate():  # ================================ re activate all buttons
    list_button = path_button_1, path_button_2, path_button_3
    for button in list_button:
        button["background"] = "cyan"
        button["state"] = "normal"


def restart_grid():
    de_activate()
    deleting_tk_grid()
    x = random.randrange(15, 50)
    y = random.randrange(15, 50)
    item = random.randrange(3, 11)
    Path(x, y, item).by_path_generator()
    game.restart_tk()
    re_activate()


Grid.restart_grid = restart_grid  # <- for restart from Grid.terminated()


def restart_grid_in_square():
    de_activate()
    deleting_tk_grid()
    x = y = 15
    Path(x, y).by_path_generator()
    game.restart_tk()
    re_activate()


def loading_defaut_map():
    de_activate()
    deleting_tk_grid()
    Path().by_load_defaut_map()
    game.restart_tk()
    re_activate()


frame_info = tkinter.Frame(
    game.tk,  # ============================================= log console PRINT
    width=500,
    height=250,
    bg="orange",
)
frame_info.grid(row=1, column=0)
# frame_info.grid_propagate(0) ----------------------> use for force Frame size
V.to_print = tkinter.StringVar()  # --------------------> init string for print
canvas_info = tkinter.Label(
    frame_info,
    bg="black",
    anchor="sw",
    width=99,
    font=("Terminal", -12),
    textvariable=V.to_print,
    justify="left",
    fg="cyan",
)
V.tk_ready = True  # ----------------------------------------> Enable print /!\
canvas_info.grid(row=0, column=0)
V.caneva_update = game.tk.update
print("/////// print in tkinter ignited ///////")
list_canvas_info = []


def init_show_bag():
    global list_canvas_info
    list_canvas_info = []
    x = len(Grid.dic) * 30 / 2
    x = 400 / 2 - x + 6
    for index, name in enumerate(Grid.dic):
        if name == 'start':
            color = 'lightgreen'
        elif 'item' in name:
            color = 'cyan'
        else:
            color = 'red'
        list_canvas_info.append(
            game.canvas2.create_rectangle(
                x + 30 * index,
                300 + 7,
                x + 30 * index + 20,
                300 + 27,
                outline=color
            )
        )
    return None


print("init bag - ", end="")
time.sleep(0.1)
init_show_bag()


def f_canvas_info(old_bag=[None], deja_vu_grid=[None]):
    global list_canvas_info
    if old_bag[0] is None:
        old_bag[0] = set()
    if deja_vu_grid[0] != Grid.dic:  # if game has restart, re-initialize
        for square in list_canvas_info:
            game.canvas2.delete(square)
        init_show_bag()
        for sqr in list_canvas_info:
            game.canvas2.itemconfig(sqr, fill="")
        deja_vu_grid[0] = Grid.dic.copy()
        game.canvas2.itemconfig(list_canvas_info[0], fill="green")
        game.canvas2.update()
        return None
    if Grid.status != [None]:
        game.canvas2.itemconfig(list_canvas_info[-1], fill="red")
    if old_bag[0] == Hero.bag:
        return None  # if nothing change, pass
    for index in range(1, len(Hero.bag) + 1):
        game.canvas2.itemconfig(list_canvas_info[index], fill="white")
    game.canvas2.update()
    old_bag[0] = Hero.bag.copy()
    return None


print("init buttons - ", end="")
time.sleep(0.1)
# button left
path_button_1 = tkinter.Button(
    game.canvas2,
    command=restart_grid,
    disabledforeground="white",
    text="random path",
    background="cyan",
    activebackground="black",
    activeforeground="cyan",
)
game.canvas2.create_window(10, HEIGHT - 60, anchor="nw", window=path_button_1)
# button right
path_button_2 = tkinter.Button(
    game.canvas2,
    command=restart_grid_in_square,
    disabledforeground="white",
    text="15*15 grid",
    background="cyan",
    activebackground="black",
    activeforeground="cyan",
)
game.canvas2.create_window(330, HEIGHT - 60, anchor="nw", window=path_button_2)
# middle button
path_button_3 = tkinter.Button(
    game.canvas2,
    command=loading_defaut_map,
    disabledforeground="white",
    text="load defaut map",
    background="cyan",
    activebackground="black",
    activeforeground="cyan",
)
game.canvas2.create_window(97, HEIGHT - 60, anchor="nw", window=path_button_3)


def verbose_clean():
    if activate_verbose.get():
        return None
    for line in list_text_canvas:
        game.canvas2.itemconfig(line, text="")


print("init check verbose")
time.sleep(0.1)
activate_verbose = tkinter.IntVar()
activate_verbose.set(1)
check_verbose = tkinter.Checkbutton(
    game.canvas2,
    variable=activate_verbose,
    command=verbose_clean,
    text="activate verbose",
    background="cyan",
    activebackground="black",
    activeforeground="cyan",
)
game.canvas2.create_window(202, HEIGHT - 60, anchor="nw", window=check_verbose)


def print_log(intern_var=[[0, 0, 0]]):
    m, limit, old_a = intern_var[0]
    m = m + 1 if m <= limit else 0
    a = []
    all = []

    if activate_verbose.get():

        for i, j in V.a.items():  # all messages to show
            text = str(j[1])  # all text
            all += [str(j[0])] if len(all) < 17 else []  # all increment
            if len(text) > 50:  # if msg > width canvas
                if m > len(text) - 50:  # to stop for 50 loop the msh show
                    a.append(f"{i[:10]: <10} : {text[-50:]:.>50}")
                else:  # to advance the msg
                    a.append(f"{i[:10]: <10} : {text[m:m+50]:.>50}")
            # if msg < width canvas
            else:
                a.append(f"{i[:10]: <10} : {text[-50:]:.>50}")
            limit = max(limit, len(text))  # limit = bigger msg
        for i, j in zip([a[0]] + a[:1:-1], list_text_canvas):
            game.canvas2.itemconfig(j, text=i)
        old_a = a

    else:
        for value in V.a.values():
            all += [str(value[0])] if len(all) < 17 else []  # all increment

    game.canvas2.itemconfig(end_canvas[0], text=" ".join(all))
    # show progress of m
    loop_prog = m / limit * (WIDTH - 20)
    game.canvas2.coords(
        end_canvas[1], 10, HEIGHT - 10, 10 + loop_prog, HEIGHT - 10
    )
    c = "cyan" if m < limit - 50 else "orange"
    game.canvas2.itemconfig(end_canvas[1], fill=c)
    intern_var[0] = m, limit, old_a


print(" ==== starting main loop ==== ")
time.sleep(0.1)
while 1:

    print_log()
    f_canvas_info()
    if Grid.status != [None]:
        Grid.terminated()
    game.run()
    game_py.run(mode_run=2)
