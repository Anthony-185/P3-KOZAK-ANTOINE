""" _______________________________________________
# /!\ don't actually work, it's a prototype !!!!!!!
________________________________________________"""
import tkinter
import random
import time
import string



class V:

	def __init__(self) :

		self.i_verbose = 0
		self.tk = tkinter.Tk()
		self.tk.title('game')
		self.canvas = tkinter.Canvas(self.tk, width=400, height=280, bd=0, bg='black', highlightthickness=0)
		self.canvas.pack()
		self.canvas.create_text(40,40,text='===  VERBOSE  ACTIVATED  ===', fill='green', tag='vendetta')
		self.tk.update()
				
	def for_vendetta(self, string, lvl=0) : # clas GRID : 5 '===  '
	
		self.canvas.create_text(40,80+self.i*40,text='{0}.{1}'.format(lvl,string), fill='green', tag='verbose')
		self.i += 1
		
	
class Window:
	"""self.width_window, self.height_window, self.tk, self.canvas"""

	def __init__(self):
	
		self.width_window = 550
		self.height_window = 400
		
		self.tk = Tk()
		self.tk.title("MacGyver's Game")
		
		self.canvas = tkinter.Canvas(
			self.tk, 
			width=width_window,
			height=height_window, 
			bg='black',
			highlightthickness=0)

		self.canvas.pack()
		self.tk.update()


