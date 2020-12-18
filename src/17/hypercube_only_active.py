import sys
import os
import time
from cell import *
from pprint import pprint as pp

INPUT_FILE = "input/init_state.txt"
SAMPLE_INPUT_FILE = "input/sample_init_state.txt"

ACTIVE = '#'
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

    grid = set()
    process_init_4d(input, grid)

    for i in range(CYCLES):
        print(f"Cycle {i}:")
        grid = execute_cycle(grid)

    sum_active = len(grid)
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
                new_cell_active_neighbours_count = len(grid.intersection(set(new_cell_neighbours)))
                if (new_cell_active_neighbours_count == 3):
                    new_grid.add(neighbour)

            # neighbour already in grid
            else:
                existing_cell_active_neighbours_count += 1
   
        if (existing_cell_active_neighbours_count < 2
                or existing_cell_active_neighbours_count > 3):
            new_grid.remove(existing_cell)

    return new_grid       


def process_init(input, grid: set):
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (input[y][x] == ACTIVE):
                grid.add(Cell([x, y, 0]))


def process_init_4d(input, grid):
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



