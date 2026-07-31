"""This module provides a display class for ASCII rendering.

It includes a palette dict variable with ANSI escape codes as values,
methods for switching colors, displaying the maze and every details in it,
displaying the solution pathway and a menu at the bottom, using

"""

from mazegen import MazeGenerator

# global variable needed to reset the color every time
RESET = "\033[0m"

# putting the colors into global dict for easy access
PALETTES = [
    {
        # Default white outline
        "wall": "\033[37m",
        "pattern": "\033[94m",
        "solution": "\033[31m",
        "entry": "\033[43m",
        "exit": "\033[41m"
    },
    {
        # Red outline
        "wall": "\033[91m",
        "pattern": "\033[38;5;207m",
        "solution": "\033[38;5;214m",
        "entry": "\033[48;5;14m",
        "exit": "\033[48;5;229m"
    },
    {
        # Green outline
        "wall": "\033[38;5;40m",
        "pattern": "\033[38;5;11m",
        "solution": "\033[38;5;162m",
        "entry": "\033[48;5;43m",
        "exit": "\033[48;5;156m"
    },
    {
        # Purple outline
        "wall": "\033[38;5;63m",
        "pattern": "\033[38;5;197m",
        "solution": "\033[38;5;175m",
        "entry": "\033[48;5;21m",
        "exit": "\033[48;5;220m"
    }
]


class DisplayAscii:
    """Display the maze and details using colored ASCII characters.

    Arguments for instantiation:
        - the MazeGenerator object;
        - the color index to pick the color to be used
        from the predefined pallette dict.
    """

    def __init__(self, maze: MazeGenerator, color_index: int = 0) -> None:
        """Define the attributes of the object."""
        self.maze = maze
        self.color_index = color_index
        self.display_solution = self.maze.display
        self.pattern_there = self.maze.pattern_there

    def next_color(self) -> int:
        """Switches the color to the next one in the palette dict.

        The choices are limited to the length of the palette dict.
        """
        self.color_index = (self.color_index + 1) % len(PALETTES)
        return self.color_index

    def paint(self, key: str, content: str) -> str:
        """Wraps an ASCII character with the prior defined color.

        Colors differ according to the type of cell detail,
        be it a wall, a pattern cell, a solution cell, or
        the entry and exit cells.
        """
        return (PALETTES[self.color_index][key] + content + RESET)

    def display(self) -> None:
        """Print every details of the maze (the carved board).

        ASCII characters wrapped with ANSI escape codes for
        styling and coloring purposes are used for this purpose.
        """
        rows: list[str] = []
        board = self.maze.board

        # mark the entry and exit cells
        board.entry_and_exit()

        # if maze too small, middle pattern omitted
        if not self.pattern_there:
            print("\nNotice : too small for 42 pattern\n")

        # go through the grid list, one list(row) of cells at a time
        for y in range(self.maze.height):

            # just print the top and left wall for each cell
            top_wall = ""
            left_wall = ""
            for x in range(self.maze.width):
                current = board.get_cell(x, y)

                top_wall += self.paint("wall", '▪')
                top_wall += (
                    self.paint("wall", "━━━") if current.wall_exist("N")
                    or current.pattern else "   ")

                left_wall += (
                    self.paint("wall", "┃") if current.wall_exist("W")
                    or current.pattern else " ")

                if current.pattern:
                    left_wall += self.paint("pattern", " █ ")
                elif current.entry:
                    left_wall += self.paint("entry", " S ")
                elif current.exit:
                    left_wall += self.paint("exit", " F ")
                elif current.solution and self.display_solution:
                    left_wall += self.paint("solution", " ● ")
                else:
                    left_wall += "   "

            top_wall += self.paint("wall", '▪')
            left_wall += self.paint("wall", "┃")  # right border
            rows.append(top_wall)
            rows.append(left_wall)

        # print the bottom border of the maze
        bottom_wall = ""
        for x in range(board.width):
            current = board.get_cell(x, self.maze.height - 1)
            bottom_wall += self.paint("wall", "+━━━")
        bottom_wall += self.paint("wall", "+")
        rows.append(bottom_wall)

        # print every added line with a new line at the end
        print("\n".join(rows))

        # practical display of the current seed
        print(f"\nSEED = {self.maze.seed}\n")

    def print_menu(self) -> None:
        """Displays a simple menu at the bottom of the maze.

        This presents the possible choices for further
        actions.
        """
        print("=== A-Maze-ing Menu ===")
        print(
            "1.Regenerate a new maze\n"
            "2.Show/hide solution\n"
            "3.Change maze color\n"
            "4.Quit\n"
        )
