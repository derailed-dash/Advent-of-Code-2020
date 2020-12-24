
import sys
import os
import time
import re
import copy
from pprint import pprint as pp
from hex import Hexagon

INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    data = read_input(input_file)

    tiles = proces_tile_positions(data)
    black_tiles = sum(hex.get_colour() == 'b' for hex in tiles.values())
    print(f"Sum of black tiles: {black_tiles}")

    tiles = living_art(tiles, 100)
    black_tiles = sum(hex.get_colour() == 'b' for hex in tiles.values())    
    print(f"Sum of black tiles: {black_tiles}")

def pad_missing_tiles(tiles):
    tile_locations = tiles.keys()
    max_x = min_x = 0
    max_y = min_y = 0

    for loc in tile_locations:
        current_x = loc[0]
        current_y = loc[1]        
        max_x = max(max_x, current_x)
        min_x = min(min_x, current_x)
        max_y = max(max_y, current_y)
        min_y = min(min_y, current_y)

    for x in range(min_x - 2, max_x + 3):
        for y in range(min_y - 2 , max_y + 3):
            locn = tuple([x, y])

            if locn not in tiles:
                tiles[locn] = Hexagon()

    return


def living_art(tiles, iterations):
    iteration = 0

    while (iteration < iterations):
        iteration += 1
        pad_missing_tiles(tiles)
        old_tiles = tiles.copy()

        for tile_location, tile in old_tiles.items():
            neighbours = tile.get_neighbours(tile_location)
            black_neighbours = 0
            for neighbour_location in neighbours:
                if neighbour_location in old_tiles:
                    if old_tiles[neighbour_location].get_colour() == 'b':
                        black_neighbours += 1

            if tile.get_colour() == 'b':
                # print(f"Black tile {tile_location} has {black_neighbours} black neighbours.")
                if black_neighbours == 0 or black_neighbours > 2:
                    # print("Flipping")
                    tiles[tile_location] = Hexagon('w')
            else:
                # white tile
                if black_neighbours == 2:
                    tiles[tile_location] = Hexagon('b')

    return tiles


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read().splitlines()

    return data


def proces_tile_positions(data):
    tokenizer = re.compile(r'(ne|e|se|sw|w|nw)')

    # store tiles as { [x,y]: 'b', [x,y]: 'w', etc}
    tiles = {}

    for tile in data:
        tokens = tokenizer.findall(tile)
        location_x = 0
        location_y = 0
        for token in tokens:
            if token == 'ne':
                location_x += 1
                location_y += 1
            elif token == 'e':
                location_x += 2
            elif token == 'se':
                location_x += 1
                location_y -= 1
            elif token == 'sw':
                location_x -= 1
                location_y -= 1
            elif token == 'w':
                location_x -= 2
            elif token == 'nw':
                location_x -= 1
                location_y += 1
        
        target_location = tuple([location_x, location_y])
        if target_location not in tiles:
            tiles[target_location] = Hexagon('b')
        else:
            tiles[target_location].flip()

    return tiles


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



