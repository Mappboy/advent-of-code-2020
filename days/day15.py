import operator
from collections import defaultdict
from functools import reduce
from typing import List

from utils.all import *

test = """0,3,6"""


def str_to_ints(input_list: str):
    return list(map(int, input_list.split(",")))


def get_spoken(input_data: List[int], stop_number=2020):
    """Could improve memory performance only saving last two numbers"""
    numbers = defaultdict(list)
    for i, n in enumerate(input_data):
        numbers[n].append(i)
    idx = len(numbers)
    spoken = input_data[-1]
    while idx < stop_number:
        last_number = numbers[spoken]
        if len(last_number) == 1:
            spoken = 0
        else:
            spoken = last_number[-1] - last_number[-2]
        numbers[spoken].append(idx)
        idx += 1
    return spoken


if __name__ == '__main__':
    advent.setup(2020, 15)
    fin = advent.get_input()
    input_data = fin.read()
    assert get_spoken(str_to_ints(test)) == 436
    assert get_spoken(str_to_ints("3,2,1")) == 438
    assert get_spoken(str_to_ints("3,1,2")) == 1836
    advent.submit_answer(1, get_spoken(str_to_ints(input_data)))
    assert get_spoken(str_to_ints("0,3,6"), 30000000) == 175594
    advent.submit_answer(2, get_spoken(str_to_ints(input_data), 30000000))
