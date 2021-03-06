from tkinter import *
import random
import time

Global_MacG_xy = [0,0]
Global_Ball_xy = [0,0]

weight_window = 550
height_window = 400







def adjust_coord_for_the_canvas(pos):


	return pos[0] * (weight_window//15) + 1, pos[1] * (height_window//15) + 1






class Grid:



	def __init__(self, canvas) :

	
		self.canvas = canvas
		list_grid_canvas = []
		
		for i_x in range(0,height_window,height_window//15):
			list_grid_canvas.append( canvas.create_line(0, i_x, weight_window//15*15, i_x, fill='green') )
		for i_y in range(0,weight_window,weight_window//15):
			list_grid_canvas.append( canvas.create_line(i_y, 0, i_y, height_window//15*15, fill='green') )


		# coord_h = coordonées humaines ("A1", "A2", etc ....)
		# coord_m = coordonnées machines ((1,1),(2,1),....)
		
		tableX = 'ABCDEFGHIJKLMNO' ; tableY = '123456789ABCDEF'
		
		coord_h	= tuple(("%(a)s%(b)s"%{'a':i,'b':j}) for i in tableX for j in tableY)
		coord_m	= tuple( Case( self.canvas, adjust_coord_for_the_canvas((a, b)) ) for b in range(len(tableX)) for a in range(len(tableY)) )
		
		# dictionnaire { "coord" : tkinter id case }
		# ex: "A2" : Case(canvas, (2,1))
		
		dict_grid = { i : j for i, j in zip( coord_h , coord_m ) }

		print(dict_grid)
		for i, j in zip(dict_grid.keys(), dict_grid.values()) :
			print(i,j,j.coord,j.id)
			
			
	

	def check_point_in_grid(self ,position):
	
		
		if position[0] >= 1 and position[0] <= 15 :
		
			if position[1] >= 1 and position[1] <= 15 : 
			
				return True
				
		return False




	def road(self):
		""" Faut qu'il donne la position de toute les cases du chemin gagnant,
		la position de MacGyver,
		la position de l'objectif intermeidaire,
		et la position de l'objectif final """
	
		
		start = (random.range(15),random.range(15))
		
		actual_position = start
		
		road_finish = False
		
		goal_middle_placed = False
		
		while road_finish != True :
		
			""" --- old model ---
			future_position = random(								# random x for this :
			( actual_position[0] - 1 , actual_position[1] + 0 ) ,	# 	 [X]
			( actual_position[0] + 1 , actual_position[1] + 0 ) ,	# [X][O][X]
			( actual_position[0] + 0 , actual_position[1] + 1 ) ,	#    [X]
			( actual_position[0] + 0 , actual_position[1] - 1 ) )	# (O actual_position)
			"""

			direction = random.random(	# random x like this :
			( + 1 , + 0 ) ,				# 	 [X]
			( - 1 , + 0 ) ,				# [X][O][X]
			( + 0 , + 1 ) ,				#    [X]
			( + 0 , - 1 ) )				# (O actual_position)

			future_position = (
				actual_position[0] + direction[0] , 
				actual_position[1] + direction[1] )
			
			if check_point_in_grid(future_position) :
			
				range = random.range(2,4)
				
				future_position = (
					actual_position[0] + direction[0] * range , 
					actual_position[1] + direction[1] * range )
			
				if check_point_in_grid(future_position) :
				
					actual_position = future_position
					
					# fonction qui retien le tracé ( append(actual_postion) jusqu'a future_position)
				
					if random.range(6) > 3 :
					
						if not goal_middle_placed : 
						
							# case = middle_goal here define = actual position
							
							goal_middle_placed = True
							
						else:
						
							# case = final_goal here define = actual position
			
							road_finish = True
							
							
	
							






class Case:


	
	def __init__(self,canvas,coord) :
	
	
		self.canvas = canvas		# main canvas appartenance
	
		self.coord = coord			# ex : (3,2) , (14,5) , ......
		
		# self.coord = Grid.adjust_coord_for_the_canvas(coord)
		
		self.type = "free"			# "free" , "McGyver" , "border" , "goal_middle" , "target"
	
		self.color = "blue"		# as you wish ....
		
		self.id = canvas.create_rectangle(
			self.coord[0]					, self.coord[1]					,
			self.coord[0] -2+ weight_window//15, self.coord[1] -2+ height_window//15,
			fill=self.color) # border green for the style !!!
		
		












class Ball:



	def __init__(self, canvas, paddle, color):
	
		self.canvas = canvas
		self.paddle = paddle

		self.id = canvas.create_oval(10, 10, 25, 25, fill=color)

		starts = [-3, -2, -1, 1, 2, 3]
		random.shuffle(starts)

		self.x = starts[0]
		self.y = -3
		self.canvas_height = canvas.winfo_height()
		self.canvas_width = canvas.winfo_width()

		self.is_hitting_bottom = False

		canvas.move(self.id, 245, 100)
		
		
		

	def draw(self):
	
	
		global Global_Ball_xy
	
		self.canvas.move(self.id, self.x, self.y)

		pos = self.canvas.coords(self.id)

		if pos[1] <= 0:
			self.y = 1

		if pos[3] >= self.canvas_height//15*15:
			self.y = -1										# endless game (ball can hit bottom)
			# self.is_hitting_bottom = True 				# (inverse commentary for reactivate)

		if self.hit_top_paddle(pos) == True:
			self.y = -3

		if self.hit_bottom_paddle(pos) == True:
			self.y = 1

		if pos[0] <= 0:
			self.x = 3

		if pos[2] >= self.canvas_width//15*15:
			self.x = -3
			
		Global_Ball_xy = pos
			
			
			
			

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
		
		
		
		

class Paddle:


	def __init__(self, canvas, color):
	
	
	
		self.canvas = canvas
		self.id = canvas.create_rectangle(0, 0, weight_window//15, height_window//15, fill=color)

		self.x = 0
		self.y = 0 # add

		self.canvas_width = canvas.winfo_width()
		self.canvas_height = canvas.winfo_height()				# add

		canvas.move(self.id, weight_window//15, height_window//15)

		canvas.bind_all('<KeyPress-Left>', self.move_left)
		canvas.bind_all('<KeyPress-Right>', self.move_right)
		canvas.bind_all('<KeyPress-Up>', self.move_up)			# add
		canvas.bind_all('<KeyPress-Down>', self.move_down)		# add



	def draw(self):

		global Global_MacG_xy

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)

		self.x = 0
		self.y = 0

		Global_MacG_xy = pos



	def move_left(self, event):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[0] <= 0: # weight_window//15:
			self.x = -weight_window//15 +1
			self.y = 0
		pass
		

	def move_right(self, event):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[2] >= self.canvas_width - weight_window//15:
			self.x = weight_window//15
			self.y = 0
		pass
		

	def move_down(self, event): # add
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[3] >= self.canvas_height - height_window//15:
			self.y = height_window//15
			self.x = 0
		pass
		

	def move_up(self, event):	# add

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[1] <= 0: # height_window//15:
			self.y = -height_window//15 +1
			self.x = 0
		pass




tk = Tk()
tk.title('Game')

canvas = Canvas(tk, width=weight_window, height=height_window, bd=0, bg='black', highlightthickness=0)
canvas.pack()

canvas_debug = Canvas(tk, width=weight_window, height=100, bd=0, bg='black', highlightthickness=0)
debug_1 = canvas_debug.create_text(50,25,text='hello', fill='green')
debug_2 = canvas_debug.create_text(150,25, text=Global_MacG_xy, fill='green')
debug_3 = canvas_debug.create_text(150,50, text=Global_Ball_xy, fill='green')
canvas_debug.pack()

tk.update()

grid = Grid(canvas)
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

while 1:
	if ball.is_hitting_bottom == False:
		ball.draw()
		paddle.draw()

		canvas_debug.itemconfig(debug_2,text = Global_MacG_xy)
		canvas_debug.itemconfig(debug_3,text = Global_Ball_xy)

	else :
		a = input('lol')
	# print(paddle.canvas.coords)
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)