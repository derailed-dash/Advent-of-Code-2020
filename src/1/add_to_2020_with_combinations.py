import sys
import os
import time
import re
from itertools import combinations
from math import prod as prod

INPUT_FILE = "input/expenses.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    print("Input file is: " + input_file)
    entries = read_input(input_file)
    print(entries)

    target = 2020
    determine_terms(entries, target, 2)
    determine_terms(entries, target, 3)


def determine_terms(entries, target, num_terms):
    for num_list in combinations(entries, num_terms):
        the_sum = sum(num_list)
        if the_sum == target:
            print(f"Terms: {num_list}.")
            print(f"And the product is: " + str(prod(num_list)))
            break


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        entries_list = [int(x) for x in f.read().splitlines()]

    return entries_list


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")