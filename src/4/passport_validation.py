""" Passport_Validation.py
Author: Darren
Date: 06/12/2020

Process K:V pairs to determine if passport is valid
"""

import sys
import os
import time
from pprint import pprint as pp

PASSPORT_INPUT_FILE = "input/passports.txt"

BIRTH_YEAR = "byr"
ISSUE_YEAR = "iyr"
EXP_YEAR = "eyr"
HEIGHT = "hgt"
HAIR_COLOR = "hcl"
EYE_COLOR = "ecl"
PASSPORD_ID = "pid"
COUNTRY_ID = "cid"

count_passports_processed = 0
count_passports_valid = 0
count_passports_invalid = 0

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, PASSPORT_INPUT_FILE)
    print("Input file is: " + input_file)
    
    passports = read_input(input_file)
    print("File read.")

    list_of_passport_dicts = process_passports(passports)
    pp(list_of_passport_dicts)

    dict_keys = [
        BIRTH_YEAR,
        ISSUE_YEAR,
        EXP_YEAR,
        HEIGHT,
        HAIR_COLOR,
        EYE_COLOR,
        PASSPORD_ID,
        COUNTRY_ID
    ]

    validate_passports(list_of_passport_dicts, dict_keys)

    print("Total passwords processed: " + str(count_passports_processed))
    print("Total passwords valid: " + str(count_passports_valid))
    print("Total passwords invalid: " + str(count_passports_invalid))

def validate_passports(passports, keys):
    global count_passports_invalid, count_passports_valid, count_passports_processed
    
    for passport in passports:
        count_passports_processed += 1

        for k in keys:
            passport_valid = True

            if k not in passport:
                if (k == COUNTRY_ID):
                    # we're going to ignore this!
                    continue
                else:
                    # invalid
                    passport_valid = False
                    break
            else:
                # let's validate the value
                # TBC
                pass
                    
        if (passport_valid):
            count_passports_valid += 1
        else:
            count_passports_invalid += 1


def process_passports(passports):
    list_of_passport_dicts = []

    for row in passports:
        passport = dict(x.split(":") for x in row.split(" "))
        list_of_passport_dicts.append(passport)

    return list_of_passport_dicts


def read_input(a_file):
    # first build a list, where each row contains a single passport
    with open(a_file, mode="rt") as f:
        passports = []
        current_passport = ""
        
        for line in f:
            if (line == "\n"):
                # add current row to passports list
                passports.append(current_passport.rstrip(" "))
                current_passport = ""
            else:
                # build current password string by appending lines
                current_passport += line.rstrip("\n") + " "
    
        if (current_passport != ""):
            passports.append(current_passport.rstrip(" "))

    return passports


"""
def read_input(a_file):
    
    with open(a_file, mode="rt") as f:
        passports = []

        # dictionary for current passport
        current_passport = {}

        for line in f:
            if (line == "\n"):
                # add current passport dict to passports list
                passports.append(current_passport)
                current_passport = {}
            else:
                # split current line into K:V entries
                entries = line.rstrip("\n").split(" ")

                # each entry will be in K:V format
                for entry in entries:
                    entry_pair = entry.split(":")
                    current_passport = {entry_pair[0], entry_pair[1]}

            passports.append(current_passport)
    
    return passports
"""

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
