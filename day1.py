"""
Two solutions
1: Using a simple permutation approach
2: More optimal solution using a set to check if answer exists
"""
import operator
import time
from functools import reduce
from itertools import permutations, takewhile
from pathlib import Path
from typing import List, Tuple


def find_sums(input_list: List[int], limit=2020, perms: int = 2) -> Tuple[int]:
    """
    Just going to use a simple permutations approach.
    Not accounting for negative or numbers over limit.
    I've ordered the list to optimise and take the lowest and filter out all the list entries that exceed the limit.
    This will reduce permutations.
    >>> find_sums([1010, 1010, 5])
    [(1010,1010)]
    """
    filtered_list = sorted(input_list)
    optimised_list = takewhile(lambda x: x + filtered_list[0] <= limit, filtered_list)
    for perm in permutations(optimised_list, perms):
        if sum(perm) == limit:
            return perm


def set_solver(input_list: List, answer=2020) -> int:
    entries = set(input_list)
    for x in input_list:
        if answer - x in entries:
            return (answer - x) * x


def set_solver2(input_list: List, answer=2020) -> int:
    entries = set(input_list)
    for x in input_list:
        for y in input_list:
            if (answer - x - y) in entries:
                return (answer - x - y) * x * y


def get_multiplied(input_tuple: Tuple) -> int:
    """Reduce to product"""
    return reduce(operator.mul, input_tuple)


if __name__ == "__main__":
    with open(Path("inputs").joinpath("day1"), "r") as input_data:
        file_input = [int(_) for _ in input_data.readlines()]
        start_time = time.time()
        ans_1 = get_multiplied(find_sums(file_input))
        finished = time.time() - start_time
        print(f"part 1 std lib = {ans_1}, {finished}")
        start_time = time.time()
        ans_1_hashed = set_solver(file_input)
        finished2 = time.time() - start_time
        print(f"part 1 set = {ans_1_hashed}, {finished2} {finished/finished2} faster")
        start_time = time.time()
        ans2 = get_multiplied((find_sums(
            file_input, perms=3)))
        finished3 = time.time() - start_time
        print(f"part 2 std lib = {ans2}, {finished3}")
        start_time = time.time()
        ans_2_hashed = set_solver2(sorted(file_input))
        finished4 = time.time() - start_time
        print(f"part 2 set = {ans_2_hashed}, {finished4} {finished3/finished4} faster")
