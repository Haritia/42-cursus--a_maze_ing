*This project has been created as part of the 42 curriculum by tanrandr and haranivo.*

# A-MAZE-ING

## Description
A-MAZE-ING is a Python project from the 42 curriculum that generates, solves, and exports mazes. It reads a configuration file, builds a maze, finds a path from the entry to the exit, and can display the result in the terminal or export it as a hexadecimal text file.

## Instructions
### Installation and execution
The project requires Python 3.11 or newer.

From the project folder, you can install the dependencies with:
```bash
python3 -m venv .mazenv
source .mazenv/bin/activate
pip install -r requirements.txt
```

You can also use the provided Makefile:
```bash
make install
make run
make lint
make clean
```

To run the program manually:
```bash
python3 a_maze_ing.py config.txt
```

The program validates the configuration, generates the maze, solves it, displays the result, and writes the export file.

## Configuration file
The program reads a text configuration file with key/value pairs. The expected structure is:
```txt
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=18,16
OUTPUT_FILE=maze.txt
PERFECT=false
DISPLAY=false
SEED=42
```

### Parameters
- WIDTH and HEIGHT: maze size, must be greater than 2 and smaller than 200.
- ENTRY and EXIT: start and finish coordinates in x,y format.
- OUTPUT_FILE: name of the file created by the solver.
- PERFECT: keeps the maze perfect when set to true; otherwise extra openings are added.
- DISPLAY: enables or disables the ASCII display of the solution.
- SEED: fixed value used to reproduce the same maze generation.

### Configuration files in the project
- config.txt: main configuration file used by the program at runtime.

## Maze generation algorithm
#### config_manager
`extract_config` extract the required configuration in the config.txt   
This ensures the necessary key-value pairing for the maze generation
`validate_config` check the configuration data, and verify if its value is valid
`a_maze_ing.py` main entry point of the program. It loads the configuration, creates the maze, solves it, displays it, and exports the result.
`display.py` handles the ASCII rendering of the maze in the terminal. It colors the walls, entry, exit, and solution path for better visualization.
`input_choice.py` manages the interactive menu shown at the end of the program. It lets the user regenerate the maze, show or hide the solution, change colors, or quit.
`mazegen/mazegen.py` contains the maze generator. It uses a randomized DFS algorithm with backtracking to carve passages and build the maze.
`mazegen/solver.py` contains the solver. It uses BFS to find the shortest path from the entry to the exit.
`mazegen/cellandboard.py` defines the cell and board structures. It stores the maze grid, the walls of each cell, and the methods used to remove or add walls.
`mazegen/config_manager/extract_config.py` reads the configuration file and extracts the key/value pairs.
`mazegen/config_manager/validate_config.py` validates the configuration values and ensures that the parameters are coherent before generation.


The maze is generated using a randomized Depth-First Search (DFS) algorithm with backtracking. The solver uses Breadth-First Search (BFS) to find the shortest path.

### Why these algorithms?
- DFS is well suited for maze generation because it efficiently carves connected paths while preserving a maze-like structure.
- BFS is ideal for solving the maze because it guarantees the shortest path in an unweighted grid.


## Features
- Random maze generation
- Perfect or imperfect maze modes
- Shortest-path solving
- ASCII terminal display
- Hexadecimal export

## Resources


## Team and project management


