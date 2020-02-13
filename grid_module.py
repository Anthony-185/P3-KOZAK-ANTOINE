import random
import string
import time
import json
# _____________________________________________________________________________
# [ ] improve class Grid as a iterator
# [ ] Hero define in Path
# [X] list item customizable
# [ ] Add Game finish
# [ ] Add Game restart
# [X] Add Game Path loading from a file
# [X] log function
# [X] improve console print (shorter and faster program) Case.symbole = '.' ?
# _____________________________________________________________________________
# _____________________________________________________________________________
# code for log program (  >>> >>> game code begin at line 80 <<< <<<  )

print('in grid module, creating V')
class V: 
    ''' class log, used to log called function
        used by macgyver V17'''

    a = {'All + Last':['total', 'last called']} ; i = [0] ; last = [0]
    tk_ready = False
    to_print = []
    
    @staticmethod
    def for_vendetta(func):

        def f(*args, **kvargs):
            V.a['All + Last'][0] = V.i[0] = V.i[0] + 1
            V.a['All + Last'][1] = V.last[0] = [func.__name__, args, kvargs]
            
            if func.__name__ in V.a: V.a[func.__name__][0] += 1
            else: V.a[func.__name__] = [0,'msg']
            
            to_add = func, args, kvargs
            if not to_add in V.a[func.__name__]:
                V.a[func.__name__].append( to_add)
                
            V.a[func.__name__][1] = to_add
            
            return func(*args, **kvargs)
        return f
    # if lunched by Macgyver V17, caneva_update() will be created (for tkinter)

class file_like:
    '''object create to simualte an output file for print:
    >>> fake_file = file_like()
    >>> print('try out', file = fake_file)
    (if print not overwritten) '''
    def __init__(self):
        self.content = []
    def write(self, msg):
        self.content.append(msg)
        
# _____________________________________________________________________________
#   /// /// /// /// /// /// print overwrite /// /// /// /// /// ///   <<<   /!\
saved_print_function = print
def print(*args, _intern_list = [''], **kvargs):

    if not V.tk_ready:
        saved_print_function(*args, **kvargs)
        
    msg = file_like() # msg = fake_file
    kvargs.update( {'file': msg}) # update kvargs of print with the fake file
    saved_print_function(*args, **kvargs) # print to the fake file
    
    msg = ''.join(msg.content)

    _intern_list[0] = _intern_list[0] + msg
    _intern_list[0] = _intern_list[0].split('\n')[-20:] # keep last 19 lines
    _intern_list[0] = '\n'.join(_intern_list[0])
    
    if V.tk_ready:
        V.to_print.set(_intern_list[0])
        V.caneva_update()
    return None

# =========================================================================== #
# >>>> >>>> >>>> >>>>  Main code for the game start here  <<<< <<<< <<<< <<<< #
# =========================================================================== #
def generate_default_map():
    ''' generate the defaut map, stocked in 'default_map.json' '''
    d = '[\
[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0],\
[0], [0], [.], [0], [.], [.], [.], [.], [.], [0], [.], [0], [.], [.], [.],\
[0], [0], [.], [0], [0], [0], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [.], [.], [.], [0], [.], [0], [.], [0], [.], [.], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [.], [.], [.], [.], [.], [.], [.], [.], [.], [.], [.], [.], [.], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [0], [.], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [.], [.], [.], [0], [.], [0], [.], [0], [.], [.], [0],\
[0], [0], [.], [0], [0], [0], [0], [0], [.], [0], [.], [0], [.], [0], [0],\
[0], [0], [.], [0], [.], [.], [.], [.], [.], [0], [.], [0], [.], [.], [.],\
[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]\
]'
    for j,i in enumerate(d):
        if i == '.':
            d = d[:j] + '1' + d[j+1:]
    d = json.JSONDecoder().decode(d)
    grid = [ (x+1,y+1) for y in range(15) for x in range(15) ]
    path = set()
    for i, j in zip(d, grid):
        if i[0]: path |= {j}
    else: path = list(path)
    start = (2,8)
    final_goal = (14,8)
    data = {
    'start' : start,
    'final_goal' : final_goal,
    'path' : path }
    with open('default_map.json', 'w') as f:
        json.dump(data, f)           

class Grid: # transform this in a iterator
    row, column = 15, 15
    dic   = dict()
    all   = set()
    path  = set()
    object= {}
    status = [None]
    
    @staticmethod
    def terminated():
        if   Grid.status == [True]:
            print('\n *** Game Won! *** \n\n')
        elif Grid.status == [False]:
            print('\n |X| Game Over |X| \n\n')
        print('re-starting in :')
        for i in range(3,0,-1):
            print(i)
            time.sleep(1)
        else: print('NOW')
        if V.tk_ready: Grid.restart_grid()
        else:
            Hero.bag = set()
            Grid.path = set()
            Path().by_path_generator()

class Case(tuple): # add __add__ and compare function
    pass

