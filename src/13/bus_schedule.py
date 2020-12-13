import sys
import os
import time
from operator import itemgetter
from pprint import pp

INPUT_FILE = "input/bus_schedule.txt"
SAMPLE_INPUT_FILE = "input/sample_schedule.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input_data = read_input(input_file)
    target, bus_sched = split_input(input_data)

    bus = process_schedule(target, bus_sched)
    bus_num = bus[0]
    bus_time = bus[1]
    print(f"Earliest available bus: {bus[0]} at time {bus[1]}")
    print(f"Solution answer: {(bus_time - target) * bus_num}")


def process_schedule(target, sched):
    buses = {}

    for bus in sched:
        # e.g. 7
        if bus.isnumeric():
            bus_sched = int(bus)
            buses[bus_sched] = compute_first_available_time(target, bus_sched)

    return min(buses.items(), key=itemgetter(1))


def compute_first_available_time(target, bus_sched):
    time = 0
    while True:
        time += bus_sched
        if (time >= target):
            return time
    

def split_input(input_data):
    bus_sched = input_data[1].split(",")
    return int(input_data[0]), bus_sched


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        codelines = f.read().splitlines()
        
    return codelines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

