import re
from collections import defaultdict, Counter
from typing import List, Dict

from utils.all import *

LINE_PATTERN = re.compile(r"(((\w+)\s)+)\(contains (.*)\)")

test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


def parse_rules(data: List[str]):
    all_ingredients = set()
    counter = Counter()
    allergens = defaultdict(list)
    possible_allergens = defaultdict(set)
    for line in data:
        match = LINE_PATTERN.match(line)
        if match:
            ingredients = [_ for _ in match.group(1).split(" ") if _]
            includes = match.group(4).split(",")
            all_ingredients.update(ingredients)
            counter.update(ingredients)
            for allergen in includes:
                allergens[allergen.strip()].append(set(ingredients))
    for allergen, ingredients in allergens.items():
        possible_allergens[allergen].update(set.intersection(*ingredients))
    return all_ingredients, possible_allergens, counter


def process_allergens(allergens: Dict[str, set]):
    found_allergens = set()
    while len(found_allergens) != len(allergens):
        for k, v in sorted(allergens.items(), key=lambda kv: len(kv[1])):
            if len(v) == 1:
                found_allergen = list(v)[0]
                found_allergens.add(found_allergen)
                # remove
                for kk, vv in allergens.items():
                    if found_allergen in vv and kk != k:
                        vv.discard(found_allergen)
            else:
                removed_allergens = v.difference(found_allergens)
                if len(removed_allergens) == 1:
                    found_allergens.update(removed_allergens)
                    allergens[k] = removed_allergens
    return allergens


def part1(data: List[str]):
    ingredients, allergens, counter = parse_rules(data)
    no_allergens = ingredients.difference(set.union(*allergens.values()))
    return sum((counter[c] for c in no_allergens))


def part2(data: List[str]):
    ingredients, allergens, counter = parse_rules(data)
    processed_allergens = process_allergens(allergens)
    return ",".join(
        (list(v)[0] for k, v in sorted(processed_allergens.items(), key=lambda kv: (kv[0], kv[1]))))


if __name__ == '__main__':
    advent.setup(2020, 21)
    fin = advent.get_input()
    input_data = fin.read()
    assert part1(test.splitlines()) == 5
    assert part2(test.splitlines()) == "mxmxvkd,sqjhc,fvjkl"
    # advent.submit_answer(1, part1(input_data.splitlines()))
    print(part2(input_data.splitlines()))
    advent.submit_answer(2, part2(input_data.splitlines()))
