import operator
import re
from collections import defaultdict
from functools import reduce
from typing import List, Mapping

from utils.all import *

RULE_RE = re.compile(r"([a-zA-Z\s]+): (\d+)-(\d+) or (\d+)-(\d+)")

test = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


def str_to_ints(input_list: str):
    return list(map(int, input_list.split(",")))


def get_fails(input_list: List[int], rules):
    errors = 0
    for value in input_list:
        matched_rules = [rule[0] <= value <= rule[1] or rule[2] <= value <= rule[3] for rule in rules.values()]
        if not any(matched_rules):
            errors += value
    return errors


def part1(input_lines: List[str]):
    rules = {}
    input_section = 0
    skip_lines = 0
    error_count = 0
    for line in input_lines:
        if not line:
            input_section += 1
            skip_lines = 2
        if input_section == 0:
            m = RULE_RE.match(line)
            if m:
                rule_name, x1, x2, y1, y2 = m.groups()
                # I originally used a lambda below but it was failing
                rules[rule_name] = [int(x1), int(x2), int(y1), int(y2)]
                continue
        if input_section == 1:
            continue
        if input_section == 2:
            if skip_lines:
                # skip line with nearby tickets
                skip_lines -= 1
                continue
            error_count += get_fails(str_to_ints(line), rules)
    return error_count


def determine_fields(valid_tickets: List[List[int]], rules):
    ticket_len = len(valid_tickets[0])
    # Might have to determine what's only available I guessed that would happen
    ticket_mappings = defaultdict(list)
    for rule_name, rule in rules.items():
        for field in range(ticket_len):
            if all([rule[0] <= ticket[field] <= rule[1] or rule[2] <= ticket[field] <= rule[3] for ticket in
                    valid_tickets]):
                ticket_mappings[rule_name].append(field)
    return ticket_mappings


def determine_correct_mapping(ticket_mapping: Mapping[str, list], ticket_len: int):
    """Probably a better way to figure out ordering"""
    ticket_ordering = {}
    for rule, fields in sorted(ticket_mapping.items(), key=lambda x: len(x[1])):
        for field in fields:
            if field not in ticket_ordering.values():
                ticket_ordering[rule] = field
                break
    for rule in {_ for _ in ticket_mapping.keys()}.difference(ticket_ordering.keys()):
        ticket_ordering[rule] = list({i for i in range(ticket_len)}.difference(ticket_ordering.values()))[0]
    return ticket_ordering


def part2(input_lines: List[str]):
    """
    Should find a nicer way to reuse values or code from part1
    :param input_lines:
    :return:
    """
    rules = {}
    input_section = 0
    skip_lines = 0
    valid_lines = []
    for line in input_lines:
        if not line:
            input_section += 1
            skip_lines = 2
        if input_section == 0:
            m = RULE_RE.match(line)
            if m:
                rule_name, x1, x2, y1, y2 = m.groups()
                # I originally used a lambda below but it was failing
                rules[rule_name] = [int(x1), int(x2), int(y1), int(y2)]
                continue
        if input_section == 1:
            if skip_lines:
                # skip line with my tickets
                skip_lines -= 1
                continue
            my_ticket = str_to_ints(line)
        if input_section == 2:
            if skip_lines:
                # skip line with nearby tickets
                skip_lines -= 1
                continue
            line = str_to_ints(line)
            if not get_fails(line, rules):
                valid_lines.append(line)
    possible_fields = determine_fields(valid_lines, rules)
    correct_fields = determine_correct_mapping(possible_fields, ticket_len=len(valid_lines[0]))
    ticket_vals = [my_ticket[v] for k, v in correct_fields.items() if k.startswith('departure')]
    assert len(ticket_vals) == 6
    return reduce(operator.mul, ticket_vals)


if __name__ == '__main__':
    advent.setup(2020, 16)
    fin = advent.get_input()
    input_data = fin.read()

    t1 = part1(test.splitlines())
    assert t1 == 71
    advent.submit_answer(1, part1(input_data.splitlines()))
    # part2(input_data.splitlines())
    advent.submit_answer(2, part2(input_data.splitlines()))