class Hero(Case):
    name = 'Mac_gyver'
    pos = [1, 1]
    bag = set()

    @staticmethod
    @V.for_vendetta
    def move(mov):
        new_pos = [0, 0]
        new_pos[0] = Hero.pos[0] + mov[0]
        new_pos[1] = Hero.pos[1] + mov[1]
        new_pos = tuple(new_pos)
        if new_pos in Grid.path:
            Hero.pos = new_pos
            C.console_print() ; time.sleep(0)
            if new_pos in Grid.object or new_pos == Grid.dic['final_goal']:
                Hero.interact(new_pos)

    @staticmethod
    @V.for_vendetta
    def interact(new_pos):
        if   new_pos == Grid.dic['start']: return None
        elif new_pos in Grid.object:
            Hero.bag |= {new_pos}
            Grid.object -= {new_pos}
        elif new_pos == Grid.dic['final_goal']:
            if not Grid.object:
                Grid.status = [True]
            else:
                Grid.status = [False]

class Path:
    ''' path creator (~ map generator) '''
    @V.for_vendetta
    def __init__(self, column=15, row=15, nb_item=3):
        list_item = [ 'item_'+str(i + 1) for i in range(nb_item) ]
        Grid.dic = {x: 0
            for x in ['start'] + list_item + ['final_goal']}
        Grid.column = column ; Grid.row = row
        Grid.all = {Case((x+1, y+1)) for y in range(column) for x in range(row)}
        Grid.status = [None]
    
    def restart_path(): # Destroy grid, prepare for restarting map
        Hero.bag = set()
        Grid.path = set() # better ;)
    
    def by_load_defaut_map(self):
        try : 
            f = open('default_map.json', 'r')
        except FileNotFoundError:
            generate_default_map()
            f = open('default_map.json', 'r')

        data = f.readline()
        f.close()
        map_def = json.loads(data)
    
        Grid.path = { tuple(i) for i in map_def['path'] }
        Grid.dic['start'] = tuple( map_def['start'])
        Grid.dic['final_goal'] = tuple( map_def['final_goal'])
        
        for i in range(1,4):
            deja = set( Grid.dic.values())
            Grid.dic['item_' + str(i)] = \
                random.sample( Grid.path - deja, 1)[0]
        else: Grid.object = { Grid.dic['item_'+str(i+1)] \
            for i in range(len(Grid.dic)-2) }
                        
    @staticmethod
    @V.for_vendetta # take x, y as [0] -> return [X] like this #       [X]
    def near_position(x, y):                                   #   [X] [O] [X]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)  #       [X]

    @staticmethod # create to define some space between the differents element
    @V.for_vendetta
    def some_space(chance = 97):
        '''
        chance function which take size of the grid
        
        some chance value working fine:
            97: 15 * 15
            99: 25 * 25
        '''
        grid_size = Grid.row * Grid.column
        if grid_size < 225: return random.randrange(1, 101) >= 97
        return random.randrange(0, grid_size) <= 17

    @V.for_vendetta
    def by_path_generator(self, failed = [0], all_loop = [0]):
        obj = iter(Grid.dic.keys())
        
        actual_position: 'x, y' = random.choice(list(Grid.all))
        Grid.dic[next(obj)] = actual_position
        Grid.path |= {actual_position}
        Hero.pos = actual_position
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
            Grid.object = { Grid.dic['item_'+str(i+1)] \
                for i in range(len(Grid.dic)-2) }
        print(' - closing loop', failed[0] + 1, end ='')
        if not failed[0]: print(' -\n -- all path loop closed -- ')
        else: failed[0] -= 1
        all_loop[0] = 0
        # assert failed[0] == 0
        

class C:
    
    @staticmethod
    @V.for_vendetta
    def console_print():
        separator = '|' # separator
        if Grid.row > 30 or Grid.column > 20: return None
        print(80*"_" + "\n")
        for y in range(1,Grid.column+1):
            l = []
            for x in range(1,Grid.row+1):
                l.append(separator)
                if (x,y) == Hero.pos:                 symbol="."
                elif (x,y) == Grid.dic['start']:      symbol="S"
                elif (x,y) in Grid.object:            symbol="o"
                elif (x,y) == Grid.dic['final_goal']: symbol="X"
                elif (x,y) in Grid.path:              symbol=" "
                elif (x,y) not in Grid.path:          symbol="+"
                l.append(symbol)
            print("".join(l)+separator)
    
    @staticmethod
    @V.for_vendetta
    def handle():
        print(79*'_')
        command = input("z: up, d: right, s: down, q: left, exit to quit\n> ")    
        if command == 'exit': playing = False
        elif command == 'z' : Hero.move((0, -1))
        elif command == 'd' : Hero.move((+1, 0))
        elif command == 's' : Hero.move((0, +1))
        elif command == 'q' : Hero.move((-1, 0))


# =========================================================================== #
#                               ( if main )                                   #
# =========================================================================== #
if __name__ == '__main__':
        
    try: # -----------------------------------> playing with the try statement
        print('trying ... ', end = '')
        f = open('default_map.json', 'x')
        print('try done')
    except FileExistsError:
        print('failed, file existe')
    else:
        print('file created')
        f.close()
        generate_default_map()
        print('map generated')
    finally: print('executed')
    
    Path(20,30).by_load_defaut_map()
    Hero.pos = Grid.dic['start']
    playing = True
    while playing:
        C.console_print()
        C.handle()
        if Grid.status != [None] : Grid.terminated()