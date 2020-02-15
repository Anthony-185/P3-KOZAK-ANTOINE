import pygame
from pygame.locals import *
from grid_module import *

# ___________________________________________________________________________ #
# [X] Bug: if one key maintain pressed and pressing others, doing mayhem !
# [X] venv requirement.txt
# [X] load png.files
# [X] doc pdf
# ___________________________________________________________________________ #


# /  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
if __name__ == "__main__":
    extend = True
else:
    extend = False

size = (80, 60)
small_size = (48, 36)

l = [
    "MacGyver.png",
    "Gardien.png",
    "aiguille.png",
    "tube_plastique.png",
    "ether.png",
    "seringue.png",
    "floor-tiles-20x20.png",
]
path = "images/"
for i, j in enumerate(l):
    l[i] = path + j
l = iter(l)

macg_img = pygame.image.load(next(l))  # ok
macg_img = pygame.transform.scale(macg_img, size)

goal_img = pygame.image.load(next(l))  # ok
goal_img = pygame.transform.scale(goal_img, size)

it_1_img = pygame.image.load(next(l))  # ok
it_1_img = pygame.transform.scale(it_1_img, size)

it_2_img = pygame.image.load(next(l))  # ok
it_2_img = pygame.transform.scale(it_2_img, size)

it_3_img = pygame.image.load(next(l))  # ok
it_3_img = pygame.transform.scale(it_3_img, size)

it_4_img = pygame.image.load(next(l))  # ok
it_4_img = pygame.transform.scale(it_4_img, size)

wall_img_original = pygame.image.load(next(l))  # ok
wall_img = wall_img_original.subsurface((0, 0, 20, 20))
wall_img = pygame.transform.scale(wall_img, size)

path_img_original = wall_img_original
path_img = path_img_original.subsurface((20, 20, 20, 20))
path_img = pygame.transform.scale(path_img, size)


def f_a_wall_img(y=[0], x=[0], change=False):
    """ return a pygame image cropped from original floor-tiles-20x20.png """
    possibility = [
        [range(5, 11), range(12, 18)],
        [range(0, 4)],
        [range(0, 4)],
        [range(0, 4)],
        [range(0, 4)],
        [range(0, 4), range(8, 14), range(14, 20)],
    ]
    if x == [0] or change:
        y[0] = random.randrange(len(possibility) - 1)
        x[0] = random.choice(possibility[y[0]])

    global wall_img
    wall_img = path_img_original.subsurface(
        (random.choice(x[0]) * 20, y[0] * 20, 20, 20)
    )
    wall_img = pygame.transform.scale(wall_img, size)


f_a_wall_img()


def f_a_path_img(x=[0], change=False):
    """ return a pygame image cropped from original floor-tiles-20x20.png """
    possibility = [range(0, 3), range(3, 6), range(6, 9)]
    y = 12
    if x == [0] or change:
        x[0] = random.choice(possibility)

    global path_img
    path_img = wall_img_original.subsurface(
        (random.choice(x[0]) * 20, y * 20, 20, 20)
    )
    path_img = pygame.transform.scale(path_img, size)


f_a_path_img()


white, black, red, blue = (255,) * 3, (0,) * 3, (255, 0, 0), (0, 0, 255)


