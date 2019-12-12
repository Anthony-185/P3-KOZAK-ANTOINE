from tkinter import *
import random
import time


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
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)

		self.x = 0
		self.y = 0


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




# ---------------------------------

list_grid = []


for i_x in range(0,400,400//15):

	list_grid.append( canvas.create_line(0, i_x, 550, i_x, fill='green') )
	

for i_y in range(0,550,550//15):

	list_grid.append( canvas.create_line(i_y, 0, i_y, 400, fill='green') )

# ---------------------------------




canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

while 1:
	if ball.is_hitting_bottom == False:
		ball.draw()
		paddle.draw()

	else :
		a = input('lol')
	print(paddle.canvas.coords)
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)