"""
Things to tidy.
Consider using Counter
Use regex for line input
"""
import re
from pathlib import Path


def get_count(password: str, letter: str):
    """
    Get count of letter in password
    >>> get_count("abcde", "a")
    1
    """
    return len(re.findall(letter, password))


LINE_RE = re.compile(r"([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)")

if __name__ == '__main__':
    valid_part1 = 0
    valid_part2 = 0
    with open(Path("inputs").joinpath("day2.txt"), "r") as input_data:
        for line in input_data.readlines():
            low, high, letter_in, password_in = LINE_RE.match(line).groups()
            low = int(low)
            high = int(high)
            if low <= get_count(password_in, letter_in) <= high:
                valid_part1 += 1
            if (password_in[low - 1] == letter_in) ^ (password_in[high - 1] == letter_in):
                valid_part2 += 1
    print(f"Number of valid passwords part 1 {valid_part1}")
    print(f"Number of valid passwords part 2 {valid_part2}")
