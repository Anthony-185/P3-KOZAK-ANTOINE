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

		number_case_x = 15 # number of line
		number_case_y = 15 # number of column
		self.canvas = canvas
		self.line_X = ( f"{i+1:0>2}" for i in range(number_case_x) )
		# ( a+b for a,b in zip("0102030405"[::2], "0102030405"[1::2]) ) (other way)
		self.line_Y = ( i for i in string.ascii_uppercase[0:number_case_y] )
		self.case = tuple(
			Case( self.canvas, adjust_coord_for_Canvas((a,b)) ) 
			for b in range(number_case_y) for a in range(number_case_x) )
		self.dict_grid = {} i = 0
		for letter_column in self.line_Y :
			for number_line in self.line_X :
				self.dict_grid[letter_column+number_line] = self.case[i]
				i += 1
		
	
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
	
	
	def road(self) : # generate the path to win
	
		# use the class Path_generator


class Case:


	def __init__(self,canvas,coord) :
		
		self.canvas = canvas		# main canvas appartenance
		self.coord = coord			# ex : (3,2) , (14,5) , ......
		self.color = "blue"			# as you wish ....		
		self.id = canvas.create_rectangle(
			self.coord[0]						, self.coord[1]							,
			self.coord[0] -2+ width_window//15	, self.coord[1] -2+ height_window//15	,
			fill=self.color, tag = "border")
		


class Path_generator:


	def __init__(self, mode=1) :
	
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
		future_position = random(								# random x for this :
		( actual_position[0] - 1 , actual_position[1] + 0 ) ,	# 	 [X]
		( actual_position[0] + 1 , actual_position[1] + 0 ) ,	# [X][O][X]
		( actual_position[0] + 0 , actual_position[1] + 1 ) ,	#    [X]
		( actual_position[0] + 0 , actual_position[1] - 1 ) )	# (O actual_position)
		"""

		start = (random.randrange(15)+1,random.randrange(15)+1)
		self.win_way.append((start,self.return_coord_string(start)))
		self.canvas.itemconfig( self.dict_grid[self.return_coord_string(start)].id, fill='yellow') 
		actual_position = start
		road_finish = False
		goal_middle_placed = False
		reverse_direction = []
		while road_finish != True :
		
			direction = [	# random x like this :
			( + 1 , + 0 ) ,				# 	 [X]
			( - 1 , + 0 ) ,				# [X][O][X]
			( + 0 , + 1 ) ,				#    [X]
			( + 0 , - 1 ) ]				# (O actual_position)		
			if reverse_direction in direction :
				direction.remove(reverse_direction)
			direction = random.choice(direction)
			range_dir = random.randrange(2,4)
			future_position = (
				actual_position[0] + direction[0] * range_dir , 
				actual_position[1] + direction[1] * range_dir )
			if self.check_point_in_grid(future_position) :

				reverse_direction = ( - direction[0], - direction[1] )
				for i in range(range_dir):
				
					actual_position = (
						actual_position[0] + direction[0] , 
						actual_position[1] + direction[1] )
					self.win_way.append((actual_position,self.return_coord_string(actual_position)))
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
	
	playing = True
	while playing:
	
		
main()