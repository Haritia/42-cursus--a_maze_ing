"""This module provides the class for maze generation.

It includes methods for perfect and imperfect generation, as
well as a way to prevent large open areas in an imperfect maze.
"""

from .config_manager import CheckConfig
from .cellandboard import Board
import random

DIRECTIONS = ["W", "S", "E", "N"]


class MazeGenerator:
    """Make a maze out of a raw board with fully walled cells.

    This uses the DFS (Depth First Search) algorithm.

    Argument for instantiation:
        - the data class object returned by the full check process
        made on the config file. Every attribute of that data
        class object is assigned to a matching maze attribute.
    """
    def __init__(self, config: CheckConfig) -> None:
        """Instantiate the maze object with validated config data."""
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.entry = config.ENTRY
        self.exit = config.EXIT
        self.board = Board(
            config.WIDTH,
            config.HEIGHT,
            config.ENTRY,
            config.EXIT)
        self.perfect = config.PERFECT
        self.output = config.OUTPUT_FILE
        self.display = config.DISPLAY
        self.solution = ""
        self.seed = config.SEED
        self.pattern_there = False

    def generate(self, start_x: int, start_y: int) -> None:
        """Launches the DFS algorithm to create the maze.

        This carves walls throughout the cells of the board
        to make pathways. The resulted maze is perfect
        by default, as in there's only one possible
        path from entry to exit.

        Argument:
            - A random pair of x,y coordinates.
        """
        start = self.board.get_cell(start_x, start_y)
        start.been_visited()  # mark the starting cell as visited first

        random.seed(self.seed)

        # if maze big enough, define middle pattern cells
        if self.width > 10 and self.height > 6:
            self.board.pattern()
            self.pattern_there = True  # pattern is there
        # else:
        #     print("\nToo small for 42 pattern\n")

        # add starting cell to the stack
        stack = [start]

        while stack:

            # stack means "last in, first out"
            current_pos = stack[-1]
            neighbors = self.board.direct_neighbors(current_pos)

            # filter which direct neighbors are unvisited
            unvisited_neighbors = dict(filter(
                lambda item: not item[1].visited,
                neighbors.items()
            ))

            if unvisited_neighbors:
                next_dir = random.choice(list(unvisited_neighbors.keys()))
                next_cell = unvisited_neighbors[next_dir]

                # remove wall in the random direction picked
                self.board.remove_wall(next_dir, current_pos)

                # mark next cell in that direction as visited
                next_cell.been_visited()

                # add said next cell to the stack, it's the last addition
                stack.append(next_cell)

            # if all neighbors have been visited, backtrack in the stack
            else:
                stack.pop()

        # if an imperfect maze is expected, this executes at the end
        if not self.perfect:
            self.make_it_imperfect(
                extra=int(self.width * self.height / 4)
            )  # /4 for max extra connection numbers
            self.patch_hole()

    def make_it_imperfect(self, extra: int) -> None:
        """Turns a perfect maze into an imperfect one.

        This carves extra connections throughout the maze
        to make interconnected pathways.

        Argument:
            - A number of extra connections obtained dynamically
            by multiplying the width and height of the maze and
            dividing it by a number (to keep the result high
            but not too much.)
        """
        # a wall has been successfully removed
        success = 0

        while success < extra:

            # pick random coordinates
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            current_cell = self.board.get_cell(x, y)

            # random coordinates must not match a pattern cell
            if current_cell.pattern:
                continue

            neighbors = self.board.direct_neighbors(current_cell)

            # which neighbor has a wall connected to current cell
            # and is not a pattern cell
            walled_neigh = {
                direc: cell for direc, cell in neighbors.items()
                if current_cell.wall_exist(direc) and not cell.pattern
            }

            # pick one and remove the connecting wall
            if walled_neigh:
                direction = random.choice(list(walled_neigh.keys()))
                self.board.remove_wall(direction, current_cell)
                success += 1  # a wall has been removed, increment

    def patch_hole(self) -> None:
        """Eliminates risks of 3x3 open area.

        Make sure an imperfect maze with extra carved walls
        doesn't have open 3x3 area. This goes through the
        imperfect maze again, check 3x3 blocks and add a wall
        inside an open 3x3 block if it finds any.
        """
        for y in range(self.height):
            for x in range(self.width):
                no_wall = 0
                current = self.board.get_cell(x, y)

                # only consider cells without any walls
                # as the center of a possible 3x3 block
                for item in DIRECTIONS:
                    if not current.wall_exist(item):
                        no_wall += 1

                if no_wall == 4 and self.board.check_large_area(current):
                    for _ in range(2):
                        direction = random.choice(DIRECTIONS)
                        self.board.add_wall(direction, current)
