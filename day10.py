import os

import numpy as np


def part1(lines):
    ast_list = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                ast_list.append((j, i))

    asteroids = dict()
    for asteroid in ast_list:
        angles = set()
        for other in ast_list:
            if asteroid != other:
                angles.add(np.arctan2(asteroid[0] - other[0], asteroid[1] - other[1]))
        asteroids[asteroid] = angles

    max_k = None
    max_v = 0
    for k, v in asteroids.items():
        if len(v) > max_v:
            max_k = k
            max_v = len(v)

    return max_k, max_v, asteroids


def part2(asteroids, position):
    print(position)


if __name__ == "__main__":
    with open(os.path.join("data", "day10_1.txt")) as f:
        lines = [el.strip() for el in f]
        position, neighbors, asteroids = part1(lines)
        print(neighbors)
        part2(asteroids, position)
