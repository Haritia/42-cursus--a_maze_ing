import random
import sys
import time
from math import sin, cos, pi
# from mlx import Mlx
from collections import deque
random.seed(9)

sys.setrecursionlimit(10000)

class Cell:
    def __init__(self, line, column):
        self.column = column
        self.line = line
        self.visited = False
        self.forty_two = False
        self.solution = False
        self.wall = {
            "N": True,
            "S": True,
            "E": True,
            "W": True,
        }



class Grid:
    def __init__(self, column, line, entrer: tuple[int], sortie: tuple[int]):
        self.column = column
        self.line = line
        self.enter = entrer
        self.sortie = sortie
        self.cell = [[Cell(line=i, column=j) for j in range(self.column)] for i in range(self.line)]
        # self.forty_two()
        self.DFS_imparfait(line=self.enter[0], column=self.enter[1])
        self.solution_path = set()

    def hexa(self):
        for i in range(self.line):
            print()
            for j in range(self.column):
                N = 1 if self.cell[i][j].wall['N'] else 0
                S = 2 if self.cell[i][j].wall['S'] else 0
                E = 4 if self.cell[i][j].wall['E'] else 0
                W = 8 if self.cell[i][j].wall['W'] else 0
                value = N+S+E+W
                print(f"{value:x}", end="")

    def forty_two(self):
        x = (self.line) // 2
        y = (self.column) // 2

        # four
        self.cell[x][y - 1].forty_two = True
        self.cell[x][y - 2].forty_two = True
        self.cell[x][y - 3].forty_two = True
        self.cell[x - 1][y - 3].forty_two = True
        self.cell[x - 2][y - 3].forty_two = True
        self.cell[x + 1][y - 1].forty_two = True
        self.cell[x + 2][y - 1].forty_two = True

        # two
        self.cell[x][y + 1].forty_two = True
        self.cell[x][y + 2].forty_two = True
        self.cell[x][y + 3].forty_two = True
        self.cell[x - 1][y + 3].forty_two = True
        self.cell[x - 2][y + 3].forty_two = True
        self.cell[x - 2][y + 2].forty_two = True
        self.cell[x - 2][y + 1].forty_two = True
        self.cell[x + 1][y + 1].forty_two = True
        self.cell[x + 2][y + 1].forty_two = True
        self.cell[x + 2][y + 2].forty_two = True
        self.cell[x + 2][y + 3].forty_two = True


    def show(self):
        print("╔" + "╦".join(["═══"] * self.column) + "╗")

        for i in range(self.line):
            row = "║"
            for j in range(self.column):
                if not self.cell[i][j].forty_two:
                    if i == self.enter[0] and j == self.enter[1]:
                        row += " ▲ "
                    elif i == self.sortie[0] and j == self.sortie[1]:
                        row += " ▼ "
                    else:
                        if (i,j) in self.solution_path:
                            row += " ● "
                        else:
                            row += "   "
                else:
                    row += "███"
                if j < self.column - 1:
                    c, right = self.cell[i][j], self.cell[i][j + 1]
                    row += "║" if c.wall['E'] and right.wall['W'] else " "

            row += "║"
            print(row)

            # séparateur entre lignes : murs horizontaux
            if i < self.line - 1:
                sep = "╠"
                for j in range(self.column):
                    c, below = self.cell[i][j], self.cell[i + 1][j]
                    sep += "═══" if c.wall['S'] and below.wall['N'] else "   "
                    sep += "╬" if j < self.column - 1 else "╣"
                print(sep)

        # bordure du bas
        print("╚" + "╩".join(["═══"] * self.column) + "╝")

    def show_01(self):
        print("╔" + "╦".join(["═══"] * self.column) + "╗")

        for i in range(self.line):
            row = "║"
            for j in range(self.column):
                if not self.cell[i][j].forty_two:
                    if i == self.enter[0] and j == self.enter[1]:
                        row += " ▲ "
                    elif i == self.sortie[0] and j == self.sortie[1]:
                        row += " ▼ "
                    else:
                        row += "   "
                else:
                    row += "   "
                if j < self.column - 1:
                    c, right = self.cell[i][j], self.cell[i][j + 1]
                    row += "║" if c.wall['E'] and right.wall['W'] else " "

            row += "║"
            print(row)

            # séparateur entre lignes : murs horizontaux
            if i < self.line - 1:
                sep = "╠"
                for j in range(self.column):
                    c, below = self.cell[i][j], self.cell[i + 1][j]
                    sep += "═══" if c.wall['S'] and below.wall['N'] else "   "
                    sep += "╬" if j < self.column - 1 else "╣"
                print(sep)

        # bordure du bas
        print("╚" + "╩".join(["═══"] * self.column) + "╝")




    def BFS(self, line, column):
        q: deque = deque([(line, column)])
        road = []

        l = ['N', 'S', 'E', 'W']
        solution = set()
        random.shuffle(l)
        path = {
            "N": (line - 1, column),
            "S": (line + 1, column),
            "W": (line, column - 1),
            "E": (line, column + 1),
        }
        q.append((line, column))
        while q:
            yield
            # print("\033[2J\033[H", end="")
            # time.sleep(0.05)
            # self.show()
            now = q.popleft()

            if (now[0],now[1]) == self.sortie:
                # print(road)
                break

            for d in l:
                if self.cell[now[0]][now[1]].wall[d]:
                    continue
                elif self.cell[now[0] + path[d][0]][now[1] + path[d][1]].solution:
                    continue
                else:
                    q.append((now[0] + path[d][0], now[1] + path[d][1]))
                    road.append([(now),((now[0] + path[d][0]), (now[1] + path[d][1]))])


            self.cell[now[0]][now[1]].solution = True
            self.solution_path.add(now)

        # for i in range(self.line):
        #     for j in range(self.column):
        #         self.cell[i][j].solution = False

        self.solution_path = set()

        p = self.sortie

        while True:
            yield
            for key, value in road:
                    if p == value:
                        p = key
                        self.solution_path.add(value)

            if p == (0,0):
                break
        for x, y in self.solution_path:
            yield
            self.cell[x][y].solution = True

        # print("\033[2J\033[H", end="")
        # time.sleep(0.1)
        # self.show()




    def solve(self, start: tuple[int, int], end: tuple[int, int]):
        # print("\033[2J\033[H", end="")
        # time.sleep(0.05)
        # self.show()
        if start == end:
            print("solved")
            return True

        self.cell[start[0]][start[1]].solution = True
        l = ['N', 'S', 'E', 'W']
        random.shuffle(l)
        path = {
            "N": (start[0] - 1, start[1]),
            "S": (start[0] + 1, start[1]),
            "W": (start[0], start[1] - 1),
            "E": (start[0], start[1] + 1),
        }
        for next in l:
            if next == 'S' and start[0] == self.line - 1:
                continue

            if next == 'E' and start[1] == self.column -1:
                continue

            if self.cell[path[next][0]][path[next][1]].solution:
                continue


            if self.cell[start[0]][start[1]].wall[next]:
                continue
            
            self.solution_path.add(start)
            if self.solve(start=path[next], end=end):
                return True
        try:
            self.solution_path.remove(start)
        except Exception:
            pass
        finally:
            return False

    # def mlx(self):
    #     cell = 20
    #     k = 10
    #     H = self.line * cell
    #     W = self.column * cell
    #     m = Mlx()
    #     data: memoryview
    #     bpp: int
    #     ln: int


    #     mlx_ptr = m.mlx_init()
    #     win = m.mlx_new_window(mlx_ptr, W, H, "Amazing")
    #     img = m.mlx_new_image(mlx_ptr, W, H)
    #     data, bpp, ln, _ = m.mlx_get_data_addr(img)

        
    #     def put_pixel(line: int, column: int, color: int):
    #         if 0 <= line < H and 0 <= column < W:
    #             off: int = line * ln + column * (bpp // 8)
    #             data[off: off+4] = color.to_bytes(4, 'little')

    #     def wall(x: int, y: int, color: int):
    #         for i in range(cell):
    #             for j in range(cell):
    #                 if self.cell[x][y].wall['N']:
    #                     if i == 0:
    #                         put_pixel(line=x*cell+i, column=y*cell+j, color=color) # blanc haut
    #                 if self.cell[x][y].wall['S']:
    #                     if i == cell-1:
    #                         put_pixel(line=x*cell+i, column=y*cell+j, color=color) # vert bas
    #                 if self.cell[x][y].wall['W']:
    #                     if j == 0:
    #                         put_pixel(line=x*cell+i, column=y*cell+j, color=color) # bleu gauche
    #                 if self.cell[x][y].wall['E']:
    #                     if j == cell-1:
    #                         put_pixel(line=x*cell+i, column=y*cell+j, color=color)# jaune droite

    #     def circle(x: int, y: int, radius: int, color: int):
    #         step = 0.01 

    #         t = 0.0
    #         while t < 2 * pi:
    #             px = int(x + radius * cos(t))
    #             py = int(y + radius * sin(t))
    #             put_pixel(line=px, column=py, color=color)
    #             t += step

    #     def square(x: int, y: int, color: int):
    #         for i in range(cell):
    #             for j in range(cell):
    #                 put_pixel(line=x*cell+i, column=y*cell+j, color=color)# jaune droite


    #     def square(x: int, y: int, color: int):
    #         for i in range(cell):
    #             for j in range(cell):
    #                 put_pixel(line=x*cell+i, column=y*cell+j, color=color)# jaune droite

    #     def render(state):
    #         # time.sleep(0.5)
    #     # m.mlx_hook(win, 33, 0, close, ...)

    #         for i in state:
    #             data[0:ln*H] = b'\x00\x00\x00\xff' * (ln * H // 4)
    #             for i in range(self.line):
    #                 for j in range(self.column):
    #                     if self.cell[i][j].forty_two:
    #                         square(i,j, 0xFFFF0000)
    #                     wall(i, j, 0xFFFFFFFF)
    #                     if (i,j) == self.enter:
    #                         circle(self.enter[0]*cell + k, self.enter[1]*cell + k,5, 0xFF00FF00)

    #                     if (i,j) == self.sortie:
    #                         circle(self.sortie[0]*cell + k, self.sortie[1]*cell + k,5, 0xFF00FF00)
    #                     if (i,j) in self.solution_path:
    #                         put_pixel(i*cell + k+1, j*cell + k, 0xFFFF0000)
    #                         put_pixel(i*cell + k-1, j*cell + k, 0xFFFF0000)
    #                         put_pixel(i*cell + k, j*cell + k+1, 0xFFFF0000)
    #                         put_pixel(i*cell + k, j*cell + k-1, 0xFFFF0000)
    #                         put_pixel(i*cell + k, j*cell + k, 0xFFFF0000)
    #                         put_pixel(i*cell + k+2, j*cell + k, 0xFFFF0000)
    #                         put_pixel(i*cell + k-2, j*cell + k, 0xFFFF0000)
    #                         put_pixel(i*cell + k, j*cell + k+2, 0xFFFF0000)
    #                         put_pixel(i*cell + k, j*cell + k-2, 0xFFFF0000)
    #                         # put_pixel(i*cell + k, j*cell + k, 0xFFFF0000)

    #                 m.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)

    #     state = self.BFS(self.enter[0], self.enter[1])

    #     m.mlx_loop_hook(mlx_ptr, render, state)

    #     def close(cmd):
    #         return m.mlx_loop_exit(mlx_ptr)

    #     m.mlx_hook(win, 33, 0, close, ...)
    #     m.mlx_loop(mlx_ptr)


    def DFS_parfait(self, line: int, column: int):
        print("\033[2J\033[H", end="")
        time.sleep(0.05)
        self.show_01()
        self.cell[line][column].visited = True
        l = ['N', 'S', 'E', 'W']
        random.shuffle(l)
        path = {
            "N": [line - 1, column],
            "S": [line + 1, column],
            "W": [line, column - 1],
            "E": [line, column + 1],
        }

        for next in l:
            if next == "N":
                if line == 0:
                    continue
                elif self.cell[line - 1][column].visited:
                    continue

                elif self.cell[line - 1][column].forty_two:
                    continue

                self.cell[line][column].wall['N'] = False
                self.cell[line - 1][column].wall['S'] = False


            elif next == "S":
                if line == self.line - 1:
                    continue
                elif self.cell[line + 1][column].visited:
                    continue
                elif self.cell[line + 1][column].forty_two:
                    continue

                self.cell[line][column].wall['S'] = False
                self.cell[line + 1][column].wall['N'] = False

            elif next == "E":
                if column == self.column - 1:
                    continue
                elif self.cell[line][column + 1].visited:
                    continue
                elif self.cell[line][column + 1].forty_two:
                    continue

                self.cell[line][column].wall['E'] = False
                self.cell[line][column + 1].wall['W'] = False

            elif next == "W":
                if column == 0:
                    continue
                elif self.cell[line][column - 1].visited:
                    continue
                elif self.cell[line][column - 1].forty_two:
                    continue

                self.cell[line][column].wall['W'] = False
                self.cell[line][column - 1].wall['E'] = False

            self.DFS_parfait(column=path[next][1], line=path[next][0])

    def DFS_imparfait(self, line: int, column: int):
            # print("\033[2J\033[H", end="")
            # time.sleep(0.2)
            # self.show_01()
            self.cell[line][column].visited = True
            l = ['N', 'S', 'E', 'W']
            random.shuffle(l)
            path = {
                "N": [line - 1, column],
                "S": [line + 1, column],
                "W": [line, column - 1],
                "E": [line, column + 1],
            }

            for next in l:
                if next == "N":
                    if line == 0:
                        continue


                    elif random.random() > 0.1 and self.cell[line - 1][column].visited:
                        continue

                    elif self.cell[line - 1][column].forty_two:
                        continue

                    self.cell[line][column].wall['N'] = False
                    self.cell[line - 1][column].wall['S'] = False


                elif next == "S":
                    if line == self.line - 1:
                        continue
                    elif self.cell[line + 1][column].visited:
                        continue
                    elif self.cell[line + 1][column].forty_two:
                        continue

                    self.cell[line][column].wall['S'] = False
                    self.cell[line + 1][column].wall['N'] = False

                elif next == "E":
                    if column == self.column - 1:
                        continue
                    elif self.cell[line][column + 1].visited:
                        continue
                    elif self.cell[line][column + 1].forty_two:
                        continue

                    self.cell[line][column].wall['E'] = False
                    self.cell[line][column + 1].wall['W'] = False

                elif next == "W":
                    if column == 0:
                        continue
                    elif self.cell[line][column - 1].visited:
                        continue
                    elif self.cell[line][column - 1].forty_two:
                        continue

                    self.cell[line][column].wall['W'] = False
                    self.cell[line][column - 1].wall['E'] = False

                self.DFS_imparfait(column=path[next][1], line=path[next][0])





y = 6
x = 6

test = Grid(line=x, column=y, entrer=(0,0), sortie=(x-1, y-1))


test.solve((0,0), (x-1,y-1))
# test.BFS(0,0)
# test.solution_path = {(3, 4), (4, 9), (8, 9), (9, 8), (0, 5), (2, 2), (1, 0), (1, 6), (1, 3), (2, 8), (3, 3), (3, 9), (5, 9), (9, 7), (8, 8), (2, 4), (0, 4), (2, 1), (2, 7), (7, 9), (9, 9), (8, 7), (0, 3), (2, 0), (1, 4), (0, 6), (2, 3), (2, 9), (1, 7), (6, 9)}

# for i, y in x:
#     test.cell[i][y].solution = True
# print(test.solution_path)
test.show()
test.hexa()
# test.mlx()
