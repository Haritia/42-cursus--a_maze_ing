"""This module provides the classes for cell and board creation.

It includes a set of methods to modify a cell's state as well
as methods to define the board (cells put together), set its
entry and exit point, check for a given cell's neighbors,
remove and add walls.
"""

OPPOSITE_PAIR = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}

DIR_NEXT = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}


class Cell:
    """Define one cell's properties.

    Sets cells's coordinates, if it's
    been visited, if it's the entry or exit point and its walls.
    Each cell's wall is represented by a bit (0 means open, 1 means
    closed).
    """

    def __init__(self, x: int, y: int) -> None:
        """The instantiation of a cell requires x,y coordinates."""
        self.horizontal = x
        self.vertical = y
        self.visited: bool = False  # for DFS
        self.pattern = False
        self.entry = False
        self.exit = False
        self.walls = {
            "W": 1,
            "S": 1,
            "E": 1,
            "N": 1
        }
        self.walked = False  # for BFS
        self.solution = False

    def been_visited(self) -> None:
        """Mark a cell as visited so that DFS doesn't go in anymore."""
        self.visited = True

    def close_for_pattern(self) -> None:
        """Mark a cell as part of the 42 middle pattern.

        This guarantees the cells pattern remains fully walled
        in every direction and don't get visited by DFS
        during the carve operation"
        """
        self.pattern = True
        self.visited = True

    def is_entry(self) -> None:
        """Mark a cell as the entry cell.

        Allows allow said cell to be highlighted as such
        once the maze is displayed.
        """
        self.entry = True

    def is_exit(self) -> None:
        """Mark a cell as the exit cell.

        Allows allow said cell to be highlighted as such
        once the maze is displayed.
        """
        self.exit = True

    def wall_exist(self, direction: str) -> bool:
        """Check if the wall in the given direction is still up."""
        if self.walls[direction]:
            return True
        else:
            return False

    def punch_wall(self, direction: str) -> None:
        """Remove the wall in the given direction.

        This turns the bit of the wall from 1 to 0.
        """
        self.walls[direction] = 0

    def put_wall(self, direction: str) -> None:
        """Add back the wall in the given direction.

        Turns the bit from 0 to 1.
        """
        self.walls[direction] = 1


class Board:
    """Define a board made from an amalgamation of cells.

    The board is set according to a defined width and height,
    as well as the entry and exit coordinates.
    The grid in itself is defined as a list of lists
    containing cells (one internal list is one row).
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int]
    ) -> None:
        """Instantiate the board with provided maze configs."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def pattern(self) -> None:
        """Mark a set of cells in the middle of the grid.

        The set of cells is flagged as part of the 42 middle
        pattern by toggling their is_pattern attribute.
        """
        x = int(self.width / 2)
        y = int(self.height / 2)
        for i in range(x - 3, x):
            cell = self.get_cell(i, y)
            cell.close_for_pattern()
        for j in range(y - 2, y + 1):
            cell = self.get_cell(x - 3, j)
            cell.close_for_pattern()
            cell = self.get_cell(x + 3, j)
            cell.close_for_pattern()
        for j in range(y, y + 3):
            cell = self.get_cell(x - 1, j)
            cell.close_for_pattern()
            cell = self.get_cell(x + 1, j)
            cell.close_for_pattern()

        for i in range(x + 1, x + 4):
            cell = self.get_cell(i, y + 2)
            cell.close_for_pattern()
            cell = self.get_cell(i, y - 2)
            cell.close_for_pattern()
            cell = self.get_cell(i, y)
            cell.close_for_pattern()

    def within_bound(self, x: int, y: int) -> bool:
        """Check if a pair of coordinates is inside the grid."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        else:
            return False

    def entry_and_exit(self) -> None:
        """Mark entry cell and exit cell as such.

        This toggles the is_entry/exit attribute of each cell.
        """
        one = self.get_cell(self.entry[0], self.entry[1])
        one.is_entry()
        two = self.get_cell(self.exit[0], self.exit[1])
        two.is_exit()

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell matching a pair of coordinates.

        Looks for the matching cell in the grid,
        aka the list of cells.
        """
        return self.grid[y][x]

    def direct_neighbors(self, cell: Cell) -> dict[str, Cell]:
        """Return the four direct neighbors of a given cell.

        The neighbors are store in a dict where key is the
        direction and value is the cell.
        Make sure the neighboring cell is within bound first.
        """
        result = {}
        for dir, coordinate in DIR_NEXT.items():
            next_x = cell.horizontal + coordinate[0]
            next_y = cell.vertical + coordinate[1]
            if self.within_bound(next_x, next_y):
                result[dir] = self.get_cell(next_x, next_y)
        return result

    def check_large_area(self, cell: Cell) -> bool:
        """Check if current cell is in the middle of a 3x3 open area.

        Returns True if no wall is found inside a 3x3 area.
        """
        x, y = cell.horizontal, cell.vertical

        for next_x in range(x - 1, x + 2):
            for next_y in range(y - 1, y + 1):
                current = self.get_cell(next_x, next_y)
                if (
                    not self.within_bound(next_x, next_y)
                    or current.wall_exist("S")
                ):
                    return False

        for next_y in range(y - 1, y + 2):
            for next_x in range(x - 1, x + 1):
                current = self.get_cell(next_x, next_y)
                if (
                    not self. within_bound(next_x, next_y)
                    or current.wall_exist("E")
                ):
                    return False

        return True

    def remove_wall(self, direction: str, cell: Cell) -> None:
        """Remove a wall from a cell, in the given direction.

        (by turning the bit of that direction from 1 to 0). For
        consistancy, it also removes the opposite wall from the
        adjacent cell in that direction.
        """
        cell.punch_wall(direction)
        next_cell = self.direct_neighbors(cell)[direction]
        next_cell.punch_wall(OPPOSITE_PAIR[direction])

    def add_wall(self, direction: str, cell: Cell) -> None:
        """Add back a wall to a cell in the given direction.

        (by turning the bit of that direction from 0 to 1) and do
        the same for the adjacent cell in that direction.
        Necessary to repair 3x3 areas by adding a random wall inside.
        """
        cell.put_wall(direction)
        opposite_cell = self.direct_neighbors(cell)[direction]
        opposite_cell.put_wall(OPPOSITE_PAIR[direction])