class Grid:


	def __init__(self, canvas):

		self.number_case_x = 15 # number of line
		self.number_case_y = 15 # number of column
		self.canvas = canvas
		
		self.line_X = ( f"{i+1:0>2}" for i in range(number_case_x) )
		self.line_Y = ( i for i in string.ascii_uppercase[0:number_case_y] )
		
		self.dict_case = {}
		self.dict_str_to_int = {}
		
		for x, i in enumerate( self.line_X ) :
			for y, j in enumerate ( self.line_Y ) :
			
				self.dict_case[ x+1,y+1 ] = Case( canvas, (x+1,y+1) , j+i )
				self.dict_A2_to_12[ j+i ] = x+1,y+1
			
	def coord_str_To_int(self, coord):
		""" "A02" >> (1,2) """
	
		a = self.dict_A2_to_12.get([coord])
		if a : return a
		else : print('error in convert str to int')
		
	def coord_int_To_str(self, coord):
		""" (1,2) >> "A02" """
		
		for i,j in self.dict_A2_to_12.items() :
			if j == coord : return i
		else : print('error in convert int to str')

		
	def adjust_coord_for_Canvas(self, pos):
		""" (1,2) >> 12,25 """
	
		return pos[0] * (width_window//number_case_x) + 1, pos[1] * (height//number_case_y) + 1
		
	def check_point_in_grid(self, pos) :
		""" is (1,2) in grid of the game ? (True or False) """
	
		return(	( pos[0] >= 1 and pos[0] <= number_case_x ) and
				( pos[1] >= 1 and pos[1] <= number_case_y ) )


class Case:

	def __init__(self,canvas,pos, name) :
		
		self.canvas = canvas		# main canvas appartenance
		self.pos = pos			# ex : (3,2) , (14,5) , ......
		self.color = "blue"			# as you wish ....
		self.name = name

		self.id = canvas.create_rectangle( self.f_coord_case(), fill=self.color, tag = "free" )

	def f_coord_case(self, pos=Fasle) :
	
		if pos == False : pos = self.pos
		
		x1, y1 = grid.adjust_coord_for_Canvas(pos)

		x2 = x1 - 2 + ( Window.width_window	 //	Grid.number_case_x	)
		y2 = y1 - 2 + ( Window.height_window //	Grid.number_case_y	)
		
		return x1, y1, x2, y2

		
class Path_generator:

	def __init__(self, grid, canvas, mode=1) :
	
		self.mode = mode
		self.canvas = canvas
		self.grid = grid
		
		self.start	= (0,0)
		self.middle	= (0,0)
		self.finish	= (0,0)
		self.path	= []
		
		if	 mode == 1 : way_one()
		
		"""
		elif mode == 2 : way_two()
		elif mode == 3 : way_three()
		else : print('error in __init__')
		"""

		
	def way_one(self) : # --- it's a fucking copy-paste code : improve it !!!!!!
		""" --- old model ---
		random x for this :
		
			[X]
		[X]	[O]	[X]
			[X]
			
		(O actual_position)
		"""
		x = random.randrange(self.grid.number_case_x) + 1
		y = random.randrange(self.grid.number_case_y) + 1
		
		self.start = actual_position = old_position = (x, y)
		
		self.path.append( self.start )
		self.canvas.itemconfig( self.grid.dict_case[ self.start ].id, fill='yellow')
		
		road_finish = False
		goal_middle_placed = False
		
		while road_finish != True :
		
			future_position = [
			( coord_int[0] + 1 , coord_int[1] + 0 ) , # 	[X]
			( coord_int[0] - 1 , coord_int[1] + 0 ) , # [X]	[O]	[X]
			( coord_int[0] + 0 , coord_int[1] + 1 ) , # 	[X]
			( coord_int[0] + 0 , coord_int[1] - 1 ) ] # [0] actual_position
			
			if old_position in future_position :
				future_position.remove(old_position)
				
			future_position = [ i for i in future_position if self.grid.check_point_in_grid(i) ]

			actual_position = random.choice(future_position)
			
			self.path.append(actual_position)
			self.canvas.itemconfig( self.grid.dict_case[ actual_position ].id, fill='maroon') 
				
			actual_position = future_position		
			
			if random.randrange(10) > 7 : # to create some path				
				if not goal_middle_placed : 					
					goal_middle_placed = True
					self.canvas.itemconfig( self.grid.dict_case[ actual_position].id, fill='grey')
					self.middle = actual_position
				else:
					road_finish = True
					self.canvas.itemconfig( self.grid.dict_grid[ actual_position ].id, fill='red')
					self.finish = actual_position
		
	
	def way_two(self) :
		"""
		generate obstacles,
		per group of 2*2, 3*3, or even more,
		and if possible, link to the size of the grid
		"""
		
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
		
		def way_for(self):
		"""
		genere un path, check sa longueur, et une fois fois assez grand, le place dans la grille
		"""
		


		
class MacGyver:


	def __init__(self, canvas, start):
	
	
		self.BackPack = "empty"
		self.canvas = canvas
		self.id = canvas.create_rectangle( Case.f_coord_case(start), fill="orange")
		
		self.x = 0
		self.y = 0
		
		canvas.bind_all('<KeyPress-Left>', 	self.move_left)
		canvas.bind_all('<KeyPress-Right>', self.move_right)
		canvas.bind_all('<KeyPress-Up>', 	self.move_up)
		canvas.bind_all('<KeyPress-Down>', 	self.move_down)
		
	
	def draw(self):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		self.x = 0
		self.y = 0		
		
	def move_left(self, event):

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[0] <= 0:
			self.x = -Window.width_window//Grid.number_case_x +1
			self.y = 0
		pass
		

	def move_right(self, event):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[2] >= Window.width_window - Window.width_window//Grid.number_case_x:
			self.x = Window.width_window//Grid.number_case_x
			self.y = 0
		pass
		

	def move_down(self, event): # add
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[3] >= self.Window.height_window - Window.height_window//Grid.number_case_y:
			self.y = Window.height_window//Grid.number_case_y
			self.x = 0
		pass
		

	def move_up(self, event):	# add

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[1] <= 0: # height_window//15:
			self.y = -Window.height_window//Grid.number_case_y +1
			self.x = 0
		pass


class Middle_goal:

	def __init__(self, canvas, start):


class Final_goal:

	def __init__(self, canvas, start):


class Ball:

	def __init__(self, canvas, paddle):
	
		self.hit = 0
		self.canvas = canvas
		self.paddle = paddle
		self.id = canvas.create_oval(10, 10, 25, 25, fill='yellow')
		starts = [-3, -2, -1, 1, 2, 3]
		random.shuffle(starts)
		self.x = starts[0]
		self.y = -3
		self.canvas_height = Window.height_window
		self.canvas_width = Window.lengt_window
		self.is_hitting_bottom = False
		canvas.move(self.id, 245, 100)
	
		
	def draw(self):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)

		if pos[1] <= 0:
			self.y = 1
		if pos[3] >= self.canvas_height//15*15:
			self.y = -1
		if pos[0] <= 0:
			self.x = 3
		if pos[2] >= self.canvas_width//15*15:
			self.x = -3

		if self.hit_top_paddle(pos) == True:
			self.y = -3
			self.hit += 1
		if self.hit_bottom_paddle(pos) == True:
			self.y = 3
			self.hit += 1
		if self.hit_left_paddle(pos) == True:
			self.x = -3
			self.hit += 1
		if self.hit_right_paddle(pos) == True:
			self.x = 3
			self.hit += 1
			
			
	def hit_top_paddle(self, pos):

		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
			if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
				return True
		return False
		
		
	def hit_bottom_paddle(self, pos):
	
		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
			if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
				return True
		return False
		
	
	def hit_left_paddle(self, pos):

		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
			if pos[2] >= paddle_pos[0] and pos[2] <= paddle_pos[2]:
				return True
		return False


	def hit_right_paddle(self, pos):
	
		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
			if pos[0] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
				return True
		return False


def main():
		
	window = Window()
	grid = Grid(window.canvas)
	path = Path_generator(grid, window.canvas)
	
	macgyver 	= MacGyver(		path.start)
	middle_goal = Middle_goal(	path.middle)
	final_goal	= Final_goal(	path.final)
	ball		= Ball()
	
	playing = True
	while playing:
	
		
	
		
main()