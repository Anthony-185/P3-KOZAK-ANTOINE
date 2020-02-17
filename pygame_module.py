import pygame
from pygame.locals import *
from grid_module import *

# ___________________________________________________________________________ #
# [X] Bug: if one key maintain pressed and pressing others, doing mayhem !
# [X] venv requirement.txt
# [X] load png.files
# [X] doc pdf
# [ ] images must be simple (a global dic, or a class)
# [ ] mayhem actually
# ___________________________________________________________________________ #


# /  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
EXTEND = __name__ == "__main__"
# /  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //

size = (80, 60)
small_size = (48, 36)

LIST_IMAGE = [
    "MacGyver.png",
    "Gardien.png",
    "aiguille.png",
    "tube_plastique.png",
    "ether.png",
    "seringue.png",
    "floor-tiles-20x20.png",
]
PATH = "images/"
for i, j in enumerate(LIST_IMAGE):
    LIST_IMAGE[i] = PATH + j
LIST_IMAGE = iter(LIST_IMAGE)

MACG_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
MACG_IMG = pygame.transform.scale(MACG_IMG, size)

GOAL_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
GOAL_IMG = pygame.transform.scale(GOAL_IMG, size)

IT_1_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
IT_1_IMG = pygame.transform.scale(IT_1_IMG, size)

IT_2_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
IT_2_IMG = pygame.transform.scale(IT_2_IMG, size)

IT_3_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
IT_3_IMG = pygame.transform.scale(IT_3_IMG, size)

IT_4_IMG = pygame.image.load(next(LIST_IMAGE))  # ok
IT_4_IMG = pygame.transform.scale(IT_4_IMG, size)

WALL_IMG_ORIGINAL = pygame.image.load(next(LIST_IMAGE))  # ok
WALL_IMG = WALL_IMG_ORIGINAL.subsurface((0, 0, 20, 20))
WALL_IMG = pygame.transform.scale(WALL_IMG, size)

PATH_IMG_ORIGINAL = WALL_IMG_ORIGINAL
PATH_IMG = PATH_IMG_ORIGINAL.subsurface((20, 20, 20, 20))
PATH_IMG = pygame.transform.scale(PATH_IMG, size)


def f_a_WALL_IMG(y=[0], x=[0], change=False):
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

    global WALL_IMG
    WALL_IMG = PATH_IMG_ORIGINAL.subsurface(
        (random.choice(x[0]) * 20, y[0] * 20, 20, 20)
    )
    WALL_IMG = pygame.transform.scale(WALL_IMG, size)


f_a_WALL_IMG()


def f_a_PATH_IMG(x=[0], change=False):
    """ return a pygame image cropped from original floor-tiles-20x20.png """
    possibility = [range(0, 3), range(3, 6), range(6, 9)]
    y = 12
    if x == [0] or change:
        x[0] = random.choice(possibility)

    global PATH_IMG
    PATH_IMG = WALL_IMG_ORIGINAL.subsurface(
        (random.choice(x[0]) * 20, y * 20, 20, 20)
    )
    PATH_IMG = pygame.transform.scale(PATH_IMG, size)


f_a_PATH_IMG()


WHITE, BLACK, RED, BLUE = (255,) * 3, (0,) * 3, (255, 0, 0), (0, 0, 255)


