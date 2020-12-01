import os

import numpy as np


def part1(masses):
    fuels = np.floor(np.array(masses) / 3) - 2
    return np.sum(fuels)


def fuel_from_mass(mass):
    total_fuel = 0
    fuel = np.floor(mass / 3) - 2
    while fuel > 0:
        total_fuel += fuel
        fuel = np.floor(fuel / 3) - 2
    return total_fuel


def part2(masses):
    fuels = np.sum([fuel_from_mass(mass) for mass in masses])
    return fuels


if __name__ == "__main__":
    with open(os.path.join("data", "day01_1.txt")) as f:
        print(part1([int(line.strip()) for line in f]))

    with open(os.path.join("data", "day01_1.txt")) as f:
        print(part2([int(line.strip()) for line in f]))
