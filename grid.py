"""
if __name__ == '__main__'
console version of the game
"""
import random
import string

class Grid:
    ROW = 0
    COLUMN = 0
    
    def __init__(self, x = 15, y = 15):
        ''' init grid, accept optional arguments x or y,
            to define the size of the grid,
            only if 15 <= x <= 38 and 15 <= y <= 26
        '''
        if not 15 <= x <= 39:
            x = 15 if x < 15 else 39
        if not 15 <= y <= 23:
            y = 15 if y < 15 else 23
        number_case_x, number_case_y = Grid.ROW, Grid.COLUMN = x, y
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
        return( ( pos[0] >= 1 and pos[0] <= Grid.ROW ) and # Grid.number_case_x
                ( pos[1] >= 1 and pos[1] <= Grid.COLUMN ) )   # Grid.number_case_y


    class Case:
    
        def __init__(self, name, status, coord):
        
            self.name = name
            self.status = status
            self.coord = coord
            
            
    class Path:
    
    # /////////////////////////////////////////////////////////
    # Path generer par grid directement
    # generer la map, puis la load, ca serait cool
    # la faire en json ou sql, ca serait cool aussi !!!
    # /////////////////////////////////////////////////////////
    
        def __init__(self):
            ''' define two objects to keep track of the path
            self.dict_obj_pos >>> { start: (2, 3), item_1: (12, 7), ... }
            self.path >>> { (2, 3), (4,12), (12, 12), ... }
            '''
            self.dict_obj_pos = {x: 0
                for x in "start item_1 item_2 item_3 final_goal".split() }
            self.path = set()
            
        def by_load_defaut_map(self):
            pass
            
        def by_path_generator(self):
        
            x = random.randrange(Grid.ROW) + 1 
            y = random.randrange(Grid.COLUMN) + 1
            self.dict_obj_pos['start'] = actual_position = (x, y)
            self.path.add( actual_position )
            road_finish = False
            i_some_path = 0
            
            while not road_finish :
                
                x, y = actual_position[0], actual_position[1]
                future_position = [
                ( x + 1 , y + 0 ) , #       [X]
                ( x - 1 , y + 0 ) , #   [X] [O] [X]
                ( x + 0 , y + 1 ) , #       [X]
                ( x + 0 , y - 1 ) ] #   [0] actual_position
    
                future_position = [ i for i in future_position
                    if not i in self.path
                    and Grid.check_point_in_grid(i) ]
    
                if not future_position :
                    actual_position = random.sample(self.path, 1)[0]
                    continue
    
                actual_position = random.choice(future_position)
                self.path.add(actual_position)
                i_some_path += 1
                
                if i_some_path > 17 and random.randrange(117) > 77 :
                    i_some_path = 0
                    for i in self.dict_obj_pos.keys():
                        if 'item' in i and not self.dict_obj_pos[i]:
                            self.dict_obj_pos[i] = actual_position
                            break
                    else: 
                        self.dict_obj_pos['final_goal'] = actual_position
                        assert all(self.dict_obj_pos.values())
                        road_finish = True

if __name__ == '__main__':

    restart = True ; size = []
    while restart:
        
        if size: grid = Grid(x = size[0], y = size[1]) ; size = []
        else: grid = Grid()
        path = grid.Path()
        path.by_path_generator()
        Mac = path.dict_obj_pos['start']

        playing = True
        item_taken=[0] * 3

        while playing:

            print(4*"\n" + 80*"_" + "\n\n")
            for y in range(1,Grid.COLUMN+1):
                # print(2*" ", end ="")
                for x in range(1,Grid.ROW+1):
                    if (x,y) == Mac:                               symbol="|."
                    elif (x,y) == path.dict_obj_pos['start']:      symbol="|S"
                    elif (x,y) == path.dict_obj_pos['item_1']:     symbol="|o"
                    elif (x,y) == path.dict_obj_pos['item_2']:     symbol="|o"
                    elif (x,y) == path.dict_obj_pos['item_3']:     symbol="|o"
                    elif (x,y) == path.dict_obj_pos['final_goal']: symbol="|X"
                    elif (x,y) in path.path:                       symbol="| "
                    elif (x,y) not in path.path:                   symbol="|~"
                    print(symbol, end="")
                print("|")

            if   Mac == path.dict_obj_pos['item_1']: item_taken[0] = True
            elif Mac == path.dict_obj_pos['item_2']: item_taken[1] = True
            elif Mac == path.dict_obj_pos['item_3']: item_taken[2] = True

            if   Mac == path.dict_obj_pos['final_goal']:
                if all(item_taken):
                    print(80*'='+'{:!^80}'.format(' WIN ')+22*'\n')
                else:
                    print(80*'='+'{:x^80}'.format(" Game Over :'( ")+22*'\n')
                playing = False
                continue

            move = input("z: up, d: right, s: down, q: left, exit to quit\n>>> ")

            if move == 'exit' : playing = False ; new_Mac = (0,0)
            elif move == 'z' : new_Mac = ( Mac[0], Mac[1] - 1 )
            elif move == 'd' : new_Mac = ( Mac[0] + 1, Mac[1] )
            elif move == 's' : new_Mac = ( Mac[0], Mac[1] + 1 )
            elif move == 'q' : new_Mac = ( Mac[0] - 1, Mac[1] )
            elif move == 're':
                size.append( int(input('x : ')) )
                size.append( int(input('y : ')) )
                break
            else: new_Mac = (0,0)

            if Grid.check_point_in_grid(new_Mac): 
                if new_Mac in path.path:
                    Mac = new_Mac
                    
        else: restart = not input('press enter to resart: ')
    print('last line')

