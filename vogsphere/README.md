*This project has been created as part of the 42 curriculum by **tanrandr,*haranivo**

# A-MAZE-ING
## Description
The **A-maze-ing** is a fundamental project in the **42 curriculum**, the project aims to design and develop a complet and robust maze generator in python3.10 and over.    
The goal is to implement an algorithm capable of generating valid, random  mazes.   
The program take a *config.txt* file to define the generation parameters, generate the maze structure, solves ny fibdibg the shortest path, and then :
1. Exports the result as a hexadecimal-encoded text file
2. Provide a visual representation in ASCII in the terminal
3. Expose its generation program as a reusable and installable package
---
## Instructions
### Design thinking
We start by parsing the confiuration file (config.txt) and validating the parameter data.


- The complete structure and format of your config file:
```
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=18,16
PERFECT=false
DISPLAY=false
SEED=42
```
#### Configuration files in the project
- config.txt: main configuration file used by the program at runtime.

- WIDTH & HEIGHT : the size of the maze, greater than 2 and less than 200
- ENTRY & EXIT : define the start and finish point
- OUTPUT_FILE : the file name for the result export
- PERFECT : define the maze path
- DISPLAY : show or hide the solution path
- SEED : conserve the maze ID to show at every run

#### config_manager
`extract_config` extract the required configuration in the config.txt   
This ensures the necessary key-value pairing for the maze generation
`validate_config` check the configuration data, and validates the configuration values and ensures that the parameters are coherent before generation

Then after configuration parameters, we process to the maze creation

#### mazegen
`mazegen.py` contains the maze generator. It uses a randomized DFS algorithm with backtracking to carve passages and build the maze.
`solver.py` contains the solver. It uses BFS to find the shortest path from the entry to the exit.
`cellandboard.py` define the cell and board structures. It stores the maze grid, the walls of each cell, and the methods used to remove or add walls.

#### root
`a_maze_ing.py` main entry point of the program. It loads the configuration, creates the maze, solves it, displays it, and exports the result.
`display.py` handles the ASCII rendering of the maze in the terminal. It colors the walls, entry, exit, and solution path for better visualization.
`input_choice.py` manages the interactive menu shown at the end of the program. It lets the user regenerate the maze, show or hide the solution, change colors, or quit.

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


