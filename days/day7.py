import queue
import re
from collections import defaultdict

from utils.all import *

test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

test2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

PATTERN = re.compile(r"([a-z]+) ([a-z]+) bags contain ((([0-9]+) ([a-z]+) ([a-z]+) bags?[,.] ?)+|(no other bags.))")
CONTAIN_PATTERN = re.compile(r"([0-9]+) ([a-z]+) ([a-z]+) bags?.?")


# first parse list to bags
def parse_rules(input_lines: list):
    bags = defaultdict(set)
    contain_bags = defaultdict(list)
    for line in input_lines:
        match = PATTERN.match(line)
        if match:
            tone, color, inner_bags, *other = match.groups()
            contains_bags = CONTAIN_PATTERN.match(inner_bags)
            if contains_bags:
                for bag in CONTAIN_PATTERN.finditer(inner_bags):
                    bags[(bag.group(2), bag.group(3))].add((tone, color))
                    contain_bags[(tone, color)].append((int(bag.group(1)), (bag.group(2), bag.group(3))))
    return bags, contain_bags


def part1(bags, contain_bags):
    """
    Use BFS
    :param bags:
    :param contain_bags:
    :return:
    """
    number_of_bags = 0
    visited = set()
    q = queue.Queue()
    for bag in bags[('shiny', 'gold')]:
        q.put(bag)
    while not q.empty():
        bag = q.get()
        if bag not in visited:
            number_of_bags += 1
            for inner_bag in bags[bag]:
                q.put(inner_bag)
            visited.add(bag)
    return number_of_bags


def part2(contain_bags, root):
    """
    Use DFS
    :param contain_bags:
    :param root:
    :return:
    """
    if len(contain_bags[root]) == 0:
        return 0

    result = 0
    for count, bag in contain_bags[root]:
        result += count + count * part2(contain_bags, bag)
    return result



if __name__ == '__main__':
    advent.setup(2020, 7)
    fin = advent.get_input()
    input_data = fin.read()

    assert part1(*parse_rules(test.splitlines())) == 4
    ans_t2 = part2(*parse_rules(test2.splitlines()))
    assert ans_t2 == 126, f"Got {ans_t2} instead of 126"
    timer_start()
    ans1 = part1(*parse_rules(input_data.splitlines()))
    timer_stop()
    advent.submit_answer(1, ans1)
    print(ans1)
    timer_lap()
    ans2 = part2(parse_rules(input_data.splitlines())[1], ('shiny', 'gold'))
    print(ans2)
    advent.submit_answer(2, ans2)

