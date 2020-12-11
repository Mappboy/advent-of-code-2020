from collections import Counter
from typing import List

from utils.all import *

test = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


def part1(input_list: List[int]):
    values = sorted(input_list)
    values.append(values[-1] + 3)

    last_jolt = 0
    diffs = [0, 0, 0, 0]

    for jolt in values:
        diffs[jolt - last_jolt] += 1
        last_jolt = jolt

    return diffs[1] * diffs[3]


def part2(input_list: List[int]):
    values = sorted(input_list)
    values.append(values[-1] + 3)
    counts = Counter()
    counts[0] = 1
    for jolt in values:
        counts[jolt] = counts[jolt - 1] + counts[jolt - 2] + counts[jolt - 3]

    return counts[values[-1]]


if __name__ == '__main__':
    advent.setup(2020, 10)
    fin = advent.get_input()
    input_data = fin.read()
    data = [int(_) for _ in input_data.splitlines()]
    t1 = part1([int(_) for _ in test.splitlines()])
    assert t1 == 220
    ans1 = part1(data)
    print(ans1)
    # advent.submit_answer(1, ans1)
    t2 = part2([int(_) for _ in test.splitlines()])
    assert t2 == 19208, f" t2 = {t2}"
    ans2 = part2(data)
    print(ans2)
    advent.submit_answer(2, ans2)