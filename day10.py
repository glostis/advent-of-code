# pylint: disable=redefined-outer-name
from collections import defaultdict
import os

import numpy as np


def extract_asteroids(lines):
    ast_list = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                ast_list.append((j, i))
    return ast_list


def get_angles(asteroid, ast_list):
    angles = defaultdict(list)
    for other in ast_list:
        if asteroid != other:
            angle = np.arctan2(asteroid[0] - other[0], asteroid[1] - other[1])
            angles[angle].append(other)
    return angles


def part1(ast_list):
    asteroids = dict()
    for asteroid in ast_list:
        asteroids[asteroid] = get_angles(asteroid, ast_list)

    max_k = None
    max_v = 0
    for k, v in asteroids.items():
        if len(v) > max_v:
            max_k = k
            max_v = len(v)

    return max_k, max_v


def part2(position, ast_list):
    angles = get_angles(position, ast_list)

    # Sort the positions of asteroids by distance from the reference asteroid, for each angle
    sorted_angles = dict()
    for angle, positions in angles.items():
        new_pos = [
            (pos, (position[0] - pos[0]) ** 2 + (position[1] - pos[1]) ** 2) for pos in positions
        ]
        sorted_angles[angle] = sorted(new_pos, key=lambda x: x[1])

    rotations = sorted([angle for angle in sorted_angles if angle <= 0], reverse=True) + sorted(
        [angle for angle in sorted_angles if angle > 0], reverse=True
    )
    count = 0
    i = 0
    while count < 200:
        angle = rotations[i]
        count += 1
        popped = sorted_angles[angle].pop(0)[0]
        i += 1
    return popped


if __name__ == "__main__":
    with open(os.path.join("data", "day10_1.txt")) as f:
        lines = [el.strip() for el in f]
        ast_list = extract_asteroids(lines)
        position, neighbors = part1(ast_list)
        print(neighbors)
        popped = part2(position, ast_list)
        print(popped[0] * 100 + popped[1])
