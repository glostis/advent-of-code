import os
from collections import defaultdict


def part1(orbits):
    chain = dict()

    for center, satellite in orbits:
        chain[satellite] = center

    count = 0
    for satellite, center in chain.items():
        while True:
            count += 1
            if center == "COM":
                break
            else:
                satellite = center
                center = chain[center]
    return count


def part2(orbits):
    graph = defaultdict(list)

    for center, satellite in orbits:
        # Make graph go both ways, because we can traverse it
        # in any direction
        graph[satellite].append(center)
        graph[center].append(satellite)

    count = len(find_path(graph, "SAN", "YOU")) - 3
    return count


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath


if __name__ == "__main__":
    with open(os.path.join("data", "day06_1.txt")) as f:
        orbits = [orbit.strip().split(")") for orbit in f]
        print(part1(orbits))
        print(part2(orbits))
