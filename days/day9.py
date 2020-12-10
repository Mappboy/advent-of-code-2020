from typing import List

from utils.all import *

test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


def part1(input_list: List[int], preabmle_length=25):
    for i in range(len(input_list)):
        current_values = set(input_list[i:i + preabmle_length])
        summed_value = input_list[preabmle_length + i]
        if any(((summed_value - value) in current_values for value in current_values)):
            continue
        else:
            return preabmle_length + i, summed_value


def part2(input_list: List[int], ans_idx: int):
    search_value = input_list[ans_idx]
    for i in reversed(range(ans_idx)):
        # Set must be at least two numbers
        for j in range(2, i):
            values = [_ for _ in input_list[i - j:i]]
            summed_value = sum(values)
            if summed_value > search_value:
                break
            if summed_value == search_value:
                return min(values) + max(values)



if __name__ == '__main__':
    advent.setup(2020, 9)
    fin = advent.get_input()
    input_data = fin.read()
    data = [int(_) for _ in input_data.splitlines()]
    t1 = part1([int(_) for _ in test.splitlines()], 5)
    assert t1[1] == 127, f"{t1}"

    ans_idx, ans1 = part1(data)
    print(ans1)
    # advent.submit_answer(1, ans1)
    ans2 = part2(data, ans_idx)
    print(ans2)
    advent.submit_answer(2, ans2)