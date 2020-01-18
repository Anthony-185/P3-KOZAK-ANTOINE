import random
import string

class Grid: # transform this in a iterator
    row, column = 15, 15
    dic   = dict()
    all   = set()
    path  = set()
    object= set()

class Case: # add __add__ and compare function !!!
    def __init__(self,name, pos):
        self.name = name
        self.pos  = pos

class Object(Case):
    taken = False
    
class Hero(Case):
    bag = 3 * [0]
    def move(self, mov):
        new_pos = [0, 0]
        new_pos[0] = self.pos[0] + mov[0]
        new_pos[1] = self.pos[1] + mov[1]
        new_pos = tuple(new_pos)
        if new_pos in Grid.path:
            self.pos = new_pos
            if new_pos in Grid.object:
                self.interact(new_pos)
            
    def interact(self, new_pos):
        if   new_pos == Grid.dic['start']: return None
        elif new_pos == Grid.dic['item_1']: self.bag[0] = True
        elif new_pos == Grid.dic['item_2']: self.bag[1] = True
        elif new_pos == Grid.dic['item_3']: self.bag[2] = True
        elif new_pos == Grid.dic['final_goal']:
            if all(self.bag): print(12*'\n'+f'{"WIN": ^79}'+'\n')
            else: print(f'{"Game Over":X^79}'+3*'\n')


class Path:
    ''' path creator (~ map generator) '''    
    def __init__(self, column=15, row=15):
        Grid.dic = {x: 0
            for x in "start item_1 item_2 item_3 final_goal".split()}
        Grid.column = column ; Grid.row = row
        Grid.all = {(x+1, y+1) for y in range(column) for x in range(row)}
        
    def by_load_defaut_map(self):
        pass

    @staticmethod   # [0] : x, y ---> return [X] like that:   #     [X]
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
        Grid.object = set(Grid.dic.values())
  
if __name__ == '__main__':

    path = Path()
    path.by_path_generator()
    print(Grid.object < Grid.path < Grid.all)

    Mac = Hero('Mac Gyver', Grid.dic['start'])
    
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
        print(79*'_')
        command = input("z: up, d: right, s: down, q: left, exit to quit\n> ")
    
        if command == 'exit': playing = False
        elif command == 'z' : Mac.move((0, -1))
        elif command == 'd' : Mac.move((+1, 0))
        elif command == 's' : Mac.move((0, +1))
        elif command == 'q' : Mac.move((-1, 0))
        else: continue
