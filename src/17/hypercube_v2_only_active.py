"""
Author: Darren
Date: 17/12/2020

Solving: https://adventofcode.com/2020/day/17

Solution 2 of 2:
    Only stores active cells in the grid.  Much more efficient.
    Reduces execution time from 3 minutes down to ~30s using CPython, and about 5s using PyPy.

Part 1
------
3D space of cubes which are active or inactive.  
With each iteration, cells change state simultaneously, according to rules:
    - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
      Otherwise, the cube becomes inactive.
    - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. 
      Otherwise, the cube remains inactive.

Each cube will have 26 neighbours (8 in the same plane; 9 in upper and lower planes)

Part 2
------
As before, but now extends to 4D.
"""

import sys
import os
import time
from cell import *
from pprint import pprint as pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/init_state.txt"
SAMPLE_INPUT_FILE = "input/sample_init_state.txt"

ACTIVE = '#'
CYCLES = 6


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    pp(input)

    grid = set()
    process_init(input, grid)
    for i in range(CYCLES):
        print(f"Cycle {i}:")
        grid = execute_cycle(grid)

    print(f"Sum active: {len(grid)}")

    grid = set()
    process_init_4d(input, grid)

    for i in range(CYCLES):
        print(f"Cycle {i}:")
        grid = execute_cycle(grid)

    print(f"Sum active: {len(grid)}")


def execute_cycle(grid):
    cells_to_add = set()
    cells_to_remove = set()

    for existing_cell in grid:
        neighbours_of_existing_cell = existing_cell.get_neighbours()
        existing_cell_active_neighbours_count = 0
        for neighbour in neighbours_of_existing_cell:
            # neighbour not yet in grid
            # we need to add it, so we need to determine its own neighbours
            if neighbour not in grid:        
                new_cell_neighbours = neighbour.get_neighbours()
                # the intersection will give us all the active neighbours for this cell
                new_cell_active_neighbours_count = len(grid.intersection(set(new_cell_neighbours)))
                if (new_cell_active_neighbours_count == 3):
                    cells_to_add.add(neighbour)

            # neighbour already in grid
            else:
                existing_cell_active_neighbours_count += 1
   
        if (existing_cell_active_neighbours_count < 2
                or existing_cell_active_neighbours_count > 3):
            cells_to_remove.add(existing_cell)

    # do our grid updates at the end, since the cell changes are supposed to be simultaneous
    grid.update(cells_to_add)
    grid.difference_update(cells_to_remove)

    return grid       


def process_init(input, grid: set):
    # initialisation grid is 2D, so z coordinate is 0
    # only store active cells in the grid
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (input[y][x] == ACTIVE):
                grid.add(Cell([x, y, 0]))


def process_init_4d(input, grid):
    # initialisation grid is 2D, so z and w coordinates are 0
    # only store active cells in the grid
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (input[y][x] == ACTIVE):
                grid.add(Cell_4d([x, y, 0, 0]))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



