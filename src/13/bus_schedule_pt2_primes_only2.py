import sys
import os
import time
from math import gcd
from operator import itemgetter
from pprint import pprint as pp

INPUT_FILE = "input/bus_schedule.txt"
SAMPLE_INPUT_FILE = "input/sample_schedule.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    # input_file = os.path.join(script_dir, INPUT_FILE)
    input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    buses = split_input(read_input(input_file))
    print(buses)
    
    current_bus = find_aligned_buses(buses)
    print(current_bus)


def lcm(a, b):
    return abs(a*b) // gcd(a, b)


def find_aligned_buses(buses):
    buses_with_offsets = []
    for i, bus in enumerate(buses):
        # here i represents the offset from the departure time, in minutes
        if bus != "x":
            # bus_num (schedule), offset from first bus, alignment time
            buses_with_offsets.append((int(bus), i))

    pp(buses_with_offsets)

    # iterate over buses
    # with each iteration, set current bus to represent schedule that aligns with the buses
    # that we've looked at before.
    # E.g. once we've evaluated buses 7 an 13, this can be represented as a single bus #91.
    current_bus = buses_with_offsets[0]
    for i in range(1, len(buses_with_offsets)):
        current_bus = find_aligned_bus(current_bus, buses_with_offsets[i])
    return current_bus


def find_aligned_bus(bus1, bus2):
    # Two buses will align with periodicity that matches LCM
    # Since our bus schedules are always primes, LCM is simply bus1*bus2
    # We create a new bus that represents the periodicity of these two buses
    # and store the first time bus1 and bus2 align with the required offset.
    # return bus: (bus#=LCM, offset, alignment)
    lcm = bus1[0] * bus2[0]

    # get the first alignment value
    # we only actually need this when returning the last bus
    timestamp = find_init(bus1, bus2)

    print(f"Returning {(lcm, 0, timestamp)}")
    return lcm, 0, timestamp


def find_init(bus1, bus2):
    bus2_relative_delta = bus2[1] - bus1[1]

    timestamp = 0
    while (timestamp + bus2_relative_delta) % bus2[0] != 0:
        # repeat until multiple of bus1 + offset is divisible by bus2 cycle
        # with 7 and 13, this happens at 77 and 168
        timestamp += bus1[0]

    return timestamp
        
        
def split_input(input_data):
    return input_data[1].split(",")


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