class Py_game_1:
    row = column = 0
    RESOLUTION = (400, 300)
    if extend:
        BIG = (800, 300)
    else:
        BIG = RESOLUTION

    @V.for_vendetta
    def __init__(self, mode=0):
        self.DX = Py_game_1.RESOLUTION[0] // Grid.row
        self.DY = Py_game_1.RESOLUTION[1] // Grid.column
        self.CX = Py_game_1.RESOLUTION[0] % Grid.row // 2  # -----+
        self.CY = (
            Py_game_1.RESOLUTION[1] % Grid.column // 2
        )  # --+------> removing marge
        Py_game_1.row, Py_game_1.column = Grid.row, Grid.column
        pygame.init()  # Pygame init =======
        self.screen = pygame.display.set_mode(Py_game_1.BIG)
        self.clock = pygame.time.Clock()
        self.update_screen(mode=mode)
        Grid.pygame_mode = mode

    def move_img_mac(self, x, y, old_pos=[0, 0]):
        pos = old_pos[0] + x, old_pos[1] + y
        if (x != 0) or (y != 0):
            print(pos)
        self.screen.blit(macg_img, pos)
        old_pos[0] = pos[0]
        old_pos[1] = pos[1]

    def grid_15_per_15(self, x, y):
        return [
            (i, j) for i in range(x - 2, x + 3) for j in range(y - 2, y + 3)
        ]

    @V.for_vendetta
    def handleEvents(self):
        """ only handle quit pygame, not working well... """
        List_event = pygame.event.get()
        for event in List_event:
            if event.type == QUIT:
                pygame.quit()
                quit()
        return List_event

    @V.for_vendetta
    def key_pressed(self, hold=[[]]):
        """ hold is here to prevent multi case deplacement
            it's a list so it can be keep in memory inside the function """
        pressed_keys = pygame.key.get_pressed()
        if not hold[0] == pressed_keys:
            if pressed_keys[K_LEFT]:
                Hero.move((-1, 0))  # ; self.move_img_mac(-1, 0)
            elif pressed_keys[K_RIGHT]:
                Hero.move((+1, 0))  # ; self.move_img_mac(+1, 0)
            elif pressed_keys[K_UP]:
                Hero.move((0, -1))  # ; self.move_img_mac(0, -1)
            elif pressed_keys[K_DOWN]:
                Hero.move((0, +1))  # ; self.move_img_mac(0, +1)
        hold.pop()
        hold.append(pressed_keys)
        return pressed_keys

    @V.for_vendetta
    def update_screen(self, deja_vu=[0], mode=0):
        """ draw all objects """
        if deja_vu[0] == [Grid.dic, Hero.pos]:
            return None
        self.screen.fill(black)
        if mode != 2:
            for pos in Grid.all:
                color = (128, 128, 128)
                if pos in Grid.object:
                    color = white
                elif pos in Grid.path:
                    color = (50, 50, 255)
                if pos == Hero.pos:
                    color = (255, 140, 0)
                elif pos == Grid.dic["final_goal"]:
                    color = red
                elif pos == Grid.dic["start"]:
                    color = (0, 255, 0)
                self.draw(pos[0] - 1, pos[1] - 1, color)
        # ====================================================================
        #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
        # ====================================================================
        if mode == 1:
            return
        # self.move_img_mac(0, 0)
        list_pos = self.grid_15_per_15(0, 0)
        for pos, real_pos in zip(self.grid_15_per_15(*Hero.pos), list_pos):
            f_a_wall_img()
            img = wall_img
            color = (128, 128, 128)
            if pos in Grid.object:
                color = white
                if pos == Grid.dic["item_1"]:
                    img = it_1_img
                elif pos == Grid.dic["item_2"]:
                    img = it_2_img
                elif pos == Grid.dic["item_3"]:
                    img = it_3_img
                else:
                    img = it_4_img
            elif pos in Grid.path:
                color = (50, 50, 255)
                f_a_path_img()
                img = path_img
            if pos == Hero.pos:
                color = (255, 140, 0)
                img = macg_img
            elif pos == Grid.dic["final_goal"]:
                color = red
                img = goal_img
            elif pos == Grid.dic["start"]:
                color = (0, 255, 0)
                img = path_img_original.subsurface((80, 100, 20, 20))
                img = pygame.transform.scale(img, size)
            self.draw(real_pos[0] - 1, real_pos[1] - 1, color, c=2, mode=mode)
            self.screen.blit(
                img,
                self.draw(real_pos[0] - 1, real_pos[1] - 1, c=3, mode=mode),
            )

        pygame.display.flip()
        deja_vu[0] = [Grid.dic.copy(), Hero.pos]

    # ========================================================================
    #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
    # ========================================================================

    @V.for_vendetta
    def draw(self, x, y, color=(0, 0, 0), c=1, mode=0):  # ------------> add c
        """ just draw a rectangle, take x, y, and color 
            it's x - 1 and y - 1 already converted /!\ """
        if mode != 2:
            x_align = 640
            y_align = 180
        else:
            x_align = 240
            y_align = 180
        if c == 1:  # to draw in left area
            pos = (
                x * self.DX + self.CX + 1,
                y * self.DY + self.CY + 1,
                self.DX - 2,
                self.DY - 2,
            )
        elif c == 2:  # to draw in right area
            pos = (x * 80 + x_align, y * 60 + y_align, 80, 60)
        elif c == 3:  # used as a calcul function, return c = 2 position
            return (x * 80 + x_align, y * 60 + y_align, 80, 60)
        pygame.draw.rect(self.screen, color, pos)

    @V.for_vendetta
    def check_secure(self, old_grid=[None]):
        """
        in case of restarting game, redefine the variables which
        defines x and y alinement (purely graphics adjustement) """
        if old_grid[0] != Grid.dic.copy():
            f_a_path_img(change=True)
            f_a_wall_img(change=True)
            old_grid[0] = Grid.dic.copy()
            self.update_screen(deja_vu=[False], mode=Grid.pygame_mode)
        if Py_game_1.row == Grid.row and Py_game_1.column == Grid.column:
            return None  # must be fast if all ok
        else:
            self.DX = Py_game_1.RESOLUTION[0] // Grid.row
            self.DY = Py_game_1.RESOLUTION[1] // Grid.column
            self.CX = Py_game_1.RESOLUTION[0] % Grid.row // 2  # -----+
            self.CY = (
                Py_game_1.RESOLUTION[1] % Grid.column // 2
            )  # --+------> removing marge
            # f_a_wall_img(change = True)

    @V.for_vendetta
    def run(self, mode_run=3):
        """ main function of the game,
            run everything in game """
        self.key_pressed()
        self.handleEvents()
        # self.update_screen2()
        if mode_run == 4:
            self.update_screen()
        else:
            self.update_screen(mode=mode_run)
        # self.clock.tick(60)
        self.check_secure()


if __name__ == "__main__":

    # Path(25,25).by_path_generator()
    Path().by_load_defaut_map()
    Hero.pos = Grid.dic["start"]
    game = Py_game_1()
    #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
    #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
    while 1:
        game.run()
        if Grid.status != [None]:
            Grid.terminated()
