*This project has been created as part of the 42 curriculum by tanrandr,haranivo*.

# A-MAZE-ING
## Description
The **A-maze-ing** is a fundamental project in the **42 curriculum**, the project aims to design and develop a complete and robust maze generator in python3.10 or higher.

The goal is to implement an algorithm capable of generating valid, random mazes that can be set as **perfect** (with solely one valid pathway between start and finish point) or **imperfect** (with multiple pathways leading to the finish point).

The program take a *config.txt* file to define the generation parameters, generate the maze structure, solves by finding the shortest path, and then :
1. Exports the result as a hexadecimal-encoded text file;
2. Provide a visual representation in ASCII in the terminal;
3. Expose its generation program `mazegen` as a reusable and pip installable package.

## Project overall structure

```text
a-maze-ing/
├── Makefile                        - install / run / debug / clean / lint rules
├── README.md                       - THIS file you're reading
├── a_maze_ing.py                   - entry point, main executable
├── config.txt                      - key=value pairs for maze generation
├── display.py                      - ASCII rendering and menu display
├── input_choice.py                 - input management for maze interaction
├── mazegen/
│   ├── __init__.py                 - module documentation and exposed elements
│   ├── cellandboard.py             - defines Cell and Board classes
│   ├── generator.py                - MazeGenerator class (DFS)
│   ├── solver.py                   - defines Solver class (BFS)
│   └── config_manager/
│       ├── __init__.py             - submodule for file parsing
│       ├── extract_config.py       - read the config file and extract parameters
│       └── validate_config.py      - validate extracted parameters
├── mazegen-1.0.0-py3-none-any.whl  - build distribution (wheel)
├── mazegen-1.0.0.tar.gz            - source distribution
├── pyproject.toml                  - package configuration
└── requirements.txt                - development dependencies
```

## Instructions

### Requirements and installation

- Python 3.10 or higher
- Python modules: pydantic, build, flake8, flake8-docstrings and mypy

To ensure the project runs smoothly without any version conflicts or missing requirements, install the dependecies listed in the `requirements.txt` file using `pip` by calling the `install` rule specified in the `Makefile`:
```bash
make install
```
This will set up a virtual environment with all the required dependencies.

### Execution

Once the project installed, you can run either of these bash commands:
- Execute the main script of the program:
```bash
make run
```
- Launch the program in debug mode with Python's built-in debugger `pdb`:
```bash
make debug
```
- Remove all temporary files and caches cluttering the project repository to keep it clean and tidied up (this also removes the virtual env file):
```bash
make clean
```
- Execute `flake8 .` (with the `--docstring google` option) and `mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs` commands :
```bash
make lint
```
- Execute the previous commands to check flake8 and mypy compliances in strict mode:
```bash
make lint-strict
```
- Run the `command` to package the mazegen module, generate the distribution packages (wheel and sdist) and `pip install` the wheel in the virtual env:
```bash
make build
```
*Note: you can run the `make build` command from the get go, it will implicitly run the install rule first*

### Design logic

The maze generation requires basic configurations, like its width and height, to work properly. We then start by setting up a plain text configuration file `config.txt`. Its content will be parsed and passed through validation to insure it's suitable for the maze object instantiation.

#### Configuration file content
The complete structure and format of your config file should look something like this:
```
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=18,16
#the lines below are optional and will get a default value if omitted
OUTPUT_FILE=maze.txt
#the output file name will be "default.txt" by default
PERFECT=false
#perfect will be set up to True by default
DISPLAY=false
#display will be True by default, unless stated otherwise
SEED=42
#seed will get a randomized int by default
```

As described above, the plain text configuration file is a list of **KEY=VALUE** pairs, one per line.
Lines starting by '#' are ignored and unrequited pairs will be flagged as unecessary. Missing values and non-admissible values (coordinates out of bound, invalid tuple, invalid type of data) will also be reported with explicit error messages.

See below a detailed description of each pair:

