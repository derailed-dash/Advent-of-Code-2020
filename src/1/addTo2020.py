""" Add_to_2020.py
Author: Darren
Date: 05/12/2020

Process a list of numbers, and determine which two numbers add up to 2020.
Process a list of numbers and determine which three numbers add up to 2020.

The toboggan moves x right and y down for each iteration.
"""

import sys
import os
import time

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        global entries_list
        entries_list = [int(x) for x in f.read().splitlines()]


def total_of_two(target):
    iterations = 0
    for i, num1 in enumerate(entries_list):
        for num2 in entries_list[i+1:]:
            iterations += 1
            the_sum = num1 + num2
            if (the_sum == target):
                print(f"The sum of {num1} and {num2} is: " + str(target))
                print(f"And the product is: " + str(num1* num2))
                print(f"{iterations} iterations required.")


def total_of_three(target):
    iterations = 0
    for i, num1 in enumerate(entries_list):
        for j, num2 in enumerate(entries_list[i+1:]):
            iterations += 1
            sum_so_far = num1 + num2
            if (sum_so_far >=target):
                # we've already exceeded target with just two numbers
                continue
            
            for num3 in entries_list[j+1:]:
                iterations += 1
                the_sum = sum_so_far + num3
                if (the_sum == target):
                    print(f"The sum of {num1} and {num2} and {num3} is: " + str(the_sum))
                    print(f"And the product is: " + str(num1*num2*num3))
                    print(f"{iterations} iterations required.")
                    return


target = 2020

# get absolute path where script lives
script_dir = os.path.dirname(__file__) 

# path of input file
input_file = os.path.join(script_dir, "input/expenses.txt")
print("Input file is: " + input_file)
read_input(input_file)
print("File read.")

# print(entries_list)
print("Looking for two numbers that total " + str(target))
t1 = time.perf_counter()
total_of_two(target)
t2 = time.perf_counter()
print(f"Execution time: {t2 - t1:0.4f} seconds")

print("Looking for three numbers that total " + str(target))
t1 = time.perf_counter()
total_of_three(target)
t2 = time.perf_counter()
print(f"Execution time: {t2 - t1:0.4f} seconds")


