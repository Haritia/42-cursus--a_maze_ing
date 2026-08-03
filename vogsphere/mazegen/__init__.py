"""Maze generation, solving and export package.

Builds a maze from validate configs, generates it using DFS,
optionally solves the maze with BFS, and exports the result as
hexadecimal lines in a plain text file.

- The maze object instantiation requires  the validated data returned by
the full_check function applied to the plain text file containing the
maze configs.
- Passing parameters to the maze generator class for generation is done
throug a plain text file (.txt). The file must contain required
key-value pairs that will then be checked and validated before passing
it for the maze instantiation.
- To access the generated structure, call the method access_structure()
in the maze after generation.
- To solve the maze, instantiate a solver object, call the solve method
and then then create an output file containing the generated structure
translated into hexadecimals per cell, and a solution path.

    Example of the config file content:
        WIDTH=20
        HEIGHT=20
        ENTRY=1,0
        EXIT=18,16
        OUTPUT_FILE=maze.txt
        PERFECT=false
        DISPLAY=true
        SEED=45

Typical usage example:

    from mazegen import full_check, MazeGenerator, Solver

    param = full_check("config.txt")
    maze = MazeGenerator(param)
    maze.generate(0, 0)

    structure = maze.access_structure()
    for line in structure:
        print(line)
        print()

    solver = Solver(maze)
    solver.solve()
    solver.hexa_output()
"""

from .generator import MazeGenerator
from .cellandboard import Board, Cell
from .solver import Solver
from .config_manager import full_check, CheckConfig

__all__ = [
    "MazeGenerator",
    "Board",
    "Cell",
    "Solver",
    "full_check",
    "CheckConfig"
]
