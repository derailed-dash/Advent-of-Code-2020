""" customs_form.py
Author: Darren
Date: 07/12/2020
"""

import sys
import os
import time
from pprint import pprint as pp

CUSTOMS_FORM_INPUT_FILE = "input/customs_answers.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, CUSTOMS_FORM_INPUT_FILE)
    print("Input file is: " + input_file)
    
    group_responses = read_input(input_file)
    sum_any = 0
    sum_all = 0
    for response in group_responses:
        group_members = response["count"]
        group_response = response["group_response"]
        unique_response_chars = set(group_response)
        sum_any += len(unique_response_chars)
        for char in unique_response_chars:
            char_count = group_response.count(char)
            if (char_count == group_members):
                # everyone must have answered yes to this question
                sum_all += 1
    
    print(f"For ALL yes responses in each group, the sum is {sum_all}.")
    print(f"For any yes responses in each group, the sum is {sum_any}.")


def read_input(a_file):
    # group_responses is a list of dictionaries
    # each dictionary is:
    # {count: n, responses: group_response}
    group_responses = []

    with open(a_file, mode="rt") as f:
        group_response = []
        group_members = 0

        for line in f:
            if (line == "\n"):
                # current line is blank, so we've reached the end of the current response group
                group_responses.append({"count": group_members, "group_response": group_response})
                group_response = []
                group_members = 0
                continue

            group_members += 1
            for char in line:
                if (char != "\n"):
                    group_response.append(char)

        group_responses.append({"count": group_members, "group_response": group_response})

    return group_responses


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
