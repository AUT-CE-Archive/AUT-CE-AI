import copy
from Rules import *
from gui import draw_gui


tables = []

def read_file(filepath):
    ''' Reads and returns the puzzle file '''

    # Read puzzle
    table = []
    with open(file = filepath, mode = 'r') as reader:
        rows, cols = [int(x) for x in reader.readline().split(' ')]
        table = [reader.readline().split() for _ in range(rows)]
    return rows, cols, table


def pretty_print(table):
    ''' Prints the gorgeous '''

    for line in table:
        print(' '.join(line))


def is_full(table, n):
    ''' Checks whether table is complete '''
    for i in range(n):
        for j in range(n):
            if table[i][j] == '-':
                return False
    return True


def LCV(table, n):
    ''' Runs LCV '''

    LCVs = []

    for i in range(n):
        for j in range(n):
            if table[i][j] == '-':
                count = sum([1 for k in range(n) if table[k][j] == '-'])
                count += sum([1 for k in range(n) if table[i][k] == '-'])
                LCVs.append((i, j, count))

    # Sort and return Max
    return sorted(LCVs, key = lambda x: x[2])[-1]


def forward_checking(table, x, y, n):
    ''' Forward checking '''

    # Row
    for k in range(n):
        options = []

        if table[x][k] == '-':
            if test_candidate(x, k, table, n, '1'):
                options.append('1')
            if test_candidate(x, k, table, n, '0'):
                options.append('0')

            if len(options) == 0:
                return False
            elif len(options) == 1:
                table[x][k] = options[0]


    # Column
    for k in range(k):
        options = []

        if table[k][y] == '-':
            if test_candidate(k, y, table, n, '1'):
                options.append('1')
            if test_candidate(k, y, table, n, '0'):
                options.append('0')

            if len(options) == 0:
                return False
            elif len(options) == 1:
                table[k][y] = options[0]

    return table


def mac(table, x, y, n):
    ''' Maitaining Arc Consistancy '''

    def get_neightbors(table, x, y, n):
        ''' Returns the naighbors for the given x,y '''

        neighbors = []
        for i in range(n):
            if table[x][i] == '-':
                neighbors.append((x, i))
            if table[i][y] == '-':
                neighbors.append((i, y))
        return neighbors

    queue = [(x, y)]
    while len(queue) != 0:

        x, y = queue.pop(0)
        for neighbor in get_neightbors(table, x, y, n):

            _x, _y = neighbor[0], neighbor[1]
            options = []

            if test_candidate(_x, _y, table, n, '1'):
                options.append('1')
            if test_candidate(_x, _y, table, n, '0'):
                options.append('0')

            if len(options) == 0:
                return False
            elif len(options) == 1:
                table[_x][_y] = options[0]
                queue.append((_x, _y))

    return table


def test_candidate(x, y, table, n, option):
        ''' Tests the candiate for options '''

        temp_table = copy.deepcopy(table)
        temp_table[x][y] = option

        return is_ok(temp_table, n)


def back_track(table, n, forward_check):
    ''' Back Track '''    


    back_tack_list = []

    # Most suited candidate
    x, y, count = LCV(table, n)

    # No empty places
    if count == 0:
        return False

    options = []
    if test_candidate(x, y, table, n, '1'):     # Test for 1        
        options.append('1')
    if test_candidate(x, y, table, n, '0'):     # Test for 0
        options.append('0')    

    # No options available
    if len(options) == 0:
        return False
    else:
        back_tack_list.append((table, x, y, options))

    while len(back_tack_list) != 0:
        if len(back_tack_list[-1][3]) == 0:
            back_tack_list.pop(-1)
        else:
            # Get last backtrack item
            back_track_table, x, y, options = back_tack_list[-1]
            temp_table = copy.deepcopy(back_track_table)
            temp_table[x][y] = options[0]
            options.pop(0)

            if is_full(temp_table, n):
                return temp_table
            
            if forward_check:   # Forward Checking!
                temp_table = forward_checking(temp_table, x, y, n)            
            else:               # MAC!
                temp_table = mac(temp_table, x, y, n)

            if not temp_table:
                continue

            if is_full(temp_table, n):
                return temp_table            

            # Save for later Animation
            tables.append(temp_table)

            x, y, count = LCV(temp_table, n)

            new_options = []
            if test_candidate(x, y, temp_table, n, '1'):     # Test for 1        
                new_options.append('1')
            if test_candidate(x, y, temp_table, n, '0'):     # Test for 0
                new_options.append('0')

            if len(new_options) != 0:
                back_tack_list.append((temp_table, x, y, new_options))

    return table


# Driver Function
if __name__ == '__main__':

    # Read puzzle
    rows, cols, table = read_file('puzzles/puzzle0.txt')

    result = back_track(table, rows, forward_check = True)    

    
    if result not in [0, 1]:
        # Run GUI
        tables.append(result)
        # draw_gui(tables, rows, 400)

        # Prettify
        pretty_print(result)
    else:
        print(result)    


    # print(check_count(table, rows))
    # print(check_same(table, rows))
    # print(check_duplicate(table, rows))
    # print(is_ok(table, rows))

    # print(LCV(table, rows))