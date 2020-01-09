import tkinter
import random
import time
import string
    
COLUMN = 15 ; ROW = 15



"""
class Trace(object):

    def __init__(self, f):
        self.f =f

    def __call__(self, *args, **kwargs):
        print("entering function " + self.f.__name__)
        i=0
        for arg in args:
            print("arg {0}: {1}".format(i, arg) )
            i =i+1
            
        return self.f(*args, **kwargs)
"""		

		
class Window:
    """self.WIDTH, self.HEIGHT, self.tk, self.canvas"""

    HEIGHT = 400
    WIDTH = 550

    # @Trace
    def __init__(self):
        
        self.tk = tkinter.Tk()
        self.tk.geometry('958x404+0-0')
        self.tk.title("MacGyver's Game")
        self.canvas = tkinter.Canvas(self.tk,
            width  = Window.WIDTH,
            height = Window.HEIGHT, bg='black')
        self.canvas.grid(row=0,column=0)
        self.tk.update()

# ___________________________________________________________________________ #
class Grid:
    """ where the magic happen """
    
    COLUMN = 15 ; ROW = 15
    # some value for a good screen
    DX = Window.WIDTH // COLUMN ; DY = Window.HEIGHT // ROW

    dict_case = dict_A2_to_12 = {}
    
    def __init__(self, canvas):
        self.canvas = canvas        
        for x, i in enumerate( (f"{i:0>2}" for i in range(0, COLUMN +1) )):
            for y, j in enumerate( string.ascii_uppercase[:ROW] ) : 
                Grid.dict_case[ x+1,y+1 ] = Case( canvas, (x+1,y+1) , j+i )
                Grid.dict_A2_to_12[ j+i ] = x+1,y+1
        
    def coord_str_To_int(coord): # "A02" >> (1,2)
        return dict_A2_to_12.get([coord])
        
    def coord_int_To_str(coord): # (1,2) >> "A02" """
        return dict_case.get([coord]).name
        
    def adjust_coord_for_Canvas(pos): # (1,2) >> 12,25 """
        return( ( pos[0]-1 ) * (Grid.DX) ,
                ( pos[1]-1 ) * (Grid.DY) )

    def check_point_in_grid(pos) : # is (1,2) in grid of the game ?
        return( ( pos[0] >= 1 and pos[0] <= Grid.COLUMN ) and
                ( pos[1] >= 1 and pos[1] <= Grid.ROW ) )

class Case:

    def __init__(self,canvas,pos, name) :
        
        self.name = name            # B05, E14
        self.id = canvas.create_rectangle(
            self.f_coord_case(pos), fill="blue", tag = "free" )

    def f_coord_case(self, pos=False) :
    
        if pos == False : pos = self # this is shame ...
        x1, y1 = Grid.adjust_coord_for_Canvas(pos)
        return x1, y1, x1-2 + Grid.DX, y1-2 + Grid.DY


class Path_generator:

    Path_set = set()

    def __init__(self, grid, canvas, mode=1) :
    
        self.mode = mode
        self.canvas = canvas
        self.grid = grid
        self.start = self.middle = self.finish = (0,0)
        self.path   = []
        if   mode == 1 : self.way_one()

    def way_one(self) :
    
        x = random.randrange(self.grid.COLUMN) + 1
        y = random.randrange(self.grid.ROW) + 1
        
        self.start = actual_position = (x, y)
        self.path.append( self.start )
        self.canvas.itemconfig( self.grid.dict_case[ self.start ].id, fill='yellow')
        road_finish = goal_middle_placed = False
        i_some_path = 0
        
        while not road_finish :
        
            x, y = actual_position[0], actual_position[1]
            future_position = [
            ( x + 1 , y + 0 ) , #       [X]
            ( x - 1 , y + 0 ) , #   [X] [O] [X]
            ( x + 0 , y + 1 ) , #       [X]
            ( x + 0 , y - 1 ) ] #   [0] actual_position

            future_position = [ i for i in future_position if not i in self.path ]
            future_position = [ i for i in future_position if Grid.check_point_in_grid(i) ]

            if not future_position :
                actual_position = random.choice(self.path)
                continue

            actual_position = random.choice(future_position)
            self.path.append(actual_position)
            self.canvas.itemconfig( Grid.dict_case[ actual_position ].id, fill='maroon')            
            i_some_path += 1
            if i_some_path > 50 and random.randrange(100) > 70 : # to create some path              
                if not goal_middle_placed :                     
                    goal_middle_placed = True
                    self.middle = actual_position
                else:
                    road_finish = True
                    self.finish = actual_position
        
        self.canvas.itemconfig( Grid.dict_case[ self.middle ].id, tag="middle_goal", fill='darkgreen')
        self.canvas.itemconfig( Grid.dict_case[ self.finish ].id, tag="finish_goal", fill='red')
        Path_generator.Path_set = set( 
            tuple(
                self.canvas.coords( 
                    Grid.dict_case[ i ].id ) ) for i in self.path ) # horrible
    