|Key|Required|Description|
|---|---|---|
|`WIDTH`| YES | Width of the maze in cells count, must be an int (2 < WIDTH <= 200)|
|`HEIGHT`| YES | Height of the maze in cells count, must be an int (2 < WIDTH <= 200)|
|`ENTRY`| YES | Starting cell's coordinates, must be a couple of two int formatted as `x, y` (see example above) within the bound of the maze|
|`EXIT`| YES | Ending cell's coordinates, must be a couple of two int formatted as `x, y` within the bound of the maze|
|`OUTPUT_FILE`| Coud be omitted, will default to `default.txt` | Name of the export file containing the hexadecimal encryption of the maze, the entry and exit coordinates and the solution pathway; should be formatted as `name.txt`|
|`PERFECT`| Coud be omitted, will default to `True` | Define if the result maze is Perfect (only one true path) or Imperfect (several possible paths), must be a bool|
|`SEED`| Optional, will get a random int if absent | Optional int seed for generation reproducibility purpose|

#### config_manager sub-module
`extract_config.py` has been designed to extract the required configuration from the config.txt (or any plain text configuration file of your chocice).
This ensures the necessary key-value pairing for the maze generation have been passed.

`validate_config.py` check the configuration data extracted earler, validates the configuration values and ensures that the parameters are coherent before generation.

Once this done, we can proceed to the maze creation.

#### mazegen module
`cellandboard.py` defines the cell and board structures. It stores the maze grid, the walls of each cell, and the methods used to remove or add walls.

`generator.py` contains the maze generator. It uses a randomized DFS algorithm with backtracking to carve passages and build the maze.

`solver.py` contains the solver. It uses BFS to find the shortest path from the entry to the exit.

#### root level files
`a_maze_ing.py` is the main entry point of the program. It loads the configurations from the plain text file provided, instantiate and creates the maze, solves it, displays it, and exports the result to an output file.

`display.py` handles the ASCII rendering of the maze in the terminal. It colors the walls, entry, exit, and solution path for better visualization.

`input_choice.py` manages the interactive menu shown at the end of the program. It lets the user regenerate the maze, show or hide the solution, change colors, or quit.

#### Output file format and content

Once a maze generated, it is exported, as specified above, to `OUTPUT_FILE`, following this format:
- A block of `HEIGHT` lines of `WIDTH` hexadecimal digits, one digit represents a cell. Each digit encodes which one of the four walls of the given cell are open, using this bit layout:

|Bit position|Direction|
|---|---|
|0 (Least Significant Bit, LSB or the rightmost bit)| North|
|1 (second from the right)| East|
|2 (third from the right)| South|
|3 (first from the left)| West|

(`1` means the wall is closed, `0` indicates an open wall)

- An empty line.
- The entry cell coordinates `(x, y)`
- The exit cell coordinates `(x, y)`
- The shortest pathway from starting to ending cell, written as a line of directions (N, S, E, W).

### Choice of maze generation algorithm

The maze is generated using a randomized **Depth-First Search (DFS)** algorithm with backtracking. The solver uses **Breadth-First Search (BFS)** to find the shortest path.

#### Why these algorithms?
- DFS for maze generation because :
    - it is well suited for maze generation.
    - it efficiently carves connected paths while preserving a maze-like structure.
    - it produces a perfect maze by default: no revisiting already visited cells, backtracks instead, thus ensuring one pathway only between two points. The perfect maze can then be made into an imperfect one if the matching config has been set as such.
    - it is suitable for adding a visual feature in the maze, such as the `42 middle pattern` in this case, by marking the cells as visited prior.

- BFS for maze solution because:
    - it guarantees the shortest path between the starting and ending cells. DFS, which uses a stack (Last In First Out logic), commits to one direction and dives as deep as it allows before backtracking. BFS, which uses a queue (First in First Out logic), explores the cells in a "ripple in the water" effect, which means it will explore all cells **1 step away** from starting point before proceeding to the cells **2 steps away** and so on.

## Reusable module

The `mazegen` package found in this project has been designed as a package that can be used later on by installing it with the `pip` package manager.

The package is distributed as a pip installable package: `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz`, both available at the root of this project repository.

### Reusable module short documentation

