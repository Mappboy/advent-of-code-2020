from collections import defaultdict
from copy import deepcopy
from typing import List

from utils.all import *

test = """.#.
..#
###"""

INACTIVE = '.'
ACTIVE = '#'

directions = [(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) if
              not (x == 0 and y == 0 and z == 0)]


def get_surrounds(data: List[List[List[str]]], row: int, col: int, cube: int):
    # We could optimise this for corner cases
    for r, c, z in directions:
        row_idx = row + r
        col_idx = col + c
        z_idx = cube + z
        try:
            if row_idx < 0 or col_idx < 0 or z_idx < 0:
                yield 0
            else:
                yield data[row_idx][col_idx][z_idx] == ACTIVE
        except IndexError:
            yield 0


def neighbours(x, y, z):
    return [
        (x + dx, y + dy, z + dz, 0)
        for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if (dx, dy, dz) != (0, 0, 0)
    ]


def neighbours4d(x, y, z, w):
    return [
        (x + dx, y + dy, z + dz, w + dw)
        for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] for dw in [-1, 0, 1] if
        (dx, dy, dz, dw) != (0, 0, 0, 0)
    ]


def minmax_coords(universe):
    keys = universe.keys()
    minx = min(keys, key=lambda x: x[0])[0]
    maxx = max(keys, key=lambda x: x[0])[0]
    miny = min(keys, key=lambda x: x[1])[1]
    maxy = max(keys, key=lambda x: x[1])[1]
    minz = min(keys, key=lambda x: x[2])[2]
    maxz = max(keys, key=lambda x: x[2])[2]
    minw = min(keys, key=lambda x: x[3])[3]
    maxw = max(keys, key=lambda x: x[3])[3]
    return minx, maxx, miny, maxy, minz, maxz, minw, maxw


def process_layer(new_list: List[List[List[str]]], input_layer: List[List[List[str]]], adjacent_limit, zidx):
    layer = input_layer[zidx]
    for ridx in range(3):
        for cidx in range(len(layer[ridx])):
            z = layer[ridx][cidx]
            count = sum(get_surrounds(input_layer, zidx, ridx, cidx))
            if z == ACTIVE and not (adjacent_limit <= count <= adjacent_limit + 1):
                new_list[zidx][ridx][cidx] = INACTIVE
            elif z == INACTIVE and count == adjacent_limit + 1:
                new_list[zidx][ridx][cidx] = ACTIVE


def run_model(input_list: List[List[List[str]]], adjacent_limit=2, cycles: int = 0):
    # First we do the z = 0 and expand
    new_list = deepcopy(input_list)
    for zidx in range(len(new_list)):
        process_layer(new_list, input_list, adjacent_limit, zidx)
    return new_list


def active_neighbours(universe, x, y, z):
    return sum(universe[n] for n in neighbours(x, y, z))


def active_neighbours4d(universe, x, y, z, w):
    return sum(universe[n] for n in neighbours4d(x, y, z, w))


def step(universe):
    new_universe = defaultdict(lambda: False)
    minx, maxx, miny, maxy, minz, maxz, _, _ = minmax_coords(universe)
    for z in range(minz - 1, maxz + 2):
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                is_active = universe[x, y, z, 0]
                num_active = active_neighbours(universe, x, y, z)
                if is_active:
                    new_universe[x, y, z, 0] = num_active in [2, 3]
                else:
                    new_universe[x, y, z, 0] = num_active == 3
    return new_universe


def step2(universe):
    new_universe = defaultdict(lambda: False)
    minx, maxx, miny, maxy, minz, maxz, minw, maxw = minmax_coords(universe)
    for z in range(minz - 1, maxz + 2):
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                for w in range(minw - 1, maxw + 2):
                    is_active = universe[x, y, z, w]
                    num_active = active_neighbours4d(universe, x, y, z, w)
                    if is_active:
                        new_universe[x, y, z, w] = num_active in [2, 3]
                    else:
                        new_universe[x, y, z, w] = num_active == 3
    return new_universe


def expand_dimension(input_list, cycles: int) -> List[List[List[str]]]:
    if cycles:
        for row in input_list:
            for col in row:
                col.insert(0, INACTIVE)
                col.append(INACTIVE)
    cols = len(input_list[0][0])
    new_list = [[[INACTIVE for i in range(cols)]
                 for row in range(3)]] + input_list + [[[INACTIVE for i in range(cols)]
                                                        for row in range(3)]]
    return new_list


def part1(input_list: List[List[List[str]]]):
    state = input_list
    for cycles in range(6):
        # With each new cycle
        state = expand_dimension(state, cycles)
        state = run_model(state, cycles=cycles)
    return sum((cube == ACTIVE for dimension in state for row in dimension for cube in row))


def part1a(input_list: List[str]):
    universe = parse_input2(input_list)
    for i in range(6):
        universe = step(universe)
    return sum(universe.values())


def part2(input_list: List[str]):
    universe = parse_input2(input_list)
    for i in range(6):
        universe = step2(universe)
    return sum(universe.values())


def parse_input(input_data: List[str]) -> List[List[List[str]]]:
    data = []
    for line in input_data:
        data.append([char for char in line])
    return [data]


def parse_input2(input_data: List[str]):
    universe = defaultdict(lambda: False)
    for y, line in enumerate(input_data):
        for x, c in enumerate(line):
            universe[x, y, 0, 0] = c == ACTIVE
    return universe


def print_universe(universe):
    minx, maxx, miny, maxy, minz, maxz, _, _ = minmax_coords(universe)
    res = ""
    for z in range(minz, maxz + 1):
        res += f"z={z}\n"
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                res += ACTIVE if universe[x, y, z, 0] else INACTIVE
            res += "\n"
        res += "\n"
    print(res)


if __name__ == '__main__':
    advent.setup(2020, 17)
    fin = advent.get_input()
    input_data = fin.read()
    t1 = part1(parse_input(test.splitlines()))
    # assert t1 == 112
    ans1 = part1(parse_input(input_data.splitlines()))
    ans1a = part1a(input_data.splitlines())
    print(ans1)
    print(ans1a)
    # advent.submit_answer(1, ans1a)
    t2 = part2(test.splitlines())
    print(t2)
    assert t2 == 848
    advent.submit_answer(2, part2(input_data.splitlines()))
