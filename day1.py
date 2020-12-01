import operator
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


def get_multiplied(input_tuple: Tuple) -> int:
    """Reduce to """
    return reduce(operator.mul, input_tuple)


if __name__ == "__main__":
    with open(Path("inputs").joinpath("day1"), "r") as input_data:
        file_input = [int(_) for _ in input_data.readlines()]

        print(get_multiplied(find_sums(file_input)))
        print(get_multiplied((find_sums(
            file_input, perms=3))))
