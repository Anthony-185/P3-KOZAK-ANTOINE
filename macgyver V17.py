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
		self.dict_name = {}
		
		for x, i in enumerate( self.line_X ) :
			for y, j in enumerate ( self.line_Y ) :
			
				self.dict_case[ x+1,y+1 ] = Case( canvas, (x+1,y+1) )
				self.dict_name[ x+1,y+1 ] = j+i 
			
	def coord_str_To_int(self, coord):
		""" "A02" >> (1,2) """
	
		for i1, i2 in enumerate(self.line_X):
			if i2 == coord[0] :
				for j1, j2 in enumerate(self.line_Y):
					if j2 == coord[1] :
						return(i1 ,j1)
		print('error in transform_coord')
		
	def coord_int_To_str(self, coord):
		""" (1,2) >> "A02" """
		
		return( self.line_X[coord[0]], self.line_Y[coord[1]] )
		
	def adjust_coord_for_Canvas(self, pos):
		""" (1,2) >> 12,25 """
	
		return pos[0] * (width_window//number_case_x) + 1, pos[1] * (height//number_case_y) + 1
		
	def check_point_in_grid(self, pos) :
		""" is (1,2) in grid of the game ? (True or False) """
	
		return(	( pos[0] >= 1 and pos[0] <= number_case_x ) and
				( pos[1] >= 1 and pos[1] <= number_case_y ) )


class Case:

	def __init__(self,canvas,pos) :
		
		self.canvas = canvas		# main canvas appartenance
		self.pos = pos			# ex : (3,2) , (14,5) , ......
		self.color = "blue"			# as you wish ....

		self.id = canvas.create_rectangle( self.f_coord_case(), fill=self.color, tag = "free" )

	def f_coord_case(self) :
	
		x1, y1 = grid.adjust_coord_for_Canvas(self.pos)

		x2 = x1 - 2 + ( Window.width_window	 //	Grid.number_case_x	)
		y2 = y1 - 2 + ( Window.height_window //	Grid.number_case_y	)
		
		return x1, y1, x2, y2

		
class Path_generator:

	def __init__(self, grid, mode=1) :
	
		self.start	= (0,0)
		self.middle	= (0,0)
		self.finish	= (0,0)
		self.path	= []
		
		"""
		self.mode = mode
		if	 mode == 1 : way_one()
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
		x = random.randrange(grid.number_case_x) + 1
		y = random.randrange(grid.number_case_y) + 1
		
		coord_int = self.start = (x, y)
		coord_str = grid.coord_int_To_str( coord_int )
		
		self.start = coord_int
		self.path.append( ( coord_str, coord_int ) )
		self.canvas.itemconfig( grid.dict_grid[ coord_str ].id, fill='yellow')
		
		actual_position = old_position = coord_int
		
		road_finish = False
		goal_middle_placed = False
		
		while road_finish != True :
		
			future_position = [
			( coord_int[0] + 1 , coord_int[1] + 0 ) , # 	[X]
			( coord_int[0] - 1 , coord_int[1] + 0 ) , # [X]	[O]	[X]
			( coord_int[0] + 0 , coord_int[1] + 1 ) , # 	[X]
			( coord_int[0] + 0 , coord_int[1] - 1 ) ] # [0] actual_position
			
			if old_position in future_position :
				direction.remove(reverse_direction)
				
			future_position = [ i for i in future_position if grid.check_point_in_grid(i) ]

			actual_position = random.choice(future_position)
			
			self.path.append( (
			grid.coord_int_To_str()actual_position,
			self.return_coord_string(actual_position)))
					self.canvas.itemconfig( self.dict_grid[self.return_coord_string(actual_position)].id, fill='maroon') 
				
				actual_position = future_position								
				if random.randrange(6) > 3 : # to create some path				
					if not goal_middle_placed : 
											
						goal_middle_placed = True
						self.canvas.itemconfig( self.dict_grid[self.return_coord_string(actual_position)].id, fill='grey')
					else:
							
						road_finish = True
						self.canvas.itemconfig( self.dict_grid[self.return_coord_string(actual_position)].id, fill='red')
	
	
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


		
class MacGyver:


	def __init__(self, start):
	
		self.pos = start
		self.x = 0
		self.y = 0
		# self image = 
		self.color = 'orange'
		
		canvas.bind_all('<KeyPress-Left>', self.move_left)
		canvas.bind_all('<KeyPress-Right>', self.move_right)
		canvas.bind_all('<KeyPress-Up>', self.move_up)
		canvas.bind_all('<KeyPress-Down>', self.move_down)
		
	
	def draw(self):
	
		self.pos = self.pos[0] + self.x, self.pos[1] + self.y
		
		
		
def main():
		
	window = Window()
	grid = Grid(window.canvas)
	path = Path_generator()
	
	macgyver 	= MacGyver(		path.start)
	middle_goal = Middle_goal(	path.middle)
	final_goal	= Final_goal(	path.final)
	ball		= Ball()
	
	playing = True
	while playing:
	
		
main()