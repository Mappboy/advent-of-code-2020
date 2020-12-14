import re

from utils.all import *

test = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

test2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""
MEM = re.compile(r"mem\[([0-9]+)\] = ([0-9]+)")
MASK = re.compile(r"mask = ([X01]{36})")


def parse_data(input_data):
    mask = None, 0, 0
    instructions = []
    for line in input_data:
        mask_line = MASK.match(line)
        mem_line = MEM.match(line)
        if mask_line:
            mask_string = mask_line.group(1)
            mask = mask_string, int(mask_string.replace("X", "1"), 2), int(mask_string.replace("X", "0"), 2)
        elif mem_line:
            instructions.append((mask, (int(mem_line.group(1)), int(mem_line.group(2)))))
        else:
            # Non matching input whoops
            continue
    return instructions


def mask_to_addresses(mask, location):
    """There must be a better way to generate the addresses than this"""
    location = location | mask[1]
    loc_mask = list("{0:036b}".format(location))
    for i in re.finditer("X", mask[0]):
        loc_mask[i.start(0)] = "X"
    masks = generate_masks("".join(loc_mask))
    return [int(m, 2) for m in masks]


def generate_masks(mask: str):
    if "X" in mask:
        mask1, mask2 = mask.replace("X", "0", 1), mask.replace("X", "1", 1)
        masks = generate_masks(mask1)
        masks += generate_masks(mask2)
        if masks:
            return masks
        else:
            return [mask1, mask2]
    return []


def part1(input_data):
    mem = {}
    instructions = parse_data(input_data)
    for mask, instruction in instructions:
        location, value = instruction
        mem[location] = value & mask[1] | mask[2]
    return sum(mem.values())


def part2(input_data):
    mem = {}
    instructions = parse_data(input_data)
    for mask, instruction in instructions:
        location, value = instruction
        for loc in mask_to_addresses(mask, location):
            mem[loc] = value
    return sum(mem.values())


if __name__ == '__main__':
    advent.setup(2020, 14)
    fin = advent.get_input()
    input_data = fin.read()
    t1 = part1(test.splitlines()) == 165
    assert t1, "Failed test"
    print(part1(input_data.splitlines()))
    # advent.submit_answer(1, part1(input_data.splitlines()))
    print(part2(test2.splitlines()))
    print(part2(input_data.splitlines()))
    advent.submit_answer(2, part2(input_data.splitlines()))
