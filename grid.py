"""
if __name__ == '__main__'
console version of the game
"""
import random
import string

class Grid:
	
	def __init__(self):
	
		number_case_x = number_case_y = 15
		line_X = tuple( "{:0>2}".format(i+1) for i in range(number_case_x) )
		line_Y = tuple( i for i in string.ascii_uppercase[0:number_case_y] )
		dict_all_case = dict_str_to_int = {}
		
		for x,i in enumerate( line_X ) :
			for y,j in enumerate( line_Y ) :
				
				dict_all_case[x+1, y+1] = self.Case( j+i, "free", (x+1, y+1))
				dict_str_to_int[j+i] = x+1, y+1
				
	def coord_str_To_int(coord): # "A02" >> (1,2)
		return dict_str_to_int.get([coord])
		
	def coord_int_To_str(coord): # (1,2) >> "A02" """
		return dict_all_case.get([coord]).name
		
	def check_point_in_grid(pos) : # is (1,2) in grid of the game ? (True or False)
		return(	( pos[0] >= 1 and pos[0] <= 15 ) and # Grid.number_case_x
				( pos[1] >= 1 and pos[1] <= 15 ) )   # Grid.number_case_y


	class Case:
	
		def __init__(self, name, status, coord):
		
			self.name = name
			self.status = status
			self.coord = coord
			
			
	class Path:
	
	# /////////////////////////////////////////////////////////
	# Path generer par grid directement
	# mettre les valeurs number case lié à GRID, faire en sorte que ca se modifie facilement
	# generer la map, puis la load, ca serait cool
	# la faire en json ou sql, ca serait cool aussi !!!
	
		def __init__(self):
		
			self.start = self.middle = self.finish = (0,0)
			self.path	= set()
			
		def by_load_defaut_map(self):
		
			pass
			
		def by_path_generator(self):
		
			x = random.randrange(15) + 1 # how to link to number_case
			y = random.randrange(15) + 1 # how to link to number_case
			self.start = actual_position = (x, y)
			self.path.add( self.start )
			road_finish = goal_middle_placed = False
			i_some_path = 0	
			
			while not road_finish :

				x, y = actual_position[0], actual_position[1]
				future_position = [
				( x + 1 , y + 0 ) , # 		[X]
				( x - 1 , y + 0 ) , # 	[X] [O]	[X]
				( x + 0 , y + 1 ) , # 		[X]
				( x + 0 , y - 1 ) ] # 	[0] actual_position
	
				future_position = [ i for i in future_position if not i in self.path ]
				future_position = [ i for i in future_position if Grid.check_point_in_grid(i) ]
	
				if future_position == [] :
					actual_position = random.sample(self.path, 1)[0] # sample because path is a set
					continue
	
				actual_position = random.choice(future_position)
				self.path.add(actual_position)
				i_some_path += 1
				
				if i_some_path > 50 and random.randrange(100) > 70 : # to create some path				
					if not goal_middle_placed : 					
						goal_middle_placed = True
						self.middle = actual_position
					else:
						road_finish = True
						self.finish = actual_position

if __name__ == '__main__':

	grid = Grid()
	path = grid.Path()
	path.by_path_generator()
	Mac = path.start
	
	playing = True
	
	while playing:
		
		print(4*"\n" + 80*"_" + "\n\n")
		for y in range(1,16):
			print(20*" ", end ="")
			for x in range(1,16):
				if 		(x,y) == Mac			: print("|.", end="")
				elif	(x,y) == path.start		: print("|S", end="")
				elif	(x,y) == path.middle	: print("|O", end="")
				elif	(x,y) == path.finish	: print("|X", end="")
				elif 	(x,y) in path.path		: print("| ", end="")
				elif	(x,y) not in path.path	: print("|#", end="")
			print("|")
		
		move = input("z: up, d: right, s: down, q: left, exit to quit\n>>> ")

		if move == 'exit' : playing = False
		elif move == 'z' : new_Mac = ( Mac[0], Mac[1] - 1 )
		elif move == 'd' : new_Mac = ( Mac[0] + 1, Mac[1] )
		elif move == 's' : new_Mac = ( Mac[0], Mac[1] + 1 )
		elif move == 'q' : new_Mac = ( Mac[0] - 1, Mac[1] )
		if Grid.check_point_in_grid(new_Mac): 
			if new_Mac in path.path:
				Mac = new_Mac

