import sys
import os
import time
from circular_linked_list import Circular_Linked_List
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
    cups = get_cups(data)
    
    cups = pad_cups(cups, 1000000)
    cups = play_game(cups, 10000000)
    #print(cups)
    first_cup_after_1 = cups.get_node_after(1)
    second_cup_after_1 = cups.get_node_after(first_cup_after_1)

    print(f"The cups are: {first_cup_after_1} and {second_cup_after_1}")
    print(f"The product is: {first_cup_after_1*second_cup_after_1}")


def play_game(cups, iterations):
    iteration = 0
    list_size = cups.get_size()
    while iteration < iterations:
        iteration += 1
        #print(f"\nMove {iteration}")
        current_cup = cups.get_head()
        #print(f"Current cup: {current_cup}")

        # pop 3 clockwise
        pick_up = []
        for i in range(3):
            pick_up.append(cups.pop_after_value(current_cup))

        #print(f"Pick up: {pick_up}")
        #print(cups)

        # min is the lowest cup, excluding any cups in the pickup pile
        # only 3 in the pickup pile, so highest possible min value is 4
        for i in range(1, 5):
            if i not in pick_up:
                min_cup = i
                break

        # max is the highest cup, which is equivalent to the size of the list,
        # not including the 3 in the pickup pile.
        # So, lowest possible value for max is list_size-3
        for i in reversed(range(list_size-3, list_size+1)):
            if i not in pick_up:
                max_cup = i
                break

        destination_cup = current_cup-1
        if (destination_cup < min_cup):
            destination_cup = max_cup
        while (destination_cup in pick_up):
            destination_cup -= 1

        #print(f"Destination cup: {destination_cup}")

        for cup_val in reversed(pick_up):
            cups.insert_after_node(destination_cup, cup_val)

        cups.move_head_after_value(current_cup)
        #print(cups)

    return cups
    

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()

    return data


def get_cups(data):
    cups = Circular_Linked_List()
    for num in data:
        cups.insert_end(int(num))

    return cups

def pad_cups(cups, total_cups):
    for i in range(cups.get_size()+1, total_cups+1):
        cups.insert_end(i)

    return cups

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



