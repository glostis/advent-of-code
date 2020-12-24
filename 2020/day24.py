import os
from collections import defaultdict


def part1(instructions):
    black_tiles = set()
    for instruction in instructions:
        x, y = 0, 0
        for direction in instruction:
            if direction in ["e", "w"]:
                sign = +1 if direction == "e" else -1
                x += sign * 2
            else:
                sign_y = +1 if direction[0] == "n" else -1
                y += sign_y * 1
                sign_x = +1 if direction[1] == "e" else -1
                x += sign_x * 1
        if (x, y) not in black_tiles:
            black_tiles.add((x, y))
        else:
            black_tiles.remove((x, y))
    return black_tiles


def part2(black_tiles):
    for _ in range(100):
        new_black_tiles = set()
        white_tiles_neighbors = defaultdict(int)
        for black_tile in black_tiles:
            black_neighbors = 0
            for neighbor in neighbors(*black_tile):
                if neighbor in black_tiles:
                    black_neighbors += 1
                else:
                    white_tiles_neighbors[neighbor] += 1

            if black_neighbors == 0 or black_neighbors > 2:
                pass
            else:
                new_black_tiles.add(black_tile)

        for white_tile, black_neighbors in white_tiles_neighbors.items():
            if black_neighbors == 2:
                new_black_tiles.add(white_tile)
        black_tiles = new_black_tiles
    return black_tiles


def neighbors(x, y):
    return (x - 2, y), (x + 2, y), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1)


def main():
    instructions = []
    with open(os.path.join("data", "day24.txt")) as f:
        for line in f:
            instruction = []
            line = line.strip()
            pointer = 0
            while pointer < len(line):
                char = line[pointer]
                if char in ["e", "w"]:
                    instruction.append(char)
                    pointer += 1
                elif char in ["n", "s"]:
                    instruction.append(char + line[pointer + 1])
                    pointer += 2
            instructions.append(instruction)

    black_tiles = part1(instructions)
    print(len(black_tiles))
    print(len(part2(black_tiles)))


if __name__ == "__main__":
    main()
