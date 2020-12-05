from collections import defaultdict
from pathlib import Path

BIN_TRANSLATE = str.maketrans("FBLR", "0101")


def get_seat(boarding_pass: str):
    """
    >>> get_seat("FBFBBFFRLR")
    (44, 5, 357)
    >>> get_seat("BFFFBBFRRR")
    (70, 7, 567)

    :param boarding_pass: Boarding pass str
    :return: tuple of row, column and seat_id
    """
    row = int(boarding_pass[:7].translate(BIN_TRANSLATE), 2)
    col = int(boarding_pass[7:].translate(BIN_TRANSLATE), 2)
    seat_id = row * 8 + col
    return row, col, seat_id


def find_seat(all_seats):
    seat_directory = defaultdict(set)
    for seat in all_seats:
        seat_directory[seat[0]].add(seat[1])
    rows = [k for k, v in seat_directory.items() if len(v) != 8]
    seat = [(row, c) for c in range(1, 7) for row in rows if
            c not in seat_directory[row] and c + 1 in seat_directory[row] and c - 1 in seat_directory[row]]
    assert len(seat) == 1
    row, col = seat[0]
    seat_id = row * 8 + col
    return row, col, seat_id


if __name__ == '__main__':
    with open(Path("inputs").joinpath("day5.txt"), "r") as input_data:
        passes = input_data.read().splitlines()
        print(max([get_seat(_)[2] for _ in passes]))
        print(find_seat([get_seat(_) for _ in passes]))
