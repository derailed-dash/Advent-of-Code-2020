import sys
import os
import time
import re
from tile import Tile
from collections import deque
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

    # get dict of tiles
    tiles = process_data(data)
    for tile_ids in tiles:
        current_tile = tiles[tile_ids]
        print(current_tile)
        print(f"Edge values: {current_tile.get_edge_values()}")
        break
    
    # part 1
    corners = get_corners(tiles)
    print(f"Corners: {corners}")


def get_corners(tiles):
    corners = []

    tile_ids = list(tiles.keys())

    for i in range(len(tile_ids)):
        tile_id = tile_ids[i]
        current_tile = tiles[tile_id]

        count_matches = 0

        other_tile_ids = tile_ids.copy()
        other_tile_ids.remove(tile_id)

        for other_tile_id in other_tile_ids:
            other_tile = tiles[other_tile_id]

            if match_tile_edges(current_tile, other_tile):
                count_matches += 1
    
        if (count_matches == 2):
            corners.append(tile_id)

    return corners


def match_tile_edges(current_tile, other_tile):
    for edge_value in current_tile.get_edge_values():
        if edge_value in other_tile.get_edge_values():
            return True

    return False   


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()

    return data


def process_data(data):
    id_matcher = re.compile(r"^\D+ (\d+):")

    raw_tiles = data.split("\n\n")
    tiles = {}
    tile = []
    for raw_tile in raw_tiles:
        tile = raw_tile.splitlines()
        match = id_matcher.match(tile[0])
        if match:
            # group(0) is the entire regex match; group(1) is the ID
            id = int(match.group(1))
            tile.pop(0)

        tiles[id] = Tile(tile)

    return tiles


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



