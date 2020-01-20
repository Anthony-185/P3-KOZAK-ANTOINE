import random
import string

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
        print('--- init path ---')
        Grid.dic = {x: 0
            for x in "start item_1 item_2 item_3 final_goal".split()}
        Grid.column = column ; Grid.row = row
        Grid.all = {Case((x+1, y+1)) for y in range(column) for x in range(row)}
        print('init path done')
        
    def by_load_defaut_map(self):
        pass

    @staticmethod   # [0] : x, y ---> return [X] like that:   #     [X]
    def near_position(x, y):                                  # [X] [O] [X]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) #     [X]

    @staticmethod
    def some_space():
        return random.randrange(100) > 97

    def by_path_generator(self, failed = [0], all_loop = [0]):
        print('by path starting')
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
            print('path generator loop n°'+str(loop)) ; loop += 1
        else: 
            all_loop[0] += loop
            print('loop generator successfully finish with ', end='')
            print('failed : ',failed[0], '- all loop ', all_loop[0])
            assert all(Grid.dic.values())
            Grid.object = set(Grid.dic.values())
        print(' - closing loop', failed[0], end ='')
        if not failed[0]: print(' -\n -- all path loop closed -- ')
        else: failed[0] -= 1

class C:
    def console_print():
        print(4*"\n" + 80*"_" + "\n\n")
        for y in range(1,Grid.column+1):
            for x in range(1,Grid.row+1):
                if (x,y) == Hero.pos:                  symbol="|."
                elif (x,y) == Grid.dic['start']:      symbol="|S"
                elif (x,y) == Grid.dic['item_1']:     symbol="|o"
                elif (x,y) == Grid.dic['item_2']:     symbol="|o"
                elif (x,y) == Grid.dic['item_3']:     symbol="|o"
                elif (x,y) == Grid.dic['final_goal']: symbol="|X"
                elif (x,y) in Grid.path:              symbol="| "
                elif (x,y) not in Grid.path:          symbol="|~"
                print(symbol, end="")
            print("|")
            
if __name__ == '__main__':

    path = Path()
    path.by_path_generator()

    Hero.pos = Grid.dic['start']

    playing = True
    while playing:
        C.console_print()
        print(79*'_')
        command = input("z: up, d: right, s: down, q: left, exit to quit\n> ")
    
        if command == 'exit': playing = False
        elif command == 'z' : Hero.move((0, -1))
        elif command == 'd' : Hero.move((+1, 0))
        elif command == 's' : Hero.move((0, +1))
        elif command == 'q' : Hero.move((-1, 0))
        else: continue
