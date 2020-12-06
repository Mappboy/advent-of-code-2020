from collections import Counter

from utils.all import *

test = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def get_counts(input_data: list):
    for group in input_data:
        yield len(set([c for g in group.split("\n") for c in g]))


def part2_solution(input_data: list):
    for group in input_data:
        groups = [_ for _ in group.split("\n") if _]
        counts = Counter([c for g in groups for c in g])
        yield len([k for k, v in counts.items() if v == len(groups)])


def part2_solution_set(input_data: list):
    ans = 0
    for group in input_data:
        ans += calculate_ans2([_ for _ in group.split("\n") if _])
    return ans


def calculate_ans2(groups):
    intersection = set.intersection(*[set(c) for c in {g for g in groups}])
    return len(intersection)



if __name__ == '__main__':
    advent.setup(2020, 6)
    fin = advent.get_input()
    assert sum(get_counts(test.split("\n\n"))) == 11
    input_data = fin.read()
    timer_start()
    ans = sum(get_counts(input_data.split("\n\n")))
    timer_start()
    print(ans)
    advent.submit_answer(1, ans)
    timer_lap()
    test2 = sum(part2_solution(test.split("\n\n")))
    assert test2 == 6
    ans2 = part2_solution_set(input_data.split("\n\n"))
    advent.submit_answer(2, ans2)
