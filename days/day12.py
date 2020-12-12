import re
from math import cos, sin, radians
from typing import Tuple, List

from utils import advent

INSTRUCTION = re.compile(r"(\w{1})(\d+)")

test = """F10
N3
F7
R90
F11
"""

directions = ["W", "N", "E", "S"]


def move_ship(current_coord: tuple, magnitude: int, direction: str):
    if direction == "N":
        return current_coord[0] + magnitude, current_coord[1]
    elif direction == "S":
        return current_coord[0] - magnitude, current_coord[1]
    elif direction == "E":
        return current_coord[0], current_coord[1] + magnitude
    elif direction == "W":
        return current_coord[0], current_coord[1] - magnitude


def move_ship_waypoint(current_coord: tuple, waypoint: tuple, magnitude: int):
    x = current_coord[0] + waypoint[0] * magnitude
    y = current_coord[1] + waypoint[1] * magnitude
    return x, y


def instruction_to_coords(instruction: str, current_direction: str, current_coord: tuple) -> \
        Tuple[str, tuple]:
    """
    Convert a coord like N10
    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.
    """
    parse = INSTRUCTION.match(instruction)
    direction, magnitude = parse.groups()
    magnitude = int(magnitude)
    if direction in directions:
        return current_direction, move_ship(current_coord, magnitude, direction)
    elif direction == "L":
        return directions[int(directions.index(current_direction) - (magnitude / 90)) % 4], current_coord
    elif direction == "R":
        return directions[int(directions.index(current_direction) + (magnitude / 90)) % 4], current_coord
    elif direction == "F":
        return current_direction, move_ship(current_coord, magnitude, current_direction)
    else:
        return current_direction, current_coord


def rotate_matrix(angle, coordinate, clockwise=True):
    """
    Rotate coordinate around angle
    :param theta:
    :return:
    """
    theta = radians(angle)
    if clockwise:
        return ((int(coordinate[0] * cos(theta)) - int(coordinate[1] * sin(theta)),
                 int(coordinate[0] * sin(theta)) + int(coordinate[1] * cos(theta))))
    else:
        return ((int(coordinate[0] * cos(theta)) + int(coordinate[1] * sin(theta)),
                 int(coordinate[0] * -sin(theta)) + int(coordinate[1] * cos(theta))))


def instruction_to_waypoints(instruction: str, current_coord: tuple, waypoint: tuple = ()) -> \
        Tuple[tuple, tuple]:
    """
    Convert a coord like N10
    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.
    """
    parse = INSTRUCTION.match(instruction)
    direction, magnitude = parse.groups()
    magnitude = int(magnitude)
    if direction in directions:
        return move_ship(waypoint, magnitude, direction), current_coord
    elif direction == "L":
        return rotate_matrix(magnitude, waypoint, False), current_coord
    elif direction == "R":
        return rotate_matrix(magnitude, waypoint), current_coord
    elif direction == "F":
        return waypoint, move_ship_waypoint(current_coord, waypoint, magnitude)
    else:
        return waypoint, current_coord


def part1(data: List[str]):
    direction = 'E'
    coordinate = (0, 0)
    for instruction in data:
        direction, coordinate = instruction_to_coords(instruction, direction, coordinate)
    return sum((abs(_) for _ in coordinate))


def part2(data: List[str]):
    waypoint = (1, 10)
    coordinate = (0, 0)
    for instruction in data:
        waypoint, coordinate = instruction_to_waypoints(instruction, coordinate, waypoint)
    return sum((abs(_) for _ in coordinate))


if __name__ == '__main__':
    advent.setup(2020, 12)
    fin = advent.get_input()
    input_data = fin.read()
    assert part1(test.splitlines()) == 25
    ans1 = part1(input_data.splitlines())
    print(ans1)
    advent.submit_answer(1, ans1)
    t2 = part2(test.splitlines())
    assert t2 == 286
    ans2 = part2(input_data.splitlines())
    print(ans2)
    advent.submit_answer(2, ans2)
