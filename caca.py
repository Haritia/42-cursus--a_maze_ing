arr = "NSEW"


hex = "" \
"BB97\n" \
"C447" \
""

cell_4 = '101\n000\n111'
cell_7 = '111\n001\n111'
cell_9 = '111\n100\n101'
cell_B = '111\n101\n101'
cell_C = '101\n100\n111'
bin_4 = '0100'
bin_7 = '0111'
bin_9 = '1001'
bin_B = '1011'
bin_C = '1100'

def get_cell(c):
    if c == '4':
        return cell_4
    elif c == '7':
        return cell_7
    elif c == '9':
        return cell_9
    elif c == 'B':
        return cell_B
    elif c == 'C':
        return cell_C
    
def get_bin(c):
    if c == '4':
        return bin_4
    elif c == '7':
        return bin_7
    elif c == '9':
        return bin_9
    elif c == 'B':
        return bin_B
    elif c == 'C':
        return bin_C

def print_cell(s):
    print(s.replace('1', '█').replace('0', '░'))

def get_row(hex):
    cells = []
    for char in hex:
        cells.append(get_cell(char))
    row = ""
    for cell in cells:
        row += (cell.split('\n')[0])
    row += '\n'
    for cell in cells:
        row += (cell.split('\n')[1])
    row += '\n'
    for cell in cells:
        row += (cell.split('\n')[2])
    return (row)

def get_maze(hexa):
    maze =""
    for i in hexa.split('\n'):
        maze += (get_row(i)) + '\n'
    return maze

def replace_01(maze, x, y, char):
    x = (x * 3) + 1
    y = x + (len(maze.split('\n')[0]) + 1) * (3 * y + 1)
    l = list(maze)
    l[y] = char
    maze = "".join(l)
    return maze

print()
maze = (get_maze(hex))

entry = (0, 0)

maze = replace_01(maze, 1, 1, "S")
# maze = replace_01(maze, 2, 1, "w")
# maze = replace_01(maze, 3, 1, "w")

print_cell(maze)

# ({x}-{y}){c}->

def direction_to_go(hex, entry, out, lalana, seen, find_out, ways):
    x, y = entry
    arr = hex.split('\n')
    if (y >= len(arr) or x >= len(arr[0])):
        return
    row = arr[y]
    c = row[x]
    bi = get_bin(c)
    curr_seen = seen + [(x, y)]
    moved = False
    if out == (x, y):
        find_out = True
    if bi[0] == '0' and ((x - 1, y) not in curr_seen):
        moved = True
        direction_to_go(hex, (x - 1, y), out, lalana + f" W({x - 1},{y}) ", curr_seen, find_out, ways)
    if bi[1] == '0' and ((x, y + 1) not in curr_seen):
        moved = True
        direction_to_go(hex, (x, y + 1), out, lalana + f" S({x},{y + 1}) ", curr_seen, find_out, ways)
    if bi[2] == '0' and ((x + 1, y) not in curr_seen):
        moved = True
        direction_to_go(hex, (x + 1, y), out, lalana + f" E({x + 1},{y}) ", curr_seen, find_out, ways)
    if bi[3] == '0' and ((x, y - 1) not in curr_seen):
        moved = True
        direction_to_go(hex, (x, y - 1), out, lalana + f" N({x},{y - 1}) ", curr_seen, find_out, ways)
    if not moved and find_out == True:
        ways.append(f"{lalana}")

seen = []
entry = (1, 1)
out = (2, 1)
ways = []
(direction_to_go(hex, entry, out, "", seen, False, ways))
print('ways')

def parse_ways(ways):
    res = []
    for i in ways:
        w = ""
        l = []
        for d in (i.split('  ')):
            w += d.strip()[0]
            co = d.strip()[2:-1].split(',')
            l.append((int(co[0]), int(co[1])))
        res.append((w, l))
    return res

caca = parse_ways(ways)

for x, y in caca[0][1]:
    maze = replace_01(maze, x, y, "W")

print_cell(maze)