class MacGyver:

    def __init__(self, canvas, start):
    
        self.BackPack = False
        self.canvas = canvas
        self.id = canvas.create_rectangle( Case.f_coord_case(start), fill="orange") 
        self.x = self.y = 0
        
        canvas.bind_all('<KeyPress-Left>',  self.move_left)
        canvas.bind_all('<KeyPress-Right>', self.move_right)
        canvas.bind_all('<KeyPress-Up>',    self.move_up)
        canvas.bind_all('<KeyPress-Down>',  self.move_down)
    
    def draw(self):
    
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        self.x = self.y = 0
        if pos == self.canvas.coords('middle_goal') : self.BackPack = True
        if pos == self.canvas.coords('finish_goal') :
            if self.BackPack: 
                print("Win !")
                return False
            else :
                print("Game over")
                return False
        return True
            
    def check_path(self):
        pos = self.canvas.coords(self.id)
        future_pos = (  pos[0] + self.x, pos[1] + self.y,
                        pos[2] + self.x, pos[3] + self.y)
        if future_pos not in Path_generator.Path_set: self.x = self.y = 0

    def move_left(self, event):
        if not self.canvas.coords(self.id)[0] <= 0:
            self.x = - Grid.DX ; self.check_path()

    def move_right(self, event):
        if not self.canvas.coords(self.id)[2] >= Window.WIDTH - Grid.DX:
            self.x = Grid.DX ; self.check_path()
        
    def move_down(self, event):
        if not self.canvas.coords(self.id)[3] >= Window.HEIGHT - Grid.DY:
            self.y = Grid.DY ; self.check_path()
    
    def move_up(self, event):
        if not self.canvas.coords(self.id)[1] <= 0:
            self.y = - Grid.DY ; self.check_path()

class Middle_goal:

    def __init__(self, canvas, pos):
    
        self.taken = False
        self.pos = pos
        self.canvas = canvas
        coord = Grid.adjust_coord_for_Canvas(pos)
        coord = (
            coord[0] + Grid.DX / 2,
            coord[1] + Grid.DY / 2)
        self.id = canvas.create_text(coord,
            text = "X", fill='white', anchor = 'center', font=('Courier', '30'))
        


class Final_goal:

    def __init__(self, canvas, pos):

        self.pos = pos
        self.canvas = canvas
        coord = Grid.adjust_coord_for_Canvas(pos)
        coord = (
            coord[0] + Grid.DX / 2,
            coord[1] + Grid.DY / 2)
        self.id = canvas.create_text(coord,
            text = "X", fill='black', anchor = 'center', font=('Courier', '30'))


class Ball:

    def __init__(self, canvas, paddle):
    
        self.hit = 0
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill='yellow')
        self.x = random.choice( [-3, -2, -1, 1, 2, 3] )
        self.y = -3
        self.canvas_height = Window.HEIGHT
        self.canvas_width = Window.WIDTH
        self.is_hitting_bottom = False
        canvas.move(self.id, 245, 100)
        
    def draw(self):
    
        self.canvas.move(self.id, self.x, self.y)
        
        pos = self.canvas.coords(self.id) #wall collision
        if pos[1] <= 0: self.y = 1
        if pos[0] <= 0: self.x = 3
        if pos[3] >= self.canvas_height//15*15: self.y = -1
        if pos[2] >= self.canvas_width//15*15:  self.x = -3
            
        paddle_pos = self.canvas.coords(self.paddle.id)      #Macgyver collision
        if   pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if   pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]: #top
                self.y = -3 ; self.hit += 1
            elif pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]: #bottom
                self.y = 3  ; self.hit += 1
        elif pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
            if   pos[2] >= paddle_pos[0] and pos[2] <= paddle_pos[2]: #left
                self.x = -3 ; self.hit += 1
            elif pos[0] >= paddle_pos[0] and pos[0] <= paddle_pos[2]: #right
                self.x = 3  ; self.hit += 1

def write_in_file(path):
    date = time.strftime("map/%Y%m%d_%H%M%S_") + str(time.time())[-6:] + ".txt"
    file = open(date, 'w+')
    file.write(date+"\n\n")
    file.write(str(["start : ",path.start,", middle : ", path.middle,", finish : ", path.finish]))
    file.write("\n\n")
    for y in range(1,16):
        for x in range(1,16):
            if      (x,y) == path.start     : file.write("|S")
            elif    (x,y) == path.middle    : file.write("|O")
            elif    (x,y) == path.finish    : file.write("|X")
            elif    (x,y) in path.path      : file.write("| ")
            elif    (x,y) not in path.path  : file.write("|#")
            else: file.write("|E") # >>> Error somewhere
        file.write("|\n")
    file.write("\n")
    file.write(str(path.path))
    file.close()

def main():
    
    window = Window()
    
    grid = Grid(window.canvas)
    path = Path_generator(grid, window.canvas)

    macgyver    = MacGyver(     window.canvas, path.start)
    middle_goal = Middle_goal(  window.canvas, path.middle)
    final_goal  = Final_goal(   window.canvas, path.finish)
    ball        = Ball(window.canvas, macgyver)
    if True: write_in_file(path)
    
    while macgyver.draw():
        
        ball.draw()
        macgyver.draw()
        
        window.tk.update_idletasks()
        window.tk.update()
        time.sleep(0.01)
        
        
if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------- #
#                            END OF FILE                                      #
# --------------------------------------------------------------------------- #