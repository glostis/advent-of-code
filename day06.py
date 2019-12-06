import os


def part1(orbits):
    chain = dict()

    for center, satellite in orbits:
        chain[satellite] = center

    count = 0
    for satellite, center in chain.items():
        while True:
            count += 1
            if center == "COM":
                break
            else:
                satellite = center
                center = chain[center]
    return count


if __name__ == "__main__":
    with open(os.path.join("data", "day06_1.txt")) as f:
        orbits = [orbit.strip().split(")") for orbit in f]
        print(part1(orbits))
