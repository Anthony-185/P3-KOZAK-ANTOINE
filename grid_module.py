import random
import string
import time
# _____________________________________________________________________________
# [ ] improve class Grid as a iterator
# [ ] Hero define in Path
# [ ] list item customizable
# [ ] Add Game finish
# [ ] Add Game restart
# [ ] Add Game Path loading from a file
# [ ] log function
# [ ] improve console print (shorter and faster program) Case.symbole = '.' ?
# _____________________________________________________________________________

class Grid: # transform this in a iterator
    row, column = 15, 15
    dic   = dict()
    all   = set()
    path  = set()
    object= set()

class Case(tuple): # add __add__ and compare function !!!
    pass

class Hero(Case):
    name = 'Mac_gyver'
    pos = [1, 1]
    bag = 3 * [0]

    @staticmethod
    def move(mov):
        new_pos = [0, 0]
        new_pos[0] = Hero.pos[0] + mov[0]
        new_pos[1] = Hero.pos[1] + mov[1]
        new_pos = tuple(new_pos)
        if new_pos in Grid.path:
            Hero.pos = new_pos
            C.console_print() ; time.sleep(0)
            if new_pos in Grid.object:
                Hero.interact(new_pos)

    @staticmethod
    def interact(new_pos):
        if   new_pos == Grid.dic['start']: return None
        elif new_pos == Grid.dic['item_1']: Hero.bag[0] = True
        elif new_pos == Grid.dic['item_2']: Hero.bag[1] = True
        elif new_pos == Grid.dic['item_3']: Hero.bag[2] = True
        elif new_pos == Grid.dic['final_goal']:
            if all(Hero.bag): print(12*'\n'+f'{"WIN": ^79}'+'\n')
            else: print(f'{"Game Over":X^79}'+3*'\n')


class Path:
    ''' path creator (~ map generator) '''    
    def __init__(self, column=15, row=15):
        Grid.dic = {x: 0
            for x in "start item_1 item_2 item_3 final_goal".split()}
        Grid.column = column ; Grid.row = row
        Grid.all = {Case((x+1, y+1)) for y in range(column) for x in range(row)}
        
    def by_load_defaut_map(self):
        pass

    @staticmethod # take x, y as [0] --> return [X] like that #       [X]
    def near_position(x, y):                                  #   [X] [O] [X]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) #       [X]

    @staticmethod # create to define some space between the differents element
    def some_space(chance = 97):
        return random.randrange(1, 100+1) >= chance # -> 97% chance to be True

    def by_path_generator(self, failed = [0], all_loop = [0]):
        obj = iter(Grid.dic.keys())
        
        actual_position: 'x, y' = random.choice(list(Grid.all))
        Grid.dic[next(obj)] = actual_position
        Grid.path |= {actual_position}
        print('starting path generator main loop'); loop = 0
        while not Grid.dic['final_goal'] :
            if Grid.all == Grid.path:
                failed[0] += 1
                print(79*'-')
                print('path failed -> all walls deleted -> restarting now')
                Grid.path = set() ; all_loop[0] += loop
                self.by_path_generator()
                break
            
            future_position = [i for i in self.near_position(*actual_position)
                if i in Grid.all and i not in Grid.path]

            if not future_position :
                actual_position = random.choice(list(Grid.path))
                continue

            actual_position = random.choice(future_position)
            Grid.path |= {actual_position}
            if self.some_space():
                Grid.dic[next(obj)] = actual_position
            print('loop n°'+str(loop)) ; loop += 1
        else: 
            all_loop[0] += loop
            print('loop generator successfully finish with ', end='')
            print(f'{failed[0]} failed and {all_loop[0]} loop ' )
            assert all(Grid.dic.values())
            Grid.object = set(Grid.dic.values())
        print(' - closing loop', failed[0] + 1, end ='')
        if not failed[0]: print(' -\n -- all path loop closed -- ')
        else: failed[0] -= 1

class C:
    
    @staticmethod
    def console_print():
        print(4*"\n" + 80*"_" + "\n\n")
        for y in range(1,Grid.column+1):
            for x in range(1,Grid.row+1):
                if (x,y) == Hero.pos:                 symbol="|."
                elif (x,y) == Grid.dic['start']:      symbol="|S"
                elif (x,y) == Grid.dic['item_1']:     symbol="|o"
                elif (x,y) == Grid.dic['item_2']:     symbol="|o"
                elif (x,y) == Grid.dic['item_3']:     symbol="|o"
                elif (x,y) == Grid.dic['final_goal']: symbol="|X"
                elif (x,y) in Grid.path:              symbol="| "
                elif (x,y) not in Grid.path:          symbol="|~"
                print(symbol, end="")
            print("|")
    
    @staticmethod
    def handle():
        print(79*'_')
        command = input("z: up, d: right, s: down, q: left, exit to quit\n> ")    
        if command == 'exit': playing = False
        elif command == 'z' : Hero.move((0, -1))
        elif command == 'd' : Hero.move((+1, 0))
        elif command == 's' : Hero.move((0, +1))
        elif command == 'q' : Hero.move((-1, 0))

if __name__ == '__main__':

    Path().by_path_generator()
    Hero.pos = Grid.dic['start']
    playing = True
    while playing:
        C.console_print()
        C.handle()