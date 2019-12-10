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

    max_v = 0
    for v in asteroids.values():
        if len(v) > max_v:
            max_v = len(v)

    return max_v


if __name__ == "__main__":
    with open(os.path.join("data", "day10_1.txt")) as f:
        lines = [el.strip() for el in f]
        print(part1(lines))
