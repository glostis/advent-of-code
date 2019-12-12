import os
import re


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def update_gravity(self, moons):
        for moon in moons:
            dvx, dvy, dvz = self.compute_single_gravity(moon)
            self.vx += dvx
            self.vy += dvy
            self.vz += dvz

    def compute_single_gravity(self, moon):
        dvx = sign(moon.x - self.x)
        dvy = sign(moon.y - self.y)
        dvz = sign(moon.z - self.z)
        return dvx, dvy, dvz

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    @property
    def energy(self):
        potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic_energy = abs(self.vx) + abs(self.vy) + abs(self.vz)
        return potential_energy * kinetic_energy

    def __repr__(self):
        return (
            "Moon("
            f"<x={self.x}, y={self.y}, z={self.z}, "
            f"vx={self.vx}, vy={self.vy}, vz={self.vz}, "
            f"energy={self.energy})"
        )


def sign(a):
    return 1 if a > 0 else -1 if a < 0 else 0


def parse_file(filepath):
    with open(filepath) as f:
        lines = [line.strip() for line in f]

    moons = []
    for line in lines:
        line = re.sub(r"<(.*)>", r"\1", line)
        x = int(re.sub(r"^x=(-?[0-9]*).*$", r"\1", line))
        y = int(re.sub(r"^.*y=(-?[0-9]*).*$", r"\1", line))
        z = int(re.sub(r"^.*z=(-?[0-9]*)$", r"\1", line))
        moons.append(Moon(x, y, z))
    return moons


def part1():
    moons = parse_file(os.path.join("data", "day12_1.txt"))
    for i in range(1, 1001):
        print(f"After {i} steps:")
        for moon in moons:
            moon.update_gravity(moons)

        for moon in moons:
            moon.update_position()

        total_energy = sum([moon.energy for moon in moons])
        print(total_energy)

        print()


if __name__ == "__main__":
    part1()
