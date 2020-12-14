import sys
import os
import time
import re
from pprint import pprint as pp

INPUT_FILE = "input/docking_program.txt"
SAMPLE_INPUT_FILE = "input/sample_docking_program.txt"

ADDR_SIZE = 36
INSTR_PATTERN = re.compile(r"mem\[(\d+)")


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    #pp(input)
    
    v1_mem_values, updated_addresses = process_input(input)
    # pp(v1_mem_values)
    sum_of_values = sum(v1_mem_values.values())
    print(f"Sum of v1 mem values = {sum_of_values}")

    sum_of_updated_addresses = sum(updated_addresses.values())
    print(f"Sum of v2 updated address values = {sum_of_updated_addresses}")

def process_input(data):
    INSTR_MASK = "mask"

    v1_mem_values = {}
    updated_addresses = {}
    current_mask = None

    for line in data:
        instr, value = [x.strip() for x in line.split("=")]
        if (instr == INSTR_MASK):
            current_mask = value
            #pp(current_mask)
        else:
            addr, new_val = process_mem_update_v1(instr, value, get_mask_as_dict(current_mask))
            v1_mem_values[addr] = new_val

            updated_addresses.update(process_mem_update_v2(instr, value, current_mask))

    return v1_mem_values, updated_addresses


def get_mask_as_dict(value):
    mask = {}

    # process the bit mask from right to left
    for i in reversed(range(len(value))):
        mask[(len(value)-1)-i] = value[i]

    return mask


def convert_to_bin_rep(addr):
    int_addr = int(addr)

    # get a str binary representation that's 36 chars long
    return format(int_addr, "036b")


def process_mem_update_v2(instr, value, mask):
    # Modify the address being written to, using a mask
    # The data to be written is not modified by the mask
    # Multiple addresses can be written

    # Regex to extract the memory address
    addr = int(INSTR_PATTERN.findall(instr)[0])

    # First, get binary equivalent of address supplied
    # bin converts to binary string equivalent, prefixd with 0b.
    # we need to strip off 0b
    bin_addr = bin(addr)[2:]
    bin_addr_list = list(bin_addr.zfill(36))
    # print(f"Addr: {addr}, {bin_addr}")

    # placeholder for masked address
    intermediate_addr = ADDR_SIZE * ["0"]

    # This is the easy bit.
    # zip creates tuples from mask and addr
    # E.g. if mask[0] is X and bin_addr_list[0] is 0, then the zip is ('X', '0')
    # These are then unpacked into mark_char and addr_char
    for i, (mask_char, addr_char) in enumerate(zip(mask, bin_addr_list)):
        if (mask_char == 'X'):
            # intermediate address includes our floating X
            intermediate_addr[i] = 'X'
        elif (mask_char == '1'):
            # intermediate address set to 1
            intermediate_addr[i] = '1'
        elif (mask_char == '0'):
            # intermediate address set to addr
            intermediate_addr[i] = addr_char

    num_X = intermediate_addr.count("X")
    num_perms = (2**num_X)
    perms = []

    # build up a list of perms. E.g. if 3 Xs in mask ending 000X0XX:
    # [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], etc
    for i in range(num_perms):
        perms.append(list(bin(i)[2:].zfill(num_X)))

    addresses_to_update = {}

    # iterate through permutations
    # E.g. perm = [0, 0, 0]
    # E.g. replace three Xs with three 0s
    # Then replace three Xs with 0, 0, 1
    # Etc
    for perm in perms:
        i = 0
        new_addr = ""
        for addr_char in intermediate_addr:
            if addr_char == "X":
                # substitute our permutation for X
                new_addr += str(perm[i])

                # increment the permutation
                i += 1
            else:
                new_addr += addr_char

        new_addr_dec = int(new_addr, 2)
        addresses_to_update[new_addr_dec] = int(value)
        
    return addresses_to_update


def process_mem_update_v1(instr, value, mask):
    # Modify the data being written to the address using a mask
    # The mask changes the bit in the address being written.

    # Regex to extract the memory address
    addr = INSTR_PATTERN.findall(instr)[0]
    new_val = int(value)

    # If mask=0, 0 is written at this bit
    # If mask=1, 1 is written at this bit.
    # If mask=x, no change to data being written
    for bit in mask.keys():
        if (mask[bit] == '1'):
            new_val = new_val | (1<<bit)
        elif (mask[bit] == '0'):
            new_val = new_val & ~(1<<bit)

    return addr, new_val


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

