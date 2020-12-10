import os
from collections import defaultdict


def part1(adapters):
    differences = defaultdict(int)
    for a1, a2 in zip(adapters[:-1], adapters[1:]):
        difference = a2 - a1
        differences[difference] += 1

    return differences[1] * differences[3]


def part2(adapters):
    cache = dict()
    return recurse(cache, adapters) + 1


def recurse(cache, adapters):
    count = 0
    if tuple(adapters) in cache:
        return cache[tuple(adapters)]

    if len(adapters) <= 2:
        pass
    else:
        element = adapters[0]
        if adapters[2] - element <= 3:
            count += 1
            count += recurse(cache, adapters[1:])
            count += recurse(cache, [element] + adapters[2:])
        else:
            count += recurse(cache, adapters[1:])
    cache[tuple(adapters)] = count
    return count


def main():
    with open(os.path.join("data", "day10.txt")) as f:
        adapters = [int(line.strip()) for line in f]

    adapters = adapters.copy()
    adapters = sorted(adapters)
    adapters = [0] + adapters + [adapters[-1] + 3]
    print(part1(adapters))
    print(part2(adapters))


if __name__ == "__main__":
    main()
