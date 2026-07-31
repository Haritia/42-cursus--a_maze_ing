#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tanrandr <tanrandr@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/17 11:12:35 by tanrandr            #+#    #+#            #
#   Updated: 2026/07/30 18:10:39 by tanrandr           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""This instantiate all objects required for maze generation and solving."""

from mazegen import MazeGenerator, Solver, full_check
from display import DisplayAscii
from input_choice import input_choice
from pydantic import ValidationError
import sys
import os


if len(sys.argv) < 2:
    print("Please provide a proper config file.")
else:
    try:
        os.system("clear")
        param = full_check(sys.argv[1])
        print(param)

        maze = MazeGenerator(param)
        maze.generate(0, 0)

        solve = Solver(maze)
        solve.solve()

        display = DisplayAscii(maze)
        display.display()

        solve.hexa_output()
        display.print_menu()
        input_choice(maze, display, solve, maze.display)
    except ValidationError as v:
        for error in v.errors():
            if "Value error" in error['msg'].split(', ', 1):
                print(
                    f"Oops, {error['msg'].split(', ', 1)[1]}",
                    file=sys.stderr)
            else:
                print(
                    f"{error['msg']} for {error['loc'][0]}",
                    file=sys.stderr)
    except ValueError as e:
        print("Oops,", e, file=sys.stderr)
