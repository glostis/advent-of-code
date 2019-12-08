import os

import numpy as np
import rasterio


def parse_image(data):
    width = 25
    height = 6
    nb_bands = int(len(data) / width / height)
    array = np.reshape(np.array([int(el) for el in data]), (nb_bands, height, width))
    return array


def part1(data):
    count = 0
    the_band = None
    array = parse_image(data)
    for band in array:
        _count = len(band[band != 0])
        if _count > count:
            count = _count
            the_band = band

    return len(the_band[the_band == 1]) * len(the_band[the_band == 2])


def part2(data):
    array = parse_image(data)
    array = np.transpose(array, (1, 2, 0))
    image = np.zeros(array.shape[:2])
    for i in range(6):
        for j in range(25):
            stack = array[i, j, :]
            color = stack[stack != 2][0]
            image[i, j] = color

    path = os.path.join("data", "day08.tiff")
    profile = dict(driver="GTiff", width=25, height=6, count=1, dtype=image.dtype)
    with rasterio.open(path, "w", **profile) as src:
        src.write(image, 1)
    print(f"Image saved at {path}")


if __name__ == "__main__":
    with open(os.path.join("data", "day08_1.txt")) as f:
        data = f.read().strip()
        print(part1(data))
        part2(data)
