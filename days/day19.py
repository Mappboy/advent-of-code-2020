import re
from collections import defaultdict
from typing import List, Dict, Pattern

from utils.all import *

test1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

test2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


def parse_rules(lines: List[str]) -> Dict[int, list]:
    rules = defaultdict(list)
    for line in lines:
        rule, values = line.split(":")
        for v in (_ for _ in values.split(" ") if _):
            if v.isnumeric():
                rules[int(rule)].append(int(v))
            else:
                rules[int(rule)].append(str(v.replace('"', '')))
    return rules


def convert_to_str(rules, value):
    """
    :return:
    """
    if isinstance(value, str):
        return value
    else:
        # check infinite recursion and replace with *
        result = ""
        if "|" in rules[value]:
            result += "("
        for v in rules[value]:
            result += convert_to_str(rules, v)
        if "|" in rules[value]:
            result += ")"
    return result


def convert_to_str2(rules, value, depth=0):
    """
    :return:
    """
    if depth > 15:
        return ''
    if isinstance(value, str):
        return value
    else:
        # check infinite recursion and replace with *
        result = ""
        if "|" in rules[value]:
            result += "("
        for v in rules[value]:
            result += convert_to_str2(rules, v, depth + 1)
        if "|" in rules[value]:
            result += ")"
    return result


def convert_to_pattern(rules: Dict[int, list], recursion=False) -> Pattern:
    pattern_str = ""

    for r in rules[0]:
        if recursion:
            pattern_str += convert_to_str2(rules, r)
        else:
            pattern_str += convert_to_str(rules, r)
    return re.compile(pattern_str)


def split_input_rules(lines: List[str]):
    """Output rules and input"""
    rules = []
    _input = []
    p = re.compile(r"\d+:.*")
    for line in lines:
        if p.match(line):
            rules.append(line)
        else:
            _input.append(line)
    return rules, _input


def part1(lines: List[str]):
    rules, _input = split_input_rules(lines)
    rules = parse_rules(rules)
    pattern = convert_to_pattern(rules)
    return sum((1 for line in _input if pattern.fullmatch(line)))


def replace_rules(rules: Dict[int, list]) -> Dict[int, list]:
    rules[8] = [42, "|", 42, 8]
    rules[11] = [42, 31, "|", 42, 11, 31]
    return rules


def part2(lines: List[str]):
    rules, _input = split_input_rules(lines)
    rules = parse_rules(rules)
    rules = replace_rules(rules)
    # Will need to add * for infinite recursive rules
    pattern = convert_to_pattern(rules, True)
    return sum((1 for line in _input if pattern.fullmatch(line)))


if __name__ == '__main__':
    advent.setup(2020, 19)
    fin = advent.get_input()
    input_data = fin.read()
    print(part1(test1.splitlines()))
    advent.submit_answer(1, part1(input_data.splitlines()))
    print(part2(test2.splitlines()))
    advent.submit_answer(2, part2(input_data.splitlines()))
