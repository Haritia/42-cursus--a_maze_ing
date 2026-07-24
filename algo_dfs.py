#!/usr/bin/env python3

def get_bin(hex):
    bi = bin(int(hex, 16))
    return bi



def get_maze(maze_file: str):
    with open(maze_file, "r") as f:
        maze = f.read()
    return maze


def path_finder(maze, entry: tuple[int, int], exit: tuple[int, int], way, visited, out, path):
    """
        maze.split(\n) = line
        line[x]= row
    """

get_maze("mazegen.py")