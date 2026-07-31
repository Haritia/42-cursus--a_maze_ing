"""This module provides a function to interact with the maze."""

from mazegen import MazeGenerator, Solver, full_check
from display import DisplayAscii
import random
import os
import sys


def input_choice(
        maze: MazeGenerator,
        display: DisplayAscii,
        solve: Solver,
        solutiondisplay: bool,
        color_index: int = 0
) -> None:
    """Reads the user's input according at the end.

    Possible input are defined accoding to the choices
    presented in the displayed menu at the bottom of
    the maze, and triggers the matching actions.
    """
    while True:
        try:
            choice = int(input("Choice? (1-4):"))
            break
        except ValueError:
            print("Invalid choice, read the actual options.\n")
            # input_choice(maze, display, solve, color_index)
        except (KeyboardInterrupt, EOFError):
            print("\n\n=== Program interrupted ===\n")
            sys.exit()

    param = full_check("config.txt")

    # generate a new maze, solve and display it and the menu
    if choice == 1:
        os.system("clear")
        # print(f"Initial config: {param}\n")
        new_maze = MazeGenerator(param)
        new_maze.seed = random.randint(0, 1000)
        new_maze.display = solutiondisplay
        new_maze.generate(0, 0)
        solve = Solver(new_maze)
        solve.solve()
        display = DisplayAscii(new_maze, color_index)
        display.display()
        solve.hexa_output()
        display.print_menu()
        input_choice(new_maze, display, solve, solutiondisplay, color_index)

    # switch the maze attribute "display" to the opposite state
    if choice == 2:
        os.system("clear")
        maze.display = not maze.display
        new_solution = maze.display
        display = DisplayAscii(maze, color_index)
        display.display()
        display.print_menu()
        input_choice(maze, display, solve, new_solution, color_index)

    # move on to the next color of the palette dict
    if choice == 3:
        os.system("clear")
        # display = DisplayAscii(maze, color_index)
        display.color_index = display.next_color()
        display.display()
        display.print_menu()
        input_choice(
            maze,
            display, solve, solutiondisplay, display.color_index)

    # print a sendoff message then exit
    if choice == 4:
        print("=== Goodbye, stay amazing ;) ===")
        sys.exit()

    # for choices out of range, print error and prompt new input
    else:
        print("Invalid choice, read the actual options.\n")
        input_choice(maze, display, solve, solutiondisplay, color_index)
