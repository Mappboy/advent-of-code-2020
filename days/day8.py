import re
from typing import Tuple, Iterator

from utils.all import *

LINE_RE = re.compile(r"(?P<inst>\w{3}) (?P<value>[+-]\d+)")
test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


def parse_input(input_lines: list) -> Iterator[Tuple[int, dict]]:
    """Turn lines into list of instrructions"""
    for idx, line in enumerate(input_lines):
        match = LINE_RE.match(line)
        if match:
            yield idx, match.groupdict()


def part1(input_str: str):
    instructions = list(parse_input(input_str.splitlines()))
    instructions_run = set()
    idx = 0
    accumulator = 0
    while instruction := instructions[idx]:
        if instruction[0] in instructions_run:
            return accumulator
        ins_val = int(instruction[1]["value"])
        if instruction[1]["inst"] == "nop":
            idx += 1
        elif instruction[1]["inst"] == "acc":
            accumulator += ins_val
            idx += 1
        elif instruction[1]["inst"] == "jmp":
            idx += ins_val
        instructions_run.add(instruction[0])


def check_input(instruction_list: list):
    instructions_run = set()
    idx = 0
    accumulator = 0
    try:
        while instruction := instruction_list[idx]:
            if instruction[0] in instructions_run:
                return False, accumulator
            ins_val = int(instruction[1]["value"])
            if idx == len(instruction_list) - 1:
                # Final instruction
                if instruction[1]["inst"] == "acc":
                    return True, accumulator + ins_val
                else:
                    return True, accumulator
            if instruction[1]["inst"] == "nop":
                idx += 1
            elif instruction[1]["inst"] == "acc":
                accumulator += ins_val
                idx += 1
            elif instruction[1]["inst"] == "jmp":
                idx += ins_val
            instructions_run.add(instruction[0])
    except IndexError:
        # messed up an instruction
        return False, accumulator


def part2(input_str: str):
    """
    Brute force because I am not sure yet how to optomise this
    """
    instructions = list(parse_input(input_str.splitlines()))
    nop_instrcutions = [i[0] for i in instructions if i[1]["inst"] == "nop"]
    jmp_instructions = [i[0] for i in instructions if i[1]["inst"] == "jmp"]
    for nop in nop_instrcutions:
        new_instructions = instructions.copy()
        new_instructions[nop] = (nop, {"inst": "jmp", "value": instructions[nop][1]["value"]})
        run = check_input(new_instructions)
        if run[0]:
            return run[1]
    for jmp in jmp_instructions:
        new_instructions = instructions.copy()
        new_instructions[jmp] = (jmp, {"inst": "nop", "value": instructions[jmp][1]["value"]})
        run = check_input(new_instructions)
        if run[0]:
            return run[1]


if __name__ == '__main__':
    advent.setup(2020, 8)
    fin = advent.get_input()
    input_data = fin.read()
    assert part1(test) == 5
    ans1 = part1(input_data)
    print(ans1)
    t2 = part2(test)
    assert t2 == 8, f"Answer was {t2}"
    ans2 = part2(input_data)
    assert ans2 is not None
    print(ans2)
    advent.submit_answer(2, ans2)
