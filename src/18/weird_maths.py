import sys
import os
import time
import re
from pprint import pprint as pp

INPUT_FILE = "input/math_puzzle.txt"
SAMPLE_INPUT_FILE = "input/test_math_puzzle.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    # pp(input)
    
    results = process_input(input)
    pp(results)
    print(f"Sum of results: {sum(results)}")


def process_input(input):
    tokenizer = re.compile(r'\s*([()+*/-]|\d+)')

    results = []

    for line in input:
        # first, let's get all our tokens.  I.e. operators and digits.
        # Match 0 or more spaces, followed by capture group 1, which is:
        # any character set of 1 or more ()+*/- as operator tokens OR any digit
        expr_tokens = []
   
        current_pos = 0
        while current_pos < len(line):
            match = tokenizer.match(line, current_pos)
            # we match group 1, thus eliminating any whitespace matches
            expr_tokens.append(match.group(1))
            current_pos = match.end()
        
        # print(f"Processing {''.join(expr_tokens)}")
        results.append(process_weird_expr(expr_tokens))

    return results


def process_weird_expr(expr_tokens):
    # Rules: evaluate left to right; addition BEFORE multiplication; brackets take precedence

    # first let's eliminate the brackets
    expr_tokens = convert_inner_expressions(expr_tokens)

    # we've stripped the brackets.  So evaluate left to right
    result = process_inner_expression_add_over_prod(expr_tokens)

    # print(f"Intermediate result: {left_num}")
    return result


def process_inner_expression_add_over_prod(expr_tokens):
    # do addition first
    # iterate until we've done all the additions
    while "+" in expr_tokens:
        left_num = None
        right_num = None
        op = ""
        sum = 0
        for i, token in enumerate(expr_tokens):
            if token.isdigit():
                if (left_num) == None:
                    left_num = int(token)
                    left_posn = i
                else:
                    right_num = int(token)
                    right_posn = i

                    if op == "add":
                        sum = left_num + right_num

                        # substite sum for the previous terms
                        expr_tokens[left_posn:right_posn+1] = [str(sum)]

                        # break out of this loop and start next iteration
                        # otherwise we're continuing to process a list we've modified!
                        break
                    elif op == "prod":
                        left_num = right_num
                        left_posn = i

            elif token == "+":
                op = "add"
            elif token == "*":
                op = "prod"

        # print(f"Intermediate: {''.join(expr_tokens)}")
    
    # now multiplication
    left_num = None
    right_num = None
    op = ""
    sum = 0
    for token in expr_tokens:
        if token.isdigit():
            if (left_num) == None:
                left_num = int(token)
            else:
                right_num = int(token)
                if op == "add":
                    left_num = left_num + right_num
                elif op == "prod":
                    left_num = left_num * right_num

        elif token == "+":
            op = "add"
        elif token == "*":
            op = "prod"
    return left_num


def process_inner_expression(expr_tokens):
    left_num = None
    right_num = None
    op = ""
    for token in expr_tokens:
        if token.isdigit():
            if (left_num) == None:
                left_num = int(token)
            else:
                right_num = int(token)
                if op == "add":
                    left_num = left_num + right_num
                elif op == "prod":
                    left_num = left_num * right_num

        elif token == "+":
            op = "add"
        elif token == "*":
            op = "prod"
    return left_num


def convert_inner_expressions(expr_tokens):
    # keep going recursively, from outside in, until there are no more brackets
    while "(" in expr_tokens:
        bracket_count = 0
        outside_left_bracket = None

        for i, token in enumerate(expr_tokens):
            if token == "(":
                # see if this is the first bracket
                if outside_left_bracket == None:
                    outside_left_bracket = i

                # increment out bracket counter
                bracket_count += 1
            elif token == ")":
                # decrement our bracket counter
                bracket_count -= 1

                # if we get to 0, then we've reached the matching outer bracket
                if (bracket_count) == 0:
                    outside_right_bracket = i

                    # get the expression within the outer brackets
                    outer_bracket_expr = expr_tokens[outside_left_bracket+1:outside_right_bracket]

                    # recurse until we reach the innermost expression
                    result = str(process_weird_expr(outer_bracket_expr))

                    # replace the brackets with the recursive evaluation
                    expr_tokens[outside_left_bracket:outside_right_bracket+1] = [result]
                    # print("".join(expr_tokens))
                    break
    
    return expr_tokens


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines   


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



