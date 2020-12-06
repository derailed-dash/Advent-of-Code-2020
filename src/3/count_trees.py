""" Count how many trees on the toboggan journey from top left to bottom, 
where # denotes a tree, and . denotes empty space.

The toboggan moves x right and y down for each iteration.
"""

import sys
import os
import math
from pprint import pprint as pp

INPUT_TREEMAP_FILE = "input/treemap.txt"
OUTPUT_TREEMAP_FILE = "output/treemap.txt"
NAVIGATED_TREEMAP_FILE = "output/navigated_treemap.txt"

x_movement = 1
y_movement = 1


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_TREEMAP_FILE)
    print("Input file is: " + input_file)

    output_file = os.path.join(script_dir, OUTPUT_TREEMAP_FILE)
    print("Output file is: " + output_file)

    treemap = get_treemap(input_file)
    write_treemap(output_file, treemap)
   
    output_file = os.path.join(script_dir, NAVIGATED_TREEMAP_FILE)
    navigated_treemap = navigate_treemap(treemap)
    write_treemap(output_file, navigated_treemap)


def write_treemap(a_file, treemap):
    with open(a_file, 'w') as f:
        for row in treemap:
            f.write(row + "\n")


def get_treemap(a_file):
    with open(a_file, mode="rt") as f:
        
        # get the width of the map
        # strip off the newline character
        treemap_cols = len(f.readline()) - 1

        # get the number of rows in the map
        # add 1, since we've already read one row
        treemap_rows = len(f.readlines()) + 1

        print("Treemap rows: " + str(treemap_rows))
        print("Treemap cols: " + str(treemap_cols))
        
        # decide how many horizontal repeats we need, based on tobogan movement
        # i.e. for every (y), we need (x) horizontal characters
        min_width = math.ceil(treemap_rows/y_movement) * x_movement
        print("Min width: " + str(min_width))
        horizontal_repeats = math.ceil(min_width / treemap_cols)
        print("Horizontal repeats needed: " + str(horizontal_repeats))

        # Go back to the beginning of the file
        f.seek(0)
        treemap = [] 
         
        for line in f.readlines():
            line_to_add = horizontal_repeats * line.rstrip('\n')
            treemap.append(line_to_add)

    return treemap


def navigate_treemap(treemap):
    TREE = '#'
    TREE_HIT = 'X'
    TREE_MISS = 'O'

    trees_hit = 0
    
    # x, y coordinates
    posn = [1, 1]

    # let's create a new treemap, and update it with the hit/miss markers
    navigated_treemap = treemap[:]    
    
    while (posn[1] <= len(treemap)):
        # Now obtain the treemap row [y-1], and the treemap index [x-1], and see what it is.
        if ((posn[1]-1) <= len(navigated_treemap)):
            try:
                at_location = navigated_treemap[posn[1]-1][posn[0]-1]
                # print(f"Current position {posn}:" + navigated_treemap[posn[1]-1][posn[0]-1])

                # Now update our treemap with hit or miss
                newrow = list(navigated_treemap[posn[1]-1])

                if (at_location == TREE):
                    trees_hit = trees_hit + 1
                    newrow[posn[0]-1] = TREE_HIT
                    navigated_treemap[posn[1]-1] = "".join(newrow)
                else:
                    newrow[posn[0]-1] = TREE_MISS
                    navigated_treemap[posn[1]-1] = "".join(newrow)
            except IndexError:
                print("Error")
                print(posn)

        posn[0] = posn[0] + x_movement
        posn[1] = posn[1] + y_movement

    print("Bottom reached.")
    print(f"We have hit {trees_hit} trees")
    
    return navigated_treemap


if __name__ == "__main__":
    try:
        x_movement = int(input("Enter x movement: "))
        y_movement = int(input("Enter y movement: "))

        main()
    except ValueError:
        print("Movement must be an integer value")




