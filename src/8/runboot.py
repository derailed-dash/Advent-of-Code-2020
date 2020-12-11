import sys
import os
import time
from pprint import pp

BOOT_CODE_INPUT_FILE = "input/bootcode.txt"

sample_code = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "jmp -4",
    "acc +6"
]

ACC = "acc"
JMP = "jmp"
NOP = "nop"

instruction_ptr = 0
accumulator = 0
instructions_processed = []

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, BOOT_CODE_INPUT_FILE)
    print("Input file is: " + input_file)

    code = read_input(input_file)
    #code = sample_code

    success = run_code(code)
    if (success):
        print(f"Execution completed. Accumulator: {accumulator}")
    else:
        print(f"Execution could not complete. Accumulator: {accumulator}")

    success = try_substitutions(code)


def try_substitutions(code):
    substitutions_tried = 0
    
    for index, line in enumerate(code):
        substituted_code = code.copy()

        substituted = False
        if (JMP in line):
            substituted_code[index] = str(line).replace(JMP, NOP)
            substituted = True
        
        if (NOP in line):
            substituted_code[index] = str(line).replace(NOP, JMP)
            substituted = True

        if (substituted):
            substitutions_tried += 1
            print(f"Substituting at line {index+1}, instruction: {line} -> {substituted_code[index]}")
            success = run_code(substituted_code)
            if (success):
                print(f"Program terminates successfully on iteration {substitutions_tried}. Accumulator value is: {accumulator}.")
                return True

    return False


def get_line(a_ptr):
    return a_ptr + 1
    

def run_code(code):
    global accumulator, instruction_ptr

    instruction_ptr = 0
    accumulator = 0
    instructions_processed = []

    while True:
        if (instruction_ptr in instructions_processed):
            print(f"[Step {len(instructions_processed) + 1}]: We've done instruction {instruction_ptr + 1} before!")
            return False

        if (instruction_ptr >= len(code)):
            print(f"[Step {len(instructions_processed) + 1}]: EOF!")
            return True

        instructions_processed.append(instruction_ptr)
        process_instruction(code, instruction_ptr)


def process_instruction(code, ptr):
    global instruction_ptr, accumulator

    instruction, value = code[ptr].split()
    # print(f"[Step {len(instructions_processed)}, line {instruction_ptr + 1}]: Executing {instruction} {value}")

    if (instruction == ACC):
        accumulator += int(value)
        instruction_ptr += 1
    elif (instruction == NOP):
        instruction_ptr += 1
    elif (instruction == JMP):
        instruction_ptr += int(value)



def read_input(a_file):
    with open(a_file, mode="rt") as f:
        codelines = f.read().splitlines()
        
    return codelines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

