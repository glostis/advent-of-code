import os
import numpy as np
import rasterio


def get_bpass_id(bpass):
    row_min, col_min = 0, 0
    row_max, col_max = 127, 7
    for separator in bpass:
        if separator == "F":
            row_max -= ((row_max - row_min) + 1) / 2
        elif separator == "B":
            row_min += ((row_max - row_min) + 1) / 2
        if separator == "L":
            col_max -= ((col_max - col_min) + 1) / 2
        elif separator == "R":
            col_min += ((col_max - col_min) + 1) / 2
    assert row_min == row_max
    assert col_min == col_max
    return row_min, col_min


def part1(passes):
    highest_id = 0
    for _pass in passes:
        row, col = get_bpass_id(_pass)
        highest_id = max(highest_id, row * 8 + col)
    return int(highest_id)


def part2(passes):
    ids = set()
    for _pass in passes:
        row, col = get_bpass_id(_pass)
        row, col = int(row), int(col)
        id = int(row * 8 + col)
        ids.add(id)
    all_ids = set(range(min(ids), max(ids)))
    the_id = all_ids - ids
    assert len(the_id) == 1
    return the_id.pop()


def main():
    with open(os.path.join("data", "day05.txt")) as f:
        passes = [line.strip() for line in f]
    print(part1(passes))
    print(part2(passes))


if __name__ == "__main__":
    main()
