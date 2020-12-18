import sys
import os
import time
from cell import *
from pprint import pprint as pp

INPUT_FILE = "input/init_state.txt"
SAMPLE_INPUT_FILE = "input/sample_init_state.txt"

ACTIVE = '#'
INACTIVE = '.'
CYCLES = 6


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    pp(input)

    grid = {}
    # process_init(input, grid)
    process_init_4d(input, grid)

    for i in range(CYCLES):
        print(f"Cycle {i}:")
        grid = execute_cycle(grid)

    sum_active = sum([1 for x in grid if grid[x] == ACTIVE])
    print(f"Sum active: {sum_active}")


def execute_cycle(grid):
    new_grid = grid.copy()

    for existing_cell in grid:
        neighbours_of_existing_cell = existing_cell.get_neighbours()
        existing_cell_active_neighbours_count = 0
        for neighbour in neighbours_of_existing_cell:
            # neighbour not yet in grid
            # we need to add it, so we need to determine its own neighbours
            if neighbour not in grid:        
                new_cell_neighbours = neighbour.get_neighbours()
                new_cell_active_neighbours_count = 0
                for neighbour_of_new_cell in new_cell_neighbours:
                    if neighbour_of_new_cell in grid:
                        if (grid[neighbour_of_new_cell] == ACTIVE):
                            new_cell_active_neighbours_count += 1 
                
                if (new_cell_active_neighbours_count == 3):
                    new_grid[neighbour] = ACTIVE
                else:
                    new_grid[neighbour] = INACTIVE

            # neighbour already in grid
            else:
                if grid[neighbour] == ACTIVE:
                    existing_cell_active_neighbours_count += 1

        if grid[existing_cell] == ACTIVE:   
            if (existing_cell_active_neighbours_count < 2
                    or existing_cell_active_neighbours_count > 3):
                new_grid[existing_cell] = INACTIVE
        else:
            if existing_cell_active_neighbours_count == 3:
                new_grid[existing_cell] = ACTIVE

    return new_grid       


def process_init(input, grid):
    for y in range(len(input)):
        for x in range(len(input[y])):
            cell = Cell([x, y, 0])
            grid[cell] = input[y][x]


def process_init_4d(input, grid):
    for y in range(len(input)):
        for x in range(len(input[y])):
            cell = Cell_4d([x, y, 0, 0])
            grid[cell] = input[y][x]


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



