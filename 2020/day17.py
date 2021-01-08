import itertools
import os
from copy import deepcopy


def part1(active_cubes, dims):
    count = 0
    offset = 0
    while count < 6:
        count += 1
        dims = tuple(dim + 2 for dim in dims)
        offset += 1
        active_cubes = execute_cycle(active_cubes, dims, offset)

    return len(active_cubes)


def draw_cubes(active_cubes, dim_x, dim_y, dim_z, offset):
    for z in range(dim_z):
        for y in range(dim_y):
            string = ""
            for x in range(dim_x):
                if (x - offset, y - offset, z - offset) in active_cubes:
                    string += "#"
                else:
                    string += "."
            print(string)
        print()


def execute_cycle(active_cubes, dims, offset):
    ori_cubes = deepcopy(active_cubes)
    for coords in itertools.product(*[range(dim) for dim in dims]):
        coords = tuple(coord - offset for coord in coords)
        active_neighbors = 0
        for delta_coords in itertools.product([-1, 0, 1], repeat=len(dims)):
            if delta_coords == (0, 0, 0):
                continue
            new_coords = tuple(
                coord + delta_coord for (coord, delta_coord) in zip(coords, delta_coords)
            )
            if new_coords in ori_cubes and all(
                0 <= new_coord + offset < dim for (new_coord, dim) in zip(new_coords, dims)
            ):
                active_neighbors += 1
        if coords in ori_cubes:
            if not active_neighbors in (2, 3):
                active_cubes.remove(coords)
        elif active_neighbors == 3:
            active_cubes.add(coords)

    return active_cubes


def main():
    with open(os.path.join("data", "day17.txt")) as f:
        # with open("t.txt") as f:
        lines = [line.strip() for line in f]

    z, w = 0, 0
    dim_z, dim_w = 1, 1
    dim_x = len(lines[0])
    dim_y = len(lines)
    active_cubes = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                active_cubes.add((x, y, z, w))

    print(part1(active_cubes, (dim_x, dim_y, dim_z, dim_w)))


if __name__ == "__main__":
    main()
