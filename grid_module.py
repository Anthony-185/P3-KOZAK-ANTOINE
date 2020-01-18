import random
import string

class Grid:
    row, column = 15, 15
    dic   = dict()
    all   = set()
    path  = set()
    object= set()

class Case:
    def __init__(self, name):
        self.name = name
        self.attribute = None

class Object(Case):
    pass
    
class Hero(Object):
    bag = 3 * [0]
    pass

class Path:
    ''' path creator (~ map generator) '''    
    def __init__(self, column=15, row=15):
        Grid.dic = {x: 0
            for x in "start item_1 item_2 item_3 final_goal".split()}
        Grid.column = column ; Grid.row = row
        Grid.all = {(x+1, y+1) for y in range(column) for x in range(row)}
        
    def by_load_defaut_map(self):
        pass

    @staticmethod   # [0] : x, y ---> return [X] like that:  #     [X]
    def near_position(x, y):                                  # [X] [O] [X]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) #     [X]

    @staticmethod
    def some_space():
        return random.randrange(100) > 97

    def by_path_generator(self):
        obj = iter(Grid.dic.keys())
        
        actual_position: 'x, y' = random.choice(list(Grid.all))
        Grid.dic[next(obj)] = actual_position
        Grid.path |= {actual_position}
        while not Grid.dic['final_goal'] :
            future_position = [i for i in self.near_position(*actual_position)
                if i in Grid.all and i not in Grid.path]

            if not future_position :
                actual_position = random.choice(list(Grid.path))
                continue

            actual_position = random.choice(future_position)
            Grid.path |= {actual_position}
            if self.some_space():
                Grid.dic[next(obj)] = actual_position        
        assert all(Grid.dic.values())
 
  
if __name__ == '__main__':

    path = Path()
    path.by_path_generator()
    print(Grid.object < Grid.path < Grid.all)

    Mac = Hero('Mac Gyver')
    Mac.pos = Grid.dic['start']
    
    def console_print():
        print(4*"\n" + 80*"_" + "\n\n")
        for y in range(1,Grid.column+1):
            for x in range(1,Grid.row+1):
                if (x,y) == Mac.pos:                  symbol="|."
                elif (x,y) == Grid.dic['start']:      symbol="|S"
                elif (x,y) == Grid.dic['item_1']:     symbol="|o"
                elif (x,y) == Grid.dic['item_2']:     symbol="|o"
                elif (x,y) == Grid.dic['item_3']:     symbol="|o"
                elif (x,y) == Grid.dic['final_goal']: symbol="|X"
                elif (x,y) in Grid.path:              symbol="| "
                elif (x,y) not in Grid.path:          symbol="|~"
                print(symbol, end="")
            print("|")

    playing = True
    while playing:
        console_print()

        if   Mac.pos == Grid.dic['item_1']: Mac.bag[0] = True
        elif Mac.pos == Grid.dic['item_2']: Mac.bag[1] = True
        elif Mac.pos == Grid.dic['item_3']: Mac.bag[2] = True
        elif Mac.pos == Grid.dic['final_goal']:
            if all(Mac.bag): print(80*'='+'{:!^80}'.format(' WIN ')+22*'\n')
            else: print(80*'='+'{:x^80}'.format(" Game Over :'( ")+22*'\n')
    
        print(79*'_')
        move = input("z: up, d: right, s: down, q: left, exit to quit\n> ")
    
        if move == 'exit': playing = False ; new_pos = (0,0)
        elif move == 'z' : new_pos = ( Mac.pos[0], Mac.pos[1] - 1 )
        elif move == 'd' : new_pos = ( Mac.pos[0] + 1, Mac.pos[1] )
        elif move == 's' : new_pos = ( Mac.pos[0], Mac.pos[1] + 1 )
        elif move == 'q' : new_pos = ( Mac.pos[0] - 1, Mac.pos[1] )
        else: continue
    
        if new_pos in Grid.path: 
            Mac.pos = new_pos