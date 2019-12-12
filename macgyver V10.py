from tkinter import *
import random
import time

Global_MacG_xy = [0,0]
Global_Ball_xy = [0,0]



class Grid:



	def __init__(self, canvas) :

	
		self.canvas = canvas
		list_grid_canvas = []
		
		for i_x in range(0,400,400//15):
			list_grid_canvas.append( canvas.create_line(0, i_x, 550, i_x, fill='green') )
		for i_y in range(0,550,550//15):
			list_grid_canvas.append( canvas.create_line(i_y, 0, i_y, 400, fill='green') )


		# coord_h = coordonées humaines ("A1", "A2", etc ....)
		# coord_m = coordonnées machines ((1,1),(2,1),....)
		
		tableX = 'ABCDEFGHIJKLMNO' ; tableY = '123456789ABCDEF'
		
		coord_h	= tuple(("%(a)s%(b)s"%{'a':i,'b':j}) for i in tableX for j in tableY)
		coord_m	= tuple( (a+1,b+1) for b in range(len(tableX)) for a in range(len(tableY)) )
		
		htom = { i : j for i, j in zip(coord_h, coord_m) }		# humain to machine ["A2"] > (2,1)
		mtoh = { i : j for i, j in zip(coord_m, coord_h) }		# machine to humain (2,1) > ["A2"]






class Border:



	def __init__(self, canvas, color):

		self.canvas = canvas
		self.id = canvas.create_polygon(
		0, 			0,
		550//15, 	0,
		550//15, 	400//15 * 10,
		0		,	400//15 * 10,
		fill=color)









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

		if pos[3] >= self.canvas_height:
			self.y = -1										# endless game (ball can hit bottom)
			# self.is_hitting_bottom = True 				# (inverse commentary for reactivate)

		if self.hit_top_paddle(pos) == True:
			self.y = -3

		if self.hit_bottom_paddle(pos) == True:
			self.y = 1

		if pos[0] <= 0:
			self.x = 3

		if pos[2] >= self.canvas_width:
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
		self.id = canvas.create_rectangle(0, 0, 550//15, 400//15, fill=color)

		self.x = 0
		self.y = 0 # add

		self.canvas_width = canvas.winfo_width()
		self.canvas_height = canvas.winfo_height()				# add

		canvas.move(self.id, 550//15, 400//15)

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
		if not pos[0] <= 0: # 550//15:
			self.x = -550//15 +1
			self.y = 0
		pass
		

	def move_right(self, event):
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[2] >= self.canvas_width - 550//15:
			self.x = 550//15
			self.y = 0
		pass
		

	def move_down(self, event): # add
	
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[3] >= self.canvas_height - 400//15:
			self.y = 400//15
			self.x = 0
		pass
		

	def move_up(self, event):	# add

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if not pos[1] <= 0: # 400//15:
			self.y = -400//15 +1
			self.x = 0
		pass




tk = Tk()
tk.title('Game')

canvas = Canvas(tk, width=550, height=400, bd=0, bg='black', highlightthickness=0)
canvas.pack()

canvas_debug = Canvas(tk, width=550, height=100, bd=0, bg='black', highlightthickness=0)
debug_1 = canvas_debug.create_text(50,25,text='hello', fill='green')
debug_2 = canvas_debug.create_text(150,25, text=Global_MacG_xy, fill='green')
debug_3 = canvas_debug.create_text(150,50, text=Global_Ball_xy, fill='green')
canvas_debug.pack()

tk.update()

grid = Grid(canvas)
border = Border(canvas, 'red')
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