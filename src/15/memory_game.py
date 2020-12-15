import sys
import os
import time
import re
from pprint import pprint as pp

INPUT_FILE = "input/starting_numbers.txt"
SAMPLE_INPUT_FILE = "input/sample_starting_numbers.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    game_seed = convert_input_to_list(read_input(input_file))
    pp(game_seed)

    iterations = 30000000
    last_val = play_game(iterations, game_seed)
    print(f"Value = {last_val}")
    

def play_game(iterations, seed):
    last_val = 0
    last_val_positions = {}

    # process seed data, exluding last number
    for count, val in enumerate(seed):
        last_val = val
        last_val_positions[val] = count

    for i in range(len(seed), iterations-1):
        # Add seq diff between this number, and the last time we saw this number
        if (last_val in last_val_positions.keys()):
            previous_index = last_val_positions[last_val]
            last_val_positions[last_val] = i
            new_val = i - previous_index
           
        # otherwise, we've not seen this number before, add 0 to seq
        else:
            new_val = 0
            last_val_positions[last_val] = i            

        # print(f"{i}: {last_val}")
        last_val = new_val        
        
    return last_val


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()
        
    return data


def convert_input_to_list(input_data):
    return [int(x) for x in input_data.split(",")]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

