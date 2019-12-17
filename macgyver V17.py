import tkinter
import random
import time
import string


class V:

	def __init__(self, window) :

		self.font = ('Courier', '10')
		self.item = []
		self.i = 0
		self.tk = window.tk
		self.canvas = tkinter.Canvas(self.tk, width=400, height=window.height_window, bg='black')
		self.canvas.grid(row=0,column=1)
		self.canvas.create_text(0,0,text='{:=^50}'.format(' VERBOSE ACTIVATED '),
			fill='green', tag='vendetta', anchor='nw', font = self.font)
		self.tk.update()

	def for_vendetta(self, string, lvl=0) : # clas GRID : 5 '===  '
	
		text = self.canvas.create_text(0,40+self.i*20,text=' {0}. >> {1}'.format(lvl,string),
			fill='green', tag='verbose', anchor='nw', font = self.font)
		line = self.canvas.create_line(
			10, 56 + self.i*20,
			20, 56 + self.i*20, fill = 'cyan' )
		self.item.append( (text, line) )
		self.i += 1
		
	def progress(self, i, lvl) :
	
		coord = self.canvas.coords(self.item[lvl][1])
		coord = coord[0], coord[1], 20 + i*10 , coord[3]
		self.canvas.itemconfig(self.item[lvl][1], coord)
	
class Window:
	"""self.width_window, self.height_window, self.tk, self.canvas"""

	height_window = 400
	width_window = 550

	def __init__(self):
		
		self.tk = tkinter.Tk()
		self.tk.geometry('958x404+0-0')
		self.tk.title("MacGyver's Game")
		self.canvas = tkinter.Canvas(self.tk,
			width  = Window.width_window,
			height = Window.height_window, bg='black')
		self.canvas.grid(row=0,column=0)
		self.tk.update()
			
class Grid:
	""" where the magic happen """
	
	number_case_x = 15 ; number_case_y = 15 # nb of row, column
	DX = Window.width_window // number_case_x
	DY = Window.height_window // number_case_y
	line_X = tuple( "{:0>2}".format(i+1) for i in range(number_case_x) ) # remove tuple and we are in deep
	line_Y = tuple( i for i in string.ascii_uppercase[0:number_case_y] ) # remove tuple and we are in deep
	dict_case = dict_A2_to_12 = {}
	
	def __init__(self, canvas):
		self.canvas = canvas		
		for x, i in enumerate( Grid.line_X ) :
			for y, j in enumerate( Grid.line_Y ) :			
				Grid.dict_case[ x+1,y+1 ] = Case( canvas, (x+1,y+1) , j+i )
				Grid.dict_A2_to_12[ j+i ] = x+1,y+1
		
	def coord_str_To_int(coord): # "A02" >> (1,2)
		return dict_A2_to_12.get([coord])
		
	def coord_int_To_str(coord): # (1,2) >> "A02" """
		return dict_case.get([coord]).name
		
	def adjust_coord_for_Canvas(pos): # (1,2) >> 12,25 """
		return(	( pos[0]-1 ) * (Grid.DX) ,
				( pos[1]-1 ) * (Grid.DY) )

	def check_point_in_grid(pos) : # is (1,2) in grid of the game ? (True or False)
		return(	( pos[0] >= 1 and pos[0] <= Grid.number_case_x ) and
				( pos[1] >= 1 and pos[1] <= Grid.number_case_y ) )

class Case:

	def __init__(self,canvas,pos, name) :
		
		self.canvas = canvas		# main canvas appartenance
		self.pos = pos				# ex : (3,2) , (14,5) , ......
		self.color = "blue"			# as you wish ....
		self.name = name			# B05, E14
		self.id = canvas.create_rectangle( self.f_coord_case(self.pos), fill=self.color, tag = "free" )

	def f_coord_case(self, pos=False) :
	
		if pos == False : pos = self # this is shame ...
		x1, y1 = Grid.adjust_coord_for_Canvas(pos)
		deltaX =  - 2 + Grid.DX
		deltaY =  - 2 + Grid.DY
		return x1, y1, x1 + deltaX, y1 + deltaY

		
