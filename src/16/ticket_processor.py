import sys
import os
import time
import re
from collections import defaultdict
from pprint import pprint as pp

INPUT_FILE = "input/ticket_data.txt"
SAMPLE_INPUT_FILE = "input/sample_ticket_data.txt"

ADDR_SIZE = 36


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    # print("Input file is: " + input_file)

    input = read_input(input_file)
    # pp(input)

    field_rules, my_ticket, nearby_tickets = process_input(input)
    # pp(field_rules)

    # pp(nearby_tickets)

    print(f"My ticket: {my_ticket}")
    print(f"Nearby tickets count: {len(nearby_tickets)}")

    invalid_values = []
    invalid_values = validate_tickets(nearby_tickets, field_rules)
    print(f"Valid nearby tickets count: {len(nearby_tickets)}")
    
    # print(f"Invalid values: {invalid_values}")
    print(f"Sum of invalid values: {sum(invalid_values)}")

    fields_and_invalid_positions = get_fields_and_invalid_positions(field_rules, nearby_tickets)
    fields_and_positions = find_position_for_field(field_rules, fields_and_invalid_positions)
    pp(fields_and_positions)

    departure_field_positions = [fields_and_positions[x] for x in fields_and_positions.keys() if x.startswith("departure")]
    print(f"Daparture field positions: {departure_field_positions}")

    field_values = {}
    for field in fields_and_positions:
        if (field.startswith("departure")):
            field_values[field] = my_ticket[fields_and_positions[field]]

    pp(field_values)
    product = 1
    for val in field_values:
        product *= field_values[val]

    print(f"Solution answer is the product of departure fields: {product}")   
    

def process_input(data):
    # match a field like...
    # seat: 13-40 or 45-50
    field_pattern = re.compile(r"^(\D+): (\d+-\d+) or (\d+-\d+)")

    field_rules = {}
    nearby_tickets = []
    my_ticket = []

    current_heading = ""
    for line in data:
        current_line = line.rstrip()
        if (current_heading == ""):
            match = field_pattern.match(line)
            if match:
                field_groups = match.groups()
                field_name = field_groups[0]
                field_rule_1 = [int(val) for val in field_groups[1].split("-")]
                field_rule_2 = [int(val) for val in field_groups[2].split("-")]
                field_rules[field_name] = (field_rule_1, field_rule_2)
        elif (current_heading == "nearby tickets:"):
            if (current_line != ""):
                nearby_tickets.append([int(x) for x in current_line.split(",")])
        elif (current_heading == "your ticket:"):
            if (current_line != ""):
                my_ticket = [int(x) for x in current_line.split(",")]
        
        if (current_line == "nearby tickets:" or current_line == "your ticket:" or current_line == ""):
            current_heading = current_line

    return field_rules, my_ticket, nearby_tickets
       

def get_fields_and_invalid_positions(rules, nearby_tickets):
    # return dict of field names and positions where the value is invalid.  E.g.
    # {'departure plaform': [0, 1, 3, 6, 15, 19]
    #  'seat': [0, 1, 3, 19] ... }
    field_and_non_matching_vals = defaultdict(list)

    # iterate through all rules, which should match number of fields
    for i in range(len(rules)):
        # get field i for for each ticket
        for ticket in nearby_tickets:
            value = ticket[i]

            for field_name in rules.keys():
                rule_part_1 = rules[field_name][0]
                rule_part_2 = rules[field_name][1]
                
                if ((value < rule_part_1[0] or value > rule_part_1[1]) 
                        and (value < rule_part_2[0] or value > rule_part_2[1])):
                    # rule doesn't match so continue to next rule
                    field_and_non_matching_vals[field_name].append(i)
                    continue

    return field_and_non_matching_vals


def find_position_for_field(rules, fields_and_invalid_positions):
    # start with our dict of { field: [invalidfield1, invalidfield2, etc]}
    
    # This is our set of ALL fields
    all_fields = set(range(len(rules)))

    # This is where we store the field positions we have determined
    fields_and_positions = {}

    # sort our dictionaries by size.  
    # I.e. the one with most invalid fields.  This one will only be missing one field.
    for field_name in sorted(fields_and_invalid_positions, key=lambda k: len(fields_and_invalid_positions[k]), reverse=True):
        nm_set = set(fields_and_invalid_positions[field_name])
        
        # add, to this set of invalid field positions, 
        # field positions that we have determined for other fields
        nm_set = nm_set.union(set(fields_and_positions.values()))

        # the set diff gives us the only field that is valid for this field name
        diff = all_fields.difference(nm_set)

        if (len(diff) == 1):
            fields_and_positions[field_name] = diff.pop()

    return fields_and_positions


def validate_tickets(tickets, rules):
    invalid_values = []

    for ticket in tickets.copy():
        for value in ticket:
            if not check_all_rules_matched(rules, value):
                invalid_values.append(value)
                tickets.remove(ticket)

    return invalid_values


def check_all_rules_matched(rules, value):
    # rule pair looks like
    # {'seat': ([0, 13], [16,19])}
    # each rule in in the pair defines a min and max that is allowed
    # value must match one or other rule in the pair to be valid   
    for rule_pair in rules.keys():
        rule_part_1 = rules[rule_pair][0]
        rule_part_2 = rules[rule_pair][1]
        if ((value < rule_part_1[0] or value > rule_part_1[1]) 
                and (value < rule_part_2[0] or value > rule_part_2[1])):
            # this rule doesn't match; move onto the next
            continue
        else:
            # value matches at least one rule.  Good enough.
            return True
    
    return False


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

