""" Password_Validation_Match_Posn.py
Author: Darren
Date: 05/12/2020

Process list of rows from a file, where each row contains pwd policy and pwd.
Pwd is only valid if the indicated character is found in either the first numbered
OR second numbered position.  It is not valid if the character is found in both positions.
The password policy is 1-indexed.

E.g. 5-7 z: qhcgzzz
This pwd is invalid, since z is found in BOTH position 5 and position 7.
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
    first_posn, _, last_posn = char_counts.partition("-")
    
    #print("Char match: " + char_match)
    #print("First posn: " + first_posn)
    #print("Last posn: " + last_posn)
    #print("Pwd: " + pwd)
    #print("Pwd length: " + str(len(pwd)))

    if(int(last_posn) > len(pwd)):
        #print("Password too short")
        return False

    first_posn_match = False
    second_posn_match = False

    if (pwd[int(first_posn)-1] == char_match):
        #print("Matching char found at position " + str(int(first_posn)-1))
        first_posn_match = True
        
    if (pwd[int(last_posn)-1] == char_match):
        #print("Matching char found at position " + str(int(last_posn)-1))
        second_posn_match = True

    # Only valid if first OR second match, i.e. XOR
    if (first_posn_match ^ second_posn_match):
        return True

    return False


if __name__ == "__main__":
    main()



