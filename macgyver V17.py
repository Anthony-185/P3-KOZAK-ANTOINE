""" _______________________________________________
# /!\ don't actually work, it's a prototype !!!!!!!
________________________________________________"""
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
	
		text = self.canvas.create_text(0,40+self.i*40,text=' {0}. >> {1}'.format(lvl,string),
			fill='green', tag='verbose', anchor='nw', font = self.font)
		line = self.canvas.create_line(
			10, 56 + self.i*40,
			20, 56 + self.i*40, fill = 'cyan' )
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
	
		self.height_window  = Window.height_window = 400
		self.width_window = Window.width_window = 550
		
		self.tk = tkinter.Tk()
		# self.tk.geometry('958x404-50+50') # can be improved, link with window geometry
		self.tk.geometry('958x404+0-0')
		self.tk.title("MacGyver's Game")
		
		self.canvas = tkinter.Canvas(
			self.tk,
			width  = self.width_window,
			height = self.height_window, 
			bg='black')

		self.canvas.grid(row=0,column=0)
		self.tk.update()

class Grid:

	number_case_x = 15 # number of line
	number_case_y = 15 # number of column
	line_X = tuple( "{:0>2}".format(i+1) for i in range(number_case_x) ) # remove tuple and we are in deep
	line_Y = tuple( i for i in string.ascii_uppercase[0:number_case_y] ) # remove tuple and we are in deep
	dict_case = {}
	dict_A2_to_12 = {}
	
	def __init__(self, canvas):

		self.canvas = canvas		
		self.dict_case = {}
		self.dict_A2_to_12 = {}
		
		# print([i for i in Grid.line_X])
		for x, i in enumerate( Grid.line_X ) :
			for y, j in enumerate( Grid.line_Y ) :
			
				self.dict_case[ x+1,y+1 ] = Case( canvas, (x+1,y+1) , j+i )
				self.dict_A2_to_12[ j+i ] = x+1,y+1
	
		Grid.dict_case = self.dict_case
		Grid.dict_A2_to_12 = self.dict_A2_to_12
			
	def coord_str_To_int(coord):
		""" "A02" >> (1,2) """
	
		a = dict_A2_to_12.get([coord])
		if a : return a
		else : print('error in convert str to int')
		
	def coord_int_To_str(coord):
		""" (1,2) >> "A02" """
		
		for i,j in dict_A2_to_12.items() :
			if j == coord : return i
		else : print('error in convert int to str')

		
	def adjust_coord_for_Canvas(pos):
		""" (1,2) >> 12,25 """
		
		return(	pos[0] * (Window.width_window//Grid.number_case_x) + 1,
				pos[1] * (Window.height_window//Grid.number_case_y) + 1 )
		
	def check_point_in_grid(pos) :
		""" is (1,2) in grid of the game ? (True or False) """
	
		return(	( pos[0] >= 1 and pos[0] <= Grid.number_case_x ) and
				( pos[1] >= 1 and pos[1] <= Grid.number_case_y ) )


class Case:

	def __init__(self,canvas,pos, name) :
		
		self.canvas = canvas		# main canvas appartenance
		self.pos = pos			# ex : (3,2) , (14,5) , ......
		self.color = "blue"			# as you wish ....
		self.name = name

		self.id = canvas.create_rectangle( self.f_coord_case(self.pos), fill=self.color, tag = "free" )

	def f_coord_case(self, pos=False) :
	
		if pos == False : pos = self # this is shame ...
		
		x1, y1 = Grid.adjust_coord_for_Canvas(pos)

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
		
		if	 mode == 1 : self.way_one()
		
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
		
		i_debug = 0
		
		while road_finish != True :
		
			print("loop : ", i_debug) ; i_debug += 1
			x, y = actual_position[0], actual_position[1]
			print(x, y)
			future_position = [
			( x + 1 , y + 0 ) , # 		[X]
			( x - 1 , y + 0 ) , # 	[X] [O]	[X]
			( x + 0 , y + 1 ) , # 		[X]
			( x + 0 , y - 1 ) ] # 	[0] actual_position
			
			if old_position in future_position :
				future_position.remove(old_position)
				
			future_position = [ i for i in future_position if Grid.check_point_in_grid(i) ]

			actual_position = random.choice(future_position)
			
			self.path.append(actual_position)
			self.canvas.itemconfig( Grid.dict_case[ actual_position ].id, fill='maroon') 		
			
			if random.randrange(10) > 7 : # to create some path				
				if not goal_middle_placed : 					
					goal_middle_placed = True
					self.canvas.itemconfig( Grid.dict_case[actual_position].id, fill='grey')
					self.middle = actual_position
				else:
					road_finish = True
					self.canvas.itemconfig( Grid.dict_case[ actual_position ].id, fill='red')
					self.finish = actual_position
		
	
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
		
	def way_for(self):
		"""
		genere un path, check sa longueur, et une fois fois assez grand, le place dans la grille
		"""
		pass
		


		
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
		if not pos[3] >= Window.height_window - Window.height_window//Grid.number_case_y:
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

	def __init__(self, canvas, pos):
	
		self.taken = False
		self.pos = pos
		coord = Grid.adjust_coord_for_Canvas(pos)
		self.canvas = canvas
		self.id = canvas.create_text(coord, text = "X", fill='red')
		


class Final_goal:

	def __init__(self, canvas, pos):

		self.pos = pos
		self.canvas = canvas
		self.id = canvas.create_text(Grid.adjust_coord_for_Canvas(pos), text = "X", fill='black')


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
		self.canvas_width = Window.width_window
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
	
	v = V(window)
	v.for_vendetta(window,0)
	
	grid = Grid(window.canvas)
	v.for_vendetta(window.canvas,1)
	
	path = Path_generator(grid, window.canvas)
	v.for_vendetta(path,2)
	
	
	macgyver 	= MacGyver(		window.canvas, path.start)
	middle_goal = Middle_goal(	window.canvas, path.middle)
	final_goal	= Final_goal(	window.canvas, path.finish)
	ball		= Ball(window.canvas, macgyver)
	v.for_vendetta("help",3)
	
	
	playing = True
	while playing:
		
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