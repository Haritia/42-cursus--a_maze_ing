"""This module provide the class for solving a defined maze.

It provides methods such as a BFS solver and an
hexadecimal output file writer.
"""

from mazegen import MazeGenerator, Cell


class Solver:
    """Solves a generated maze.

    This uses the BFS (Breadth First Search) algorithm
    to ensure it returns the shortest path from entry
    to exit.

    Argument for instantiation:
        - the MazeGenerator object.
    """
    def __init__(self, maze: MazeGenerator) -> None:
        """Instantiate the solver object with the maze to solve."""
        self.maze = maze
        self.solution = ""

    def solve(self) -> None:
        """Launches the BFS algorithm.

        Looks up for an open way reaching the defined
        exit in the maze. It goes through the grid attribute
        of the maze object to do so.
        """
        board = self.maze.board

        # define the starting and finishing cell first
        start = board.get_cell(self.maze.entry[0], self.maze.entry[1])
        finish = board.get_cell(self.maze.exit[0], self.maze.exit[1])

        # check if the given start and finish are in the pattern
        if start.pattern or finish.pattern:
            print("\nNotice: Invalid entry/exit choice, "
                  "inside the 42 pattern: No solution\n")
            return

        # mark the start cell as walked in (visited is already True)
        start.walked = True

        queue: list[Cell] = []
        origin: dict[Cell, tuple[Cell, str]] = {}

        queue.append(start)
        while queue:

            # queue means "first in, first out"
            current = queue[0]
            queue.pop(0)
            if current == finish:
                break
            else:
                neighbors = board.direct_neighbors(current)
                for dir, cell in neighbors.items():
                    if not current.wall_exist(dir) and not cell.walked:
                        cell.walked = True
                        queue.append(cell)
                        origin[cell] = (current, dir)

        # add finish cell to path, then backtrack until start
        path = [finish]
        while path[-1] != start:

            # add the origin cell of finish to path,
            # then the origin of its origin, and so on until start
            path.append(origin[path[-1]][0])

        # flip the list so that start is at the beginning
        path.reverse()
        for cell in path[1:]:  # slicing because start has no origin

            # add the direction of each cell to the solution str
            self.solution += origin[cell][1]

            # mark each cell in path as solution
            cell.solution = True

    def hexa_output(self) -> None:
        """Writes the maze in hexadecimal digit per cell.

        This converts the maze into lines of hexadecimals.
        Each hexadecimal digit represents a cell
        with its open and closed wall; each line in the file
        is a row. The output file also includes the entry
        and exit coordinate, as well as the solution string.
        """
        board = self.maze.board
        hex = "0123456789ABCDEF"
        output = ""

        for y in range(board.height):
            line = ""
            for x in range(board.width):
                num = ""
                current = board.get_cell(x, y)

                # make every bit in walls attribute into an str
                for bit in current.walls.values():
                    num += str(bit)

                # convert the binary digit into a decimal int
                int_output = int(num, 2)
                hex_output = hex[int_output % 16]
                line += hex_output
            line += "\n"
            output += line

        # adds entry and exit at the end
        output += "\n" + str(self.maze.entry)
        output += "\n" + str(self.maze.exit)

        # adds solution if there's any
        if not self.solution:
            output += "\n" + "No solution to display\n"
        else:
            output += "\n" + self.solution + "\n"

        with open(self.maze.output, "w") as file:
            file.write(output)
