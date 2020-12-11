from copy import deepcopy
from typing import List

from utils.all import *

test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

state2 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

state3 = """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
"""

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'

directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (1, 1), (-1, 1)]


def get_surrounds(data: List[List[str]], row: int, col: int):
    # We could optimise this for corner cases
    for r, c in directions:
        row_idx = row + r
        col_idx = col + c
        try:
            if row_idx < 0 or col_idx < 0 or (r == 0 and c == 0):
                yield 0
            else:
                yield data[row_idx][col_idx] == OCCUPIED_SEAT
        except IndexError:
            yield 0


def get_all_directions(data: List[List[str]], row: int, col: int):
    occupied_seats = []
    # less than row
    # start searching 1 seat around.
    # then expand radius
    count = 0
    row_len = len(data)
    col_len = len(data[row])
    for row_dir, col_dir in directions:
        rix = row + row_dir
        cix = col + col_dir
        while (0 <= rix < row_len) and (0 <= cix < col_len):
            if data[rix][cix] == EMPTY_SEAT:
                break
            if data[rix][cix] == OCCUPIED_SEAT:
                count += 1
                break
            rix += row_dir
            cix += col_dir
    return count


def run_model(input_list: List[List[str]], adjacent_limit=4, use_adjacent=True):
    new_list = deepcopy(input_list)
    for ridx, row in enumerate(input_list):
        for cidx, col in enumerate(row):
            if use_adjacent:
                count = sum(get_surrounds(input_list, ridx, cidx))
            else:
                count = get_all_directions(input_list, ridx, cidx)
            if col == FLOOR:
                new_list[ridx][cidx] = FLOOR
            elif col == OCCUPIED_SEAT and count >= adjacent_limit:
                new_list[ridx][cidx] = EMPTY_SEAT
            elif col == EMPTY_SEAT and count == 0:
                new_list[ridx][cidx] = OCCUPIED_SEAT
    return new_list


def part1(input_list: List[List[str]]):
    previous_state = input_list
    new_state = None
    while new_state != previous_state:
        if new_state:
            previous_state = new_state
        new_state = run_model(previous_state)
    return sum((seat == OCCUPIED_SEAT for row in new_state for seat in row))


def part2(input_list: List[List[str]]):
    previous_state = input_list
    new_state = None
    while new_state != previous_state:
        if new_state:
            previous_state = new_state
        new_state = run_model(previous_state, 5, False)
    return sum((seat == OCCUPIED_SEAT for row in new_state for seat in row))


def parse_input(input_data: List[str]) -> List[List[str]]:
    data = []
    for line in input_data:
        data.append([char for char in line])
    return data


if __name__ == '__main__':
    advent.setup(2020, 11)
    fin = advent.get_input()
    input_data = fin.read()

    assert run_model(parse_input(test.splitlines())) == parse_input(state2.splitlines())
    state2_parse = run_model(parse_input(state2.splitlines()))
    round_two = parse_input(state3.splitlines())
    assert state2_parse == round_two
    assert part1(parse_input(test.splitlines())) == 37
    ans1 = part1(parse_input(input_data.splitlines()))
    print(ans1)
    advent.submit_answer(1, ans1)
    ans2 = part2(parse_input(input_data.splitlines()))
    print(ans2)
    advent.submit_answer(2, ans2)
