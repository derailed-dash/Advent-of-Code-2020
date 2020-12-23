import sys
import os
import time
import re
from tile import Tile
from pprint import pprint as pp

INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    # input_file = os.path.join(script_dir, INPUT_FILE)
    input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    data = read_input(input_file)

    # get dict of tiles
    tiles = process_data(data)
    for tile_ids in tiles:
        current_tile = tiles[tile_ids]
        print(current_tile)
        print(f"Edge values: {current_tile.get_edge_values()}")
        print("\n".join(current_tile.get_inner()))
        break
    
    # part 1
    corners = get_corners(tiles)
    print(f"Corners: {corners}")

    # build whole map
    tile_rows = build_map(tiles, corners)
    pp(tile_rows)


def make_uber_tile(tile_rows):
    # for each tile row
    #   join all the inner rows to make uber rows
    # use these to create a new uber tile
    pass


def build_map(tiles, corners):
    tile_rows = []
    current_tile_row = []

    # initially set a placeholder for this
    # once we find the first rh corner, we'll put in proper row length
    max_row_length = len(tiles)

    # start with first corner
    current_tile_id = corner_id = find_first_corner(corners, tiles)
    current_tile_row.append(corner_id)
    other_tiles = list(tiles.keys()).copy()
    
    current_tile = tiles[corner_id]
    next_tile_down = None

    # now add in all the tiles...
    while len(other_tiles) > 1:
        # eliminate current tile from tiles we're searching through
        other_tiles.remove(current_tile_id)

        # if the current tile is the first in the row
        # then let's find the one underneath for the next row
        if len(current_tile_row) == 1:
            # set to None if we don't find a match. I.e if we're on the last row.
            next_tile_down = None
            current_tile_bottom_value = current_tile.edge_value(current_tile.get_bottom_edge())
            for other_tile_id in other_tiles:
                other_tile = tiles[other_tile_id]
                if current_tile_bottom_value in other_tile.get_edge_values():
                    # the other tile is a match.  We need to find the right orientation
                    other_tile_configs = other_tile.get_configurations()
                    for other_tile_config in other_tile_configs:
                        if current_tile.get_bottom_edge() == other_tile_config.get_top_edge():
                            # update the tiles dict with new tile orientation and break
                            tiles[other_tile_id] = other_tile_config  
                            next_tile_down = other_tile_id
                            break 
                    break
                                                       

        # look for tile that matches our current right edge
        current_tile_right_value = current_tile.edge_value(current_tile.get_right_edge())
        for other_tile_id in other_tiles:
            other_tile = tiles[other_tile_id]
            if current_tile_right_value in other_tile.get_edge_values():
                # the other tile is a match.  We need to find the right orientation
                other_tile_configs = other_tile.get_configurations()
                for other_tile_config in other_tile_configs:
                    if current_tile.get_right_edge() == other_tile_config.get_left_edge():
                        # update the tiles dict with new tile orientation and break
                        tiles[other_tile_id] = other_tile_config
                        break
                
                # add matched tile to the grid
                current_tile_row.append(other_tile_id)
                
                # check if we've reached a corner
                if other_tile_id in corners:
                    # set the proper row length
                    max_row_length = len(current_tile_row)
                
                # if our row has reached the row length, time to start a new row
                if len(current_tile_row) == max_row_length:
                    # we're done with this row                  
                    tile_rows.append(current_tile_row)
                    current_tile_row = []
                    if (next_tile_down is not None):
                        other_tiles.remove(other_tile_id)
                        current_tile_id = next_tile_down
                        current_tile = tiles[current_tile_id]
                        current_tile_row.append(current_tile_id)
                else:
                    # make our current tile the last one we added
                    current_tile_id = other_tile_id
                    current_tile = tiles[current_tile_id]

                # we found a matching tile, so move on to next iteration
                break   
    
    return tile_rows


def find_first_corner(corners, tiles):
    for corner in corners:
        current_tile_id = corner
        current_tile = tiles[current_tile_id]
        other_tiles_ids = list(tiles.keys()).copy()
        other_tiles_ids.remove(current_tile_id)

        right_and_bottom = []
        right_and_bottom.append(current_tile.edge_value(current_tile.get_right_edge()))
        right_and_bottom.append(current_tile.edge_value(current_tile.get_bottom_edge()))

        matched_edges = 0
        for other_tile_id in other_tiles_ids:
            other_tile = tiles[other_tile_id]
            for edge_value in right_and_bottom:
                if edge_value in other_tile.get_edge_values():
                    matched_edges += 1

        if matched_edges == 2:
            break
    return corner

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

    # dict of tiles, in the format {id: Tile, id: Tile...}
    return tiles


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



