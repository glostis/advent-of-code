# pylint: disable=redefined-outer-name
import os
from collections import defaultdict

import numpy as np

from intcode import Intcode


def part1(program):
    painted, _ = paint_panels(program)
    return painted


def part2(program):
    _, panels = paint_panels(program, starting_color=1)

    positions = np.array(list(panels.keys()))
    xmin, ymin = np.min(positions, axis=0)
    xmax, ymax = np.max(positions, axis=0)
    canvas = np.zeros(((ymax - ymin + 1), (xmax - xmin + 1)))
    for k, v in panels.items():
        if v == 1:
            canvas[(ymax - ymin) - (k[1] - ymin), k[0] - xmin] = 1
    for line in canvas:
        st = ""
        for char in line:
            if char == 1:
                st += "█"
            else:
                st += " "
        print(st)


def paint_panels(program, starting_color=0):
    # Stores panels painted at least once
    painted = set()

    # Stores the color of each panel, indexed by its x, y position
    panels = defaultdict(int)

    # Stores the position of the robot
    x, y = 0, 0

    # Paint the starting panel in the given color
    panels[(x, y)] = starting_color

    # Stores the direction in which the robot is facing
    heading = 0

    computer = Intcode(program)
    while True:
        # Get the color of the current panel
        inp = panels[(x, y)]

        # Run the intcode computer once to get the color that should be painted
        computer.inputs.append(inp)
        computer.run_til_output()
        if computer.opcode == 99:
            break
        color = computer.outputs.pop()
        assert color in [0, 1]

        # Paint the panel
        panels[(x, y)] = color

        # Store panel in painted panels
        painted.add((x, y))

        # Run the intcode computer again to get the new robot's heading
        computer.run_til_output()
        if computer.opcode == 99:
            break
        heading_code = computer.outputs.pop()
        assert heading_code in [0, 1]

        # Turn the robot
        if heading_code == 0:
            heading -= 90
        else:
            heading += 90
        heading = heading % 360

        # Move the robot forward
        if heading == 0:
            y += 1
        elif heading == 90:
            x += 1
        elif heading == 180:
            y -= 1
        elif heading == 270:
            x -= 1
        else:
            raise ValueError(f"Heading {heading}")

    return painted, panels


if __name__ == "__main__":
    with open(os.path.join("data", "day11_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        painted = part1(codes)
        assert len(painted) == 2255
        print("part1 day11 OK")
        part2(codes)
        print("part2 day11 OK")
