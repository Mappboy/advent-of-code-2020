import operator
from functools import reduce
from pathlib import Path

test_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def travese_slope(input_map: list, right=3, down=1):
    tobagan = 0
    hit_tree = 0
    for idx, line in enumerate(input_map):
        # start at one
        if idx == 0 or idx % down:
            continue
        line = line.rstrip("\n")
        tobagan += right
        if line[tobagan % len(line)] == "#":
            hit_tree += 1
    return hit_tree


if __name__ == '__main__':
    test_count = travese_slope(test_input.split("\n"))
    assert test_count == 7, f"test count was {test_count}"
    with open(Path("inputs").joinpath("day3.txt"), "r") as input_data:
        snow_map = input_data.readlines()
        print(f"Part 1 = {travese_slope(snow_map)}")
        paths = [(1,1), (3,1), (5,1), (7,1), (1,2)]
        print(f"Part 2 = {reduce(operator.mul,[ travese_slope(snow_map, *_) for _ in paths ])}")


