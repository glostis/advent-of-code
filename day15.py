# pylint: disable=redefined-outer-name
import os

import networkx as nx

from intcode import Intcode

opposite_commands = {1: 2, 2: 1, 3: 4, 4: 3}
directions = {1: "North", 2: "South", 3: "West", 4: "East"}


def recurse_explore(path, computer, seen_positions, walls, good_path, verbose=True):
    x, y = path[-1]
    if verbose:
        print()
        print(f"Recurse called with {(x, y)}")
    neighbors = [((x, y - 1), 1), ((x, y + 1), 2), ((x - 1, y), 3), ((x + 1, y), 4)]
    outputs = []
    for neighbor_position, command in neighbors:
        if neighbor_position not in seen_positions:
            computer.inputs = [command]
            computer.run_til_output()
            assert len(computer.outputs) == 1
            output = computer.outputs.pop()
            if verbose:
                print(f"Probing {directions[command]} - Output {output}")
            if output in [1, 2]:
                computer.inputs = [opposite_commands[command]]
                computer.run_til_output()
                assert computer.outputs.pop() == 1
            elif output not in [0, 1, 2]:
                raise ValueError(f"Incorrect program output {output}")
            outputs.append(output)
        else:
            outputs.append(None)

    if verbose:
        print(f"Outputs {(x, y)} {outputs}")

    founds = []
    for output, (neighbor_position, command) in zip(outputs, neighbors):
        if output == 2:
            seen_positions.add(neighbor_position)
            good_path.extend(path)
            good_path.append(neighbor_position)
            founds.append(True)
        elif output == 1:
            seen_positions.add(neighbor_position)
            computer.inputs = [command]
            computer.run_til_output()
            out = computer.outputs.pop()
            assert out == 1, f"{out}"
            path.append(neighbor_position)
            founds.append(
                recurse_explore(
                    path,
                    computer,
                    seen_positions,
                    walls=walls,
                    good_path=good_path,
                    verbose=verbose,
                )
            )
        else:
            if output == 0:
                walls.add(neighbor_position)
            founds.append(False)

    if len(path) >= 2:
        x2, y2 = path.pop()
        x1, y1 = path[-1]
        if x2 - x1 == 1 and y2 == y1:
            backtrack_command = 3
        elif x2 - x1 == -1 and y2 == y1:
            backtrack_command = 4
        elif y2 - y1 == 1 and x2 == x1:
            backtrack_command = 1
        elif y2 - y1 == -1 and x2 == x1:
            backtrack_command = 2
        else:
            print(x1, x2, y1, y2)
            raise ValueError("WTF")
        computer.inputs = [backtrack_command]
        if verbose:
            print(f"TRACKED BACK to {path[-1]}")
        computer.run_til_output()
        assert computer.outputs.pop() == 1
    return True in founds


def part1(program, verbose=False):
    x, y = 0, 0
    path = [(x, y)]
    seen_positions = set([(x, y)])
    walls = set()

    computer = Intcode(program)

    good_path = []

    recurse_explore(
        path, computer, seen_positions, walls=walls, good_path=good_path, verbose=verbose
    )

    return good_path


def part2(program, verbose=False):
    x, y = 0, 0
    path = [(x, y)]
    seen_positions = set([(x, y)])
    walls = set()

    computer = Intcode(program)

    good_path = []

    recurse_explore(
        path, computer, seen_positions, walls=walls, good_path=good_path, verbose=verbose
    )

    oxygen_node = good_path[-1]

    g = nx.Graph()

    for x, y in seen_positions:
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for neighbor in neighbors:
            if neighbor in seen_positions:
                g.add_edge((x, y), neighbor)

    max_len = 0
    for node in g.nodes:
        max_len = max(max_len, nx.dijkstra_path_length(g, oxygen_node, node))

    return max_len


def print_positions(positions, walls, good_path):
    xmin = min(el[0] for el in positions)
    ymin = min(el[1] for el in positions)
    xmax = max(el[0] for el in positions)
    ymax = max(el[1] for el in positions)
    count = 0
    for i in range((xmax - xmin) + 3):
        line = ""
        for j in range((ymax - ymin) + 3):
            pos = (i + xmin - 1, j + ymin - 1)
            if pos == good_path[-1]:
                line += "Oo"
            elif pos in walls:
                line += "██"
            elif pos in positions:
                line += "  "
                count += 1
            else:
                line += "██"
        print(line)


def cli():
    with open(os.path.join("data", "day15_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
    print(len(part1(codes)) - 1)
    print(part2(codes))


if __name__ == "__main__":
    cli()
