""" Process list of rows from a file, where each row contains pwd policy and pwd.
Pwd is only valid if the indicated character is found between x and y times (inclusive) in the pwd.

E.g. 5-7 z: qhcgzzz
This pwd is invalid, since z is only found 3 times, but minimum is 5.
"""

import sys
import os

pwd_file = "input/pwd_file.txt"
pwd_list = []
count_pwds_processed = 0
count_pwds_valid = 0
count_pwds_invalid = 0

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, pwd_file)
    print("Input file is: " + input_file)
    
    read_input(input_file)
    print("File read.")

    for pwd_row in pwd_list:
        global count_pwds_processed, count_pwds_valid, count_pwds_invalid
        count_pwds_processed = count_pwds_processed + 1
        if password_okay(pwd_row):
            count_pwds_valid = count_pwds_valid + 1
        else:
            count_pwds_invalid = count_pwds_invalid + 1

    print("Total passwords processed: " + str(count_pwds_processed))
    print("Total passwords valid: " + str(count_pwds_valid))
    print("Total passwords invalid: " + str(count_pwds_invalid))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        global pwd_list
        pwd_list = f.read().splitlines()


def password_okay(pwd_row):
    pwd_policy_and_pwd = [item.strip() for item in pwd_row.split(":")]
    #print(pwd_policy_and_pwd)

    pwd = pwd_policy_and_pwd[1]
    char_counts, _, char_match = pwd_policy_and_pwd[0].partition(" ")
    min_chars, _, max_chars = char_counts.partition("-")
    
    #print("Char match: " + char_match)
    #print("Min chars: " + min_chars)
    #print("Max chars: " + max_chars)
    #print("Pwd: " + pwd)

    actual_char_count = pwd.count(char_match)
    if (actual_char_count < int(min_chars)):
        #print("Password invalid: too few matching chars")
        return False

    if (actual_char_count > int(max_chars)):
        #print("Password invalid: too few matching chars")
        return False

    return True


if __name__ == "__main__":
    main()



