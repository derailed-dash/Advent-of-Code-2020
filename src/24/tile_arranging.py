
import sys
import os
import time
import re
from pprint import pprint as pp

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
    pp(data)

    tiles = proces_tile_positions(data)
    black_tiles = sum(colour == 'b' for colour in tiles.values())
    print(f"Sum of black tiles: {black_tiles}")


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
            tiles[target_location] = 'b'
        else:
            if tiles[target_location] == 'b':
                tiles[target_location] = 'w'
            else:
                tiles[target_location] = 'b'

    return tiles


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



