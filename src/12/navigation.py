import sys
import os
import time
from pprint import pp

INPUT_FILE = "input/nav.txt"
SAMPLE_INPUT_FILE = "input/sample_nav.txt"

X = "X"
Y = "Y"
HDG = "HDG"

START_X = 0
START_Y = 0
START_HEADING = 90

location_and_bearing = {
    X: START_X,
    Y: START_Y,
    HDG: START_HEADING
}

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    nav_instructions = read_input(input_file)
    # pp(nav_instructions)

    navigate(nav_instructions)
    new_x = location_and_bearing[X]
    new_y = location_and_bearing[Y]
    manhattan_distance = abs(new_x) + abs(new_y)
    print(f"New location is E {new_x}, N {new_y} with Manhattan distance of {manhattan_distance}")
 

def navigate(instructions):
    for instr in instructions:
        process_instruction(instr)


def process_instruction(instr):
    global location_and_bearing

    instr_type = instr[0]
    instr_mag = int(instr[1:])

    # print(f"Instr is {instr_type} with magnitude: {instr_mag}")

    if (instr_type == 'N'):
        location_and_bearing[Y] = location_and_bearing[Y] + instr_mag
    elif (instr_type == 'S'):
        location_and_bearing[Y] = location_and_bearing[Y] - instr_mag
    elif (instr_type == 'E'):
        location_and_bearing[X] = location_and_bearing[X] + instr_mag
    elif (instr_type == 'W'):
        location_and_bearing[X] = location_and_bearing[X] - instr_mag 
    elif (instr_type == 'R'):
        location_and_bearing[HDG] = convert_angle(location_and_bearing[HDG] + instr_mag)
    elif (instr_type == 'L'):
        location_and_bearing[HDG] =  convert_angle(location_and_bearing[HDG] - instr_mag)
    elif (instr_type == 'F'):
        process_instruction(convert_instr(instr_type, instr_mag))


def convert_instr(instr_type, instr_mag):
    global waypoint
    new_instr_type = ""

    if (location_and_bearing[HDG] == 0):
        new_instr_type = 'N'
    elif (location_and_bearing[HDG] == 90):
        new_instr_type = 'E'
    elif (location_and_bearing[HDG] == 180):
        new_instr_type = 'S'
    elif (location_and_bearing[HDG] == 270):
        new_instr_type = 'W'

    new_instr = new_instr_type + str(instr_mag)

    return new_instr

def convert_angle(angle):
    if (angle < 0):
        angle += 360
    
    return angle % 360


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        codelines = f.read().splitlines()
        
    return codelines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