**Maze generation, solving and export package.**

Builds a maze from validate configs, generates it using DFS,
optionally solves the maze with BFS, and exports the result as
hexadecimal lines in a plain text file.

- The maze object instantiation requires the validated data returned by the `full_check` function applied to the plain text file containing the maze configs.
- Passing parameters to the maze generator class for generation is done throug a plain text file (.txt). The file must contain required key-value pairs that will then be checked and validated before passing it for the maze instantiation.
- To access the generated structure, call the method `access_structure()` in the maze after generation.
- To solve the maze, instantiate a solver object, call the solve method and then then create an output file containing the generated structure translated into hexadecimals per cell, and a solution path.

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

## Features
- Random maze generation;
- "42" middle pattern, only for suitable sized mazes;
- Perfect or imperfect maze modes;
- Shortest-path solving;
- ASCII terminal display with four color palettes;
- Hexadecimal export.

## Team and project management

### Tasks assigned to each team member
- `tanrandr`: parsing config file, maze generation algorithm (DFS), overall project design, ASCII rendering, input handling, refining README file
- `haranivo`: maze solving algorithm (DFS and BFS, but BFS was ultimately retained), makefile building, partial README redaction

### Planning
1. Reading and understanding the subject expectations.
2. Mapping the steps necessary to tick all required boxes.
3. Identify the starting point of the whole project: ultimately, the entry point of the program takes a config file that serves as foundation for the maze generation, thus working on the file parser to ensure clean data was flagged as the starting point, and so on.
4. From there, the elements of the maze were implemented step by step: a maze is a grid, made of indivual cells put together, each cells should carry a certain amount of data, hence the implementation of `Cell` and `Board` as classes.
5. The maze generator was building using the recursive backtracking, and the `Board` class, which carries and attributes containing a list of `Cell` objects.
6. Once the maze built, a solving algorithm was implemented, including an export method.
7. Then came the learning process about ASCII rendering and ANSI escape codes for custom colors.
8. The input management was added at the very end. Tests were performed allong the way, at every stop and every step, to make sure the project only moves on once the current step was showing signs of working.

### What worked well
- Spliting the work into bite sized chunks to make the overall project feel more managable, instead of seeing it as one gigantic task to tackle.
- Following the pattern above, isolating configuration parsing, data validation, cell and grid logic, maze generation, maze solving and rendering made the work flow naturally and the overall code easier to read.

### What could be improvement
- Explore more generation and solving algorithm to take the project several steps further.
- Add an mlx visual output with animations.
- Extend the options in the interactive menu.

### Tools used
- `venv` to isolate the project in its own environment;
- `pip` for package and dependency management and as a build frontend tool;
- `build` as a build frontend tool to convert the mazegen module into distribution packages (source distribution `tar.gz` and build distribution `.whl`);
- `poetry-core` as build backend;
- `pydantic` for data validation following the config parsing

## Resources

- Maze generation and solution, to understand BFS and DFS :
    - https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
    - https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
    - https://youtu.be/sVcB8vUFlmU?si=Ue5lcCtWUWz8Innk
    - https://makeschool.org/mediabook/oa/tutorials/trees-and-mazes/solving-the-maze/
- ASCII rendering with ANSI escape codes:
    - https://www.asciiart.eu/ascii-borders/gallery
    - https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/standard-16-colors/
- Expanding git commands for clean collaboration:
    - https://rogerdudler.github.io/git-guide/
- Building distribution package from a python project:
    - https://packaging.python.org/en/latest/tutorials/packaging-projects/
    - https://packaging.python.org/en/latest/tutorials/installing-packages/
- Building Makefile:
    - https://earthly.dev/blog/python-makefile/
- And, last but not least, **peer to peer learning**. Questioning our neigbohring peers has gotten us ouf of blocking predicaments more than once.

### AI Usage Description

AI was used as an assisting tool throughout the project for the following tasks:
- **Understanding new concepts**: AI proves to be quite the pedagogic tool if used properly to that specific end.
- **Mind mapping**: AI helped figuring out the starting point and how tasks should be divided between team mates.
