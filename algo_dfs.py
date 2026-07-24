#!/usr/bin/env python3


def get_maze(maze_file: str):
    with open(maze_file, "r") as f:
        maze = f.read()
    return maze


class MazeSolver:
    def __init__(self,
                 maze: str,
                 entry: tuple[int, int],
                 exits: tuple[int, int],
                 path: list[str]):
        self.maze = maze
        self.entry = entry
        self.exits = exits
        self.path = path


    @staticmethod
    def get_bin(hex):
        bi = bin(int(hex, 16))[2:]
        return bi.zfill(4)


    def path_finder(self,
                    current: tuple[int, int],
                    visited: list[tuple[int, int]],
                    find_exit: bool,
                    way: str):
        """
            maze.split(\n) = line
            line[x]= row
            B = 1    0    1    1
               [0]  [1]  [2]   [3]
                W    S    E    N
        """
        # x, y = self.entry
        x, y = current
        lines = self.maze.split('\n')  #liste ana ligne
        if (y >= len(lines) or x >= len(lines[0])):
            return
        row = lines[y].strip()
        c = row[x]
        bit = self.get_bin(c)
        visited_cells = visited + [(x, y)]
        moved = False
        if self.exits == current:
            find_exit = True
        if bit[0] == '0' and ((x - 1, y) not in visited_cells):
            moved = True
            self.path_finder((x - 1, y), visited_cells, find_exit, way + f"W ({x - 1}, {y})")
        if bit[1] == '0' and ((x, y + 1) not in visited_cells):
            moved = True
            self.path_finder((x, y + 1), visited_cells, find_exit, way + f"S ({x}, {y + 1})")
        if bit[2] == '0' and ((x + 1, y) not in visited_cells):
            moved = True
            self.path_finder((x + 1, y), visited_cells, find_exit, way + f"E ({x + 1}, {y})")
        if bit[3] == '0' and ((x, y - 1) not in visited_cells):
            moved = True
            self.path_finder((x, y - 1), visited_cells, find_exit, way + f"N ({x}, {y - 1})")

        if moved == False and find_exit == True:
            self.path.append(f"{way}")
            print(self.path)

        # print(way)
        
        
entry = (1, 1)
seen = []
find = False
path = []
maze = get_maze("maze.txt")
Maze = MazeSolver(maze, entry, (2, 1), path)
Maze.path_finder(entry, seen, find, "")

# for c in maze:
#     bi =Maze.get_bin(c)
#     print(f"{c}->{bi}  ")