class Py_game_1:
    """ class to run a pygame instance of the game """

    row = column = 0
    RESOLUTION = (400, 300)
    if EXTEND:
        BIG = (800, 300)
    else:
        BIG = RESOLUTION

    @V.for_vendetta
    def __init__(self, mode=0):
        """ init pygame """
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

    def grid_15_per_15(self, x, y):
        """ return 5 * 5 cases around x, y """
        x_list = range(x - 2, x + 3)
        y_list = range(y - 2, y + 3)
        return [(i, j) for i in x_list for j in y_list]

    @V.for_vendetta
    def handleEvents(self):
        """ only handle quit pygame, not working well... """
        list_event = pygame.event.get()
        for event in list_event:
            if event.type == QUIT:
                pygame.quit()
                quit()
        return list_event

    @V.for_vendetta
    def key_pressed(self, hold=[[]]):
        """ hold is here to prevent multi case deplacement
            it's a list so it can be keep in memory inside the function """
        pressed_keys = pygame.key.get_pressed()
        if not hold[0] == pressed_keys:
            if pressed_keys[K_LEFT]:
                Hero.move((-1, 0))
            elif pressed_keys[K_RIGHT]:
                Hero.move((+1, 0))
            elif pressed_keys[K_UP]:
                Hero.move((0, -1))
            elif pressed_keys[K_DOWN]:
                Hero.move((0, +1))
        hold.pop()
        hold.append(pressed_keys)
        return pressed_keys

    @V.for_vendetta
    def update_screen(self, deja_vu=[0], mode=0):
        """ draw all objects,
        can draw a grid, or macgyver with 5*5 cases around him 
        deja_vu pass the function if nothing change,
        mode 0 : draw like pygame_module (the two modes are print) 
        mode 1 : draw the entire grid
        mode 2 : draw macgiver with the 5*5 case around him """
        if deja_vu[0] == [Grid.dic, Hero.pos]:
            return None
        self.screen.fill(BLACK)
        if mode != 2:
            for pos in Grid.all:
                color = (128, 128, 128)
                if pos in Grid.object:
                    color = WHITE
                elif pos in Grid.path:
                    color = (50, 50, 255)
                if pos == Hero.pos:
                    color = (255, 140, 0)
                elif pos == Grid.dic["final_goal"]:
                    color = RED
                elif pos == Grid.dic["start"]:
                    color = (0, 255, 0)
                self.draw(pos[0] - 1, pos[1] - 1, color)
        # ====================================================================
        #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
        # ====================================================================
        if mode == 1:
            return None
        list_pos = self.grid_15_per_15(0, 0)
        for pos, real_pos in zip(self.grid_15_per_15(*Hero.pos), list_pos):
            f_a_WALL_IMG()
            img = WALL_IMG
            color = (128, 128, 128)
            if pos in Grid.object:
                color = WHITE
                if pos == Grid.dic["item_1"]:
                    img = IT_1_IMG
                elif pos == Grid.dic["item_2"]:
                    img = IT_2_IMG
                elif pos == Grid.dic["item_3"]:
                    img = IT_3_IMG
                else:
                    img = IT_4_IMG
            elif pos in Grid.path:
                color = (50, 50, 255)
                f_a_PATH_IMG()
                img = PATH_IMG
            if pos == Hero.pos:
                color = (255, 140, 0)
                img = MACG_IMG
            elif pos == Grid.dic["final_goal"]:
                color = RED
                img = GOAL_IMG
            elif pos == Grid.dic["start"]:
                color = (0, 255, 0)
                img = PATH_IMG_ORIGINAL.subsurface((80, 100, 20, 20))
                img = pygame.transform.scale(img, size)
            self.draw(real_pos[0] - 1, real_pos[1] - 1, color, c=2, mode=mode)
            self.screen.blit(
                img,
                self.draw(real_pos[0] - 1, real_pos[1] - 1, c=3, mode=mode),
            )

        pygame.display.flip()
        deja_vu[0] = [Grid.dic.copy(), Hero.pos]
        return None

    # ========================================================================
    #   //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
    # ========================================================================

    @V.for_vendetta
    def draw(self, x, y, color=(0, 0, 0), c=1, mode=0):  # ------------> add c
        """ just draw a rectangle, take x, y, and color
            it's x - 1 and y - 1 already converted ! 
            c: where to draw
            mode: only if two screen activated """

        x_align = 640 if mode != 2 else 240
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
        in case of restarting game, REDefine the variables which
        defines x and y alinement (purely graphics adjustement) """
        if old_grid[0] != Grid.dic.copy():
            f_a_PATH_IMG(change=True)
            f_a_WALL_IMG(change=True)
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

    @V.for_vendetta
    def run(self, mode_run=3):
        """ main function of the game,
            run everything in game """
        self.key_pressed()
        self.handleEvents()
        if mode_run == 4:
            self.update_screen()
        else:
            self.update_screen(mode=mode_run)
        self.check_secure()


if __name__ == "__main__":

    Path().by_load_defaut_map()
    Hero.pos = Grid.dic["start"]
    game = Py_game_1()
    while 1:
        game.run()
        if Grid.status != [None]:
            Grid.terminated()
