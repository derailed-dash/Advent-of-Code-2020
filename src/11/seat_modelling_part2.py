import sys
import os
import time
from pprint import pprint as pp

INPUT_FILE = "input/seating.txt"
SAMPLE_INPUT_FILE = "input/sample_seating.txt"

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'

MAX_OCCUPIED = 5
MAX_VISIBLE = 8

# each adjacent seat position, expressed as relative [row][seat]
SEATS_TO_TEST = {
    'UL': [-1, -1],
    'UM': [-1, 0],
    'UR': [-1, 1],
    'ML': [0, -1],
    'MR': [0, 1],
    'LL': [1, -1],
    'LM': [1, 0],
    'LR': [1, 1],
}

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    seating = read_input(input_file)
    # pp (seating)

    last_seating = seating
    count = 0
    while True:
        count += 1
        new_seating = process_seating_rules(last_seating)

        if (new_seating == last_seating):
            print(f"Iteration {count}: Seating layout has not changed.")
            print(f"Seats occuped = {count_occupied(new_seating)}")
            break

        last_seating = new_seating        
    

def count_occupied(seating):
    occupied_count = 0

    for row in seating:
        occupied_count += row.count(OCCUPIED)

    return occupied_count


def process_seating_rules(seating):
    # if seat is empty and no adjacent seats are occupied, this becomes occupied
    # note: everyone sits at the same time, so we only need to consider seating plan at the start of the iteration
    # I.e. if the seat to the left is filled on *this* iteration, we ignore it.

    new_seating = seating.copy()

    for row_num, row in enumerate(seating):
        for seat_num, seat in enumerate(row):

            visible_occupied = 0

            if seat != FLOOR:

                # check each of the eight dimensions
                # iterate through UL, UM, UR, LL, etc
                for visible_seat in SEATS_TO_TEST.keys():
                    # set seat location to current seat
                    # then we'll move away from it, one x,y vector at a time
                    adjacent_seat_row_num = row_num
                    adjacent_seat_col_num = seat_num

                    counter = 0
                    while True:
                        counter += 1
                        adjacent_seat_row_num += SEATS_TO_TEST[visible_seat][0]
                        adjacent_seat_col_num += SEATS_TO_TEST[visible_seat][1]

                        if (adjacent_seat_row_num < 0 or adjacent_seat_row_num >= len(seating)):
                            break

                        if (adjacent_seat_col_num < 0 or adjacent_seat_col_num >= len(row)):
                            break

                        nearest_visible_seat = seating[adjacent_seat_row_num][adjacent_seat_col_num]
                        if (nearest_visible_seat) != FLOOR:
                            if (nearest_visible_seat == OCCUPIED):
                                visible_occupied += 1
                            
                            # we don't need to go any further in this dimension
                            break
                
                if seat == EMPTY:
                    if (visible_occupied == 0):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + OCCUPIED + new_seating[row_num][seat_num+1:]
                elif seat == OCCUPIED:
                    if (visible_occupied >= MAX_OCCUPIED):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + EMPTY + new_seating[row_num][seat_num+1:]

    # pp(new_seating)
    return new_seating


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

