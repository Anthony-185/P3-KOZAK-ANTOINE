import random
import string

class Grid(set):
    def __init__(self, x = 15, y = 15):
        self.x = x if (x > 0 and int(x) == x) else 15
        self.y = y if (y > 0 and int(y) == y) else 15
        self.frozen = frozenset(
            (i, j) for i in range(self.x) for j in range(self.y))
        self.dic = {i: Case(i) for i in self.frozen}
        self.index = [0, 0]
    
    def __iter__(self):
        self.index[0] = -1
        return self

    def __next__(self): # not pep-8, yeah i know, but better to read for me
        self.index[0] += 1
        if self.index[0] >= self.x:
           self.index[0] = 0
           self.index[1] += 1
           if self.index[1] >= self.y:
              self.index[1] = 0
              raise StopIteration
        return self.dic[tuple(self.index)]
    
    def __call__(self, x, y):
        if 0 < x < self.x and 0 < y < self.y:
            return self.dic[x, y]
        return False
    
    def __getitem__(self, type):
        list = []
        for key, value in self.dic.items():
            if value.type == type: list.append(key)
        return list
    
    def __len__(self):
        return self.x * self.y
    
    def __contains__(self, other):
        return other in self.frozen

    def __repr__(self):
        return repr(self.frozen)
    

class Case(tuple):
    def __init__(self, pos):
        self.type = 'wall'   

class Hero(Case):
    bag = 3 * [0]
    def move(self, mov):
        new_pos = [0, 0]
        new_pos[0] = self[0] + mov[0]
        new_pos[1] = self[1] + mov[1]
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


class Path(list):
    ''' path creator (~ map generator) '''    
    def __init__(self):
        pass
        
    def by_load_defaut_map(self):
        pass

    @staticmethod   # [0] : x, y ---> return [X] like that:   #     [X]
    def near_position(x, y):                                  # [X] [O] [X]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) #     [X]

    @staticmethod
    def some_space():
        return random.randrange(100) > 97

    def by_path_generator(self, grid):
        path = set()
        obj = iter('start item_1 item_2 item_3 final_goal'.split())
        
        actual_position: 'x, y' = random.sample(grid, 1)
        path |= {actual_position}
        grid(actual_position) = next(obj)
        road_finished = False
        while not road_finished:
            future_position = [i for i in self.near_position(actual_position)
                if i in grid and i not in path]

            if not future_position :
                actual_position = random.sample(path, 1)
                continue

            actual_position = random.choice(future_position)
            path |= {actual_position}
            if self.some_space():
                try:
                    Grid.dic[next(obj)] = actual_position
                except StopIteration:
                    road_finished = True
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
