import re
from typing import List

from utils.all import *


class Int(int):
    def __mul__(self, other):
        return Int(int(self) * int(other))

    def __truediv__(self, other):
        return Int(int(self) + int(other))


class Int2(int):
    def __add__(self, other):
        return Int2(int(self) * int(other))

    def __mul__(self, other):
        return Int2(int(self) + int(other))


def parse(line: str):
    return eval(re.sub(r"(\d+)", r"Int(\1)", line).replace("+", "/"))


def parse2(line: str):
    return int(eval(re.sub(r"(\d+)", r"Int2(\1)", line.translate(str.maketrans({"+": "*", "*": "+"})))))


def part1(lines: List[str]):
    return sum([parse(line) for line in lines])


def part2(lines: List[str]):
    return sum([parse2(line) for line in lines])


if __name__ == '__main__':
    advent.setup(2020, 18)
    fin = advent.get_input()
    input_data = fin.read()
    assert parse("2 * 3 + (4 * 5)") == 26
    assert parse("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    # advent.submit_answer(1, part1(input_data.splitlines()))
    assert parse2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert parse2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    advent.submit_answer(2, part2(input_data.splitlines()))
