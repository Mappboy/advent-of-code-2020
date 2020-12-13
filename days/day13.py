from functools import reduce

from utils.all import *

test = """939
7,13,x,x,59,x,31,19
"""


def part1(data):
    timestamp, bus_lines = data.splitlines()
    departures = [int(_) for _ in bus_lines.split(",") if _ != 'x' and _]
    earliest_departure = None
    earliest_bus = None
    timestamp = int(timestamp)
    for bus in departures:
        departing = (timestamp - (timestamp % bus) + bus) - timestamp
        if not earliest_departure or departing < earliest_departure:
            earliest_departure = departing
            earliest_bus = bus
    return earliest_bus * earliest_departure


def part2_brute_force(data):
    """There is a simple solution here but I can't think of it. I know I've seen it before"""
    timestamp, bus_lines = data.splitlines()
    departures = [_ for _ in ((t, bus) for t, bus in enumerate(bus_lines.split(",")) if bus) if _[1] != 'x']
    found = False
    # get start counts
    times = [_[0] for _ in sorted(departures, key=lambda x: x[1], reverse=True)]
    departures = [int(_[1]) for _ in sorted(departures, key=lambda x: x[1], reverse=True)]
    # use largest value
    check_value = departures[0]
    i = 0
    while not found:
        i += 1
        check_value += departures[0]
        if all([(check_value - times[0] + times[t]) % departures[t] == 0 for t in range(len(times))]):
            return check_value - times[0]


def part2(data):
    """
    Turns out this is the solution
    Thanks to https://github.com/Kurocon/AdventOfCode2020/ and these articles
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    https://fangya.medium.com/chinese-remainder-theorem-with-python-a483de81fbb8
    https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
    """
    buses = list(map(lambda x: int(x) if x != "x" else None, data.splitlines()[1].split(",")))
    bus_times = []
    bus_start_times = []
    for i, time in enumerate(buses):
        if time:
            bus_times.append(time)
            bus_start_times.append(time - i)

    return int(chinese_remainder(bus_times, bus_start_times))


def chinese_remainder(n, a):

    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part2_c(data):
    """
    This is another interesting solution it's similar to my brute force method but more efficient
    :param data:
    :return:
    """
    timestamp, bus_lines = data.splitlines()
    intervals = [
        (i, int(j))
        for i, j
        in enumerate(bus_lines.split(','))
        if j != 'x'
    ]
    start, step = 0, intervals[0][1]

    for a, b in intervals[1:]:
        while (start + a) % b != 0:
            start += step
        step *= b
    return start


if __name__ == '__main__':
    advent.setup(2020, 13)
    fin = advent.get_input()
    input_data = fin.read()
    assert part1(test) == 295
    # advent.submit_answer(1, part1(input_data))
    assert part2("""0\n17,x,13,19""") == 3417
    assert part2("""0\n67,7,59,61""") == 754018
    assert part2("""0\n67,x,7,59,61""") == 779210
    assert part2("""0\n67,7,x,59,61""") == 1261476
    assert part2("""0\n1789,37,47,1889""") == 1202161486
    timer_start()
    # 1012171816131259
    print(part2(input_data))
    advent.submit_answer(2, part2_c(input_data))
    timer_stop()
