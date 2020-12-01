import os

from intcode import Intcode


def part1(program, verbose=False):
    count = 0
    for y in range(50):
        for x in range(50):
            computer = Intcode(program)
            computer.inputs = [x, y]
            computer.run_til_halt()
            output = computer.outputs.pop()
            if output == 1:
                count += 1
            if verbose:
                print(output, end="")
        if verbose:
            print()
    return count


def part2(program):
    ymin = 1000
    ymax = 2000
    xmin = 0
    xmax = int(ymin * 1.3)
    mins = []
    maxs = []
    for y in range(ymin, ymax):
        # Get left boundary of beam
        x = xmin
        while not xy_in_beam(program, x, y):
            x += 1
        mins.append(x)
        xmin = x - 1

        # Get right boundary of beam
        x = xmax
        while not xy_in_beam(program, x, y):
            x -= 1
        maxs.append(x)
        xmax = x + 1

    for i, y in enumerate(range(ymin, ymax - 99)):
        for x in range(mins[i], maxs[i]):
            if x + 99 <= maxs[i] and x >= mins[i + 99]:
                return x * 10000 + y


def xy_in_beam(program, x, y):
    computer = Intcode(program)
    computer.inputs = [x, y]
    computer.run_til_halt()
    output = computer.outputs.pop()
    return output == 1


def cli():
    with open(os.path.join("data", "day19_1.txt")) as f:
        program = [int(el) for el in f.readline().split(",")]
    print(part1(program))
    print(part2(program))


if __name__ == "__main__":
    cli()
