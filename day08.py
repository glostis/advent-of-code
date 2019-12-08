import os

import numpy as np


def part1(data):
    width = 25
    height = 6
    nb_bands = int(len(data) / width / height)
    array = np.reshape(np.array([int(el) for el in data]), (nb_bands, height, width))
    count = 0
    the_band = None
    for band in array:
        _count = len(band[band != 0])
        if _count > count:
            count = _count
            the_band = band

    return len(the_band[the_band == 1]) * len(the_band[the_band == 2])


if __name__ == "__main__":
    with open(os.path.join("data", "day08_1.txt")) as f:
        data = f.read().strip()
        print(part1(data))
