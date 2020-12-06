""" Add_to_2020.py
Author: Darren
Date: 05/12/2020

Process a list of numbers, and determine which two numbers add up to 2020.
Process a list of numbers and determine which three numbers add up to 2020.

The toboggan moves x right and y down for each iteration.
"""

import sys
import os

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        global entries_list
        entries_list = f.read().splitlines()

def total_of_two():
    for i in range(len(entries_list)):
        for j in range(i+1, len(entries_list)):
            the_sum = int(entries_list[i]) + int(entries_list[j])
            if (the_sum == target):
                print(f"The sum of {entries_list[i]} and {entries_list[j]} is: " + str(the_sum))
                print(f"And the product is: " + str(int(entries_list[i])*int(entries_list[j])))


def total_of_three():
    for i in range(len(entries_list)):
        for j in range(i+1, len(entries_list)):
            sum_so_far = int(entries_list[i]) + int(entries_list[j])
            if (sum_so_far >=target):
                # we've already exceeded target with just two numbers
                continue
            
            for k in range(j+1, len(entries_list)):
                the_sum = sum_so_far + int(entries_list[k])
                if (the_sum == target):
                    print(f"The sum of {entries_list[i]} and {entries_list[j]} and {entries_list[k]} is: " + str(the_sum))
                    print(f"And the product is: " + str(int(entries_list[i])*int(entries_list[j])*int(entries_list[k])))
                    return


target = 2020
the_sum = 0

# get absolute path where script lives
script_dir = os.path.dirname(__file__) 

# path of input file
input_file = os.path.join(script_dir, "input/expenses.txt")
print("Input file is: " + input_file)
read_input(input_file)
print("File read.")

# print(entries_list)
print("Looking for two numbers that total " + str(target))
total_of_two()

print("Looking for three numbers that total " + str(target))
total_of_three()



