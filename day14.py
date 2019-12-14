import os
from collections import defaultdict, namedtuple
import numpy as np


def part1(filepath):
    ore_count = make_fuel(filepath, 1)
    return ore_count


def part2(filepath):
    # Dichotomic search of the fuel quantity "needed" to use up the ore target
    ore_target = 1000000000000
    fuel_min = 0
    fuel_max = 1000000000000
    ore_count = 0

    while fuel_max - fuel_min > 1:
        fuel_quantity = int((fuel_max + fuel_min) / 2)
        ore_count = make_fuel(filepath, fuel_quantity)
        if ore_target - ore_count > 0:
            fuel_min = fuel_quantity
        else:
            fuel_max = fuel_quantity
    return fuel_quantity


def make_fuel(filepath, fuel_quantity):
    reactions = readfile(filepath)
    production = dict()
    for reaction in reactions:
        output = reaction.output[1]
        production[output] = reaction

    ore_count = 0
    materials = defaultdict(int)
    ore_count = make_material(production, "FUEL", fuel_quantity, materials, ore_count)
    return ore_count


def make_material(production, material, quantity, materials, ore_count):
    if material == "ORE":
        ore_count += quantity
        return ore_count
    reaction = production[material]
    quantity -= materials[material]
    materials[material] = 0
    output_quantity = reaction.output[0]
    reaction_multiplier = int(np.ceil(quantity / output_quantity))
    leftover = reaction_multiplier * output_quantity - quantity
    materials[material] += leftover
    for quant, reactor in reaction.inputs:
        ore_count = make_material(
            production, reactor, quant * reaction_multiplier, materials, ore_count
        )
    return ore_count


def readfile(filepath):
    Reaction = namedtuple("Reaction", ["inputs", "output"])
    with open(filepath) as f:
        lines = [el.strip() for el in f]
        reactions = []
        for line in lines:
            a, b = line.split(" => ")
            inputs = [el.split(" ") for el in a.split(", ")]
            inputs = [(int(i), j) for i, j in inputs]
            outputs = b.split(" ")
            outputs = (int(outputs[0]), outputs[1])
            reactions.append(Reaction(inputs, outputs))
    return reactions


if __name__ == "__main__":
    print(part1(os.path.join("data", "day14_1.txt")))
    print(part2(os.path.join("data", "day14_1.txt")))