class Path_generator:

	Path_set = set()

	def __init__(self, grid, canvas, mode=1) :
	
		self.mode = mode
		self.canvas = canvas
		self.grid = grid
		self.start = self.middle = self.finish = (0,0)
		self.path	= []
		if	 mode == 1 : self.way_one()
		"""
		elif mode == 2 : way_two()
		elif mode == 3 : way_three()
		else : print('error in __init__') """

	def way_one(self) :
	
		x = random.randrange(self.grid.number_case_x) + 1
		y = random.randrange(self.grid.number_case_y) + 1
		
		self.start = actual_position = old_position = (x, y)
		self.path.append( self.start )
		self.canvas.itemconfig( self.grid.dict_case[ self.start ].id, fill='yellow')
		road_finish = goal_middle_placed = False
		i_some_path = 0
		
		while road_finish != True :
		
			x, y = actual_position[0], actual_position[1]
			future_position = [
			( x + 1 , y + 0 ) , # 		[X]
			( x - 1 , y + 0 ) , # 	[X] [O]	[X]
			( x + 0 , y + 1 ) , # 		[X]
			( x + 0 , y - 1 ) ] # 	[0] actual_position

			future_position = [ i for i in future_position if not i in self.path ]
			future_position = [ i for i in future_position if Grid.check_point_in_grid(i) ]

			if future_position == [] :
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
	
	def way_two(self) :
		"""
		generate obstacles,
		per group of 2*2, 3*3, or even more,
		and if possible, link to the size of the grid
		"""
		pass
		
	def way_three(self) :
		"""
		the system check if possible to subdivise in 3*3 the gird,
		and we generate 3*3 case gard
		
		 - - - 		 - - -		 - - -
		|X| |X|		|X| |X|		|X| |X|
		 - - - 		 - - -		 - - -
		|X| | |		| | | |		| | | |
		 - - - 		 - - -		 - - -
		|X|X|X|		|X|X|X|		|X| |X|
		 - - - 		 - - -		 - - -
		
		"""
		pass
		
	def way_four(self):
		"""
		genere un path, check sa longueur, et une fois fois assez grand, le place dans la grille
		"""
		pass
		
	def way_five(self):
		"""
		use a file
		"""

class MacGyver:

	def __init__(self, canvas, start):
	
		self.BackPack = False
		self.canvas = canvas
		self.id = canvas.create_rectangle( Case.f_coord_case(start), fill="orange")	
		self.x = self.y = 0
		
		canvas.bind_all('<KeyPress-Left>', 	self.move_left)
		canvas.bind_all('<KeyPress-Right>', self.move_right)
		canvas.bind_all('<KeyPress-Up>', 	self.move_up)
		canvas.bind_all('<KeyPress-Down>', 	self.move_down)
	
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
		future_pos = (	pos[0] + self.x, pos[1] + self.y,
						pos[2] + self.x, pos[3] + self.y)
		if not {future_pos} & Path_generator.Path_set == {future_pos}: self.x = self.y = 0

	def move_left(self, event):
		if not self.canvas.coords(self.id)[0] <= 0:
			self.x = - Grid.DX ; self.check_path()

	def move_right(self, event):
		if not self.canvas.coords(self.id)[2] >= Window.width_window - Grid.DX:
			self.x = Grid.DX ; self.check_path()
		
	def move_down(self, event):
		if not self.canvas.coords(self.id)[3] >= Window.height_window - Grid.DY:
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
		self.canvas_height = Window.height_window
		self.canvas_width = Window.width_window
		self.is_hitting_bottom = False
		canvas.move(self.id, 245, 100)
		
	def draw(self):
	
		self.canvas.move(self.id, self.x, self.y)
		
		pos = self.canvas.coords(self.id) #wall collision
		if pos[1] <= 0:	self.y = 1
		if pos[0] <= 0:	self.x = 3
		if pos[3] >= self.canvas_height//15*15:	self.y = -1
		if pos[2] >= self.canvas_width//15*15:	self.x = -3
			
		paddle_pos = self.canvas.coords(self.paddle.id)		 #Macgyver collision
		if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
			if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]: #top
				self.y = -3 ; self.hit += 1
			if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]: #bottom
				self.y = 3  ; self.hit += 1
		elif pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
			if pos[2] >= paddle_pos[0] and pos[2] <= paddle_pos[2]: #left
				self.x = -3 ; self.hit += 1
			if pos[0] >= paddle_pos[0] and pos[0] <= paddle_pos[2]: #right
				self.x = 3  ; self.hit += 1
			
def main():
	
	window = Window()
	
	v = V(window)
	grid = Grid(window.canvas)
	path = Path_generator(grid, window.canvas)

	macgyver 	= MacGyver(		window.canvas, path.start)
	middle_goal = Middle_goal(	window.canvas, path.middle)
	final_goal	= Final_goal(	window.canvas, path.finish)
	ball		= Ball(window.canvas, macgyver)
	
	if True: # if you want to write the path and some info
		date = time.strftime("map/%Y%m%d_%H%M%S_") + str(time.time())[-6:] + ".txt"
		file = open(date, 'w+')
		file.write(date+"\n\n")
		file.write(str(["start : ",path.start,", middle : ", path.middle,", finish : ", path.finish]))
		file.write("\n\n")
		for y in range(1,16):
			for x in range(1,16):
				if		(x,y) == path.start		: file.write("|S")
				elif	(x,y) == path.middle	: file.write("|O")
				elif	(x,y) == path.finish	: file.write("|X")
				elif 	(x,y) in path.path		: file.write("| ")
				elif	(x,y) not in path.path	: file.write("|#")
				else: file.write("|E") # >>> Error somewhere
			file.write("|\n")
		file.write("\n")
		file.write(str(path.path))
		file.close()
	
	while macgyver.draw():
		
		ball.draw()
		macgyver.draw()
		
		window.tk.update_idletasks()
		window.tk.update()
		time.sleep(0.01)
		
		
		
		
if __name__ == '__main__':
	main()

# ---------------------------------------------------------------------------- #
# 							 END OF FILE 									   #
# ---------------------------------------------------------------------------- #