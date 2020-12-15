import os
from math import gcd


def part1(timestamp, buses):
    min_wait_time = timestamp

    for bus in buses:
        if bus is None:
            continue
        wait_time = bus - (timestamp % bus)
        if wait_time < min_wait_time:
            the_bus = bus
            min_wait_time = wait_time

    return the_bus * min_wait_time


def lcm(a, b):
    return a * b // gcd(a, b)


def merge_buses(bus1, hour1, bus2, offset2):
    """Replace two buses by a single synthetic bus

    bus1 has frequency bus1 and first departs at hour1 (which is not the case
    of "normal" buses, they all first departed at hour 0)
    bus2 has frequency bus2 and there is a time where it departs with a time offset
    offset2 w.r.t. bus1
    """
    bus3 = lcm(bus1, bus2)
    hour3 = offset(bus1, hour1, bus2, offset2)
    return bus3, hour3


def offset(bus1, hour1, bus2, offset2):
    """Find first time where bus1 and bus2 are in sync, with bus1 first departing at hour1
    and bus2 needing to depart with a time offste offset2 w.r.t. bus1
    """
    t1 = hour1
    while True:
        if (t1 + offset2) % bus2 == 0:
            return t1
        else:
            t1 += bus1


def part2(buses):
    inp = [(b, i) for i, b in enumerate(buses) if b is not None]
    bus1, hour1 = inp.pop(0)
    while len(inp) >= 1:
        bus2, offset2 = inp.pop(0)
        bus1, hour1 = merge_buses(bus1, hour1, bus2, offset2)
    return hour1


def main():
    with open(os.path.join("data", "day13.txt")) as f:
        lines = [line.strip() for line in f]

    timestamp, buses_str = lines

    timestamp = int(timestamp)
    buses = []
    for bus in buses_str.split(","):
        if bus != "x":
            buses.append(int(bus))
        else:
            buses.append(None)

    print(part1(timestamp, buses))
    print(part2(buses))


if __name__ == "__main__":
    main()
