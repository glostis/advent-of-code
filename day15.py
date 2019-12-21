# pylint: disable=redefined-outer-name
import os

from intcode import Intcode


opposite_commands = {1: 2, 2: 1, 3: 4, 4: 3}
directions = {1: "North", 2: "South", 3: "West", 4: "East"}


def recurse_explore(path, computer, seen_positions, good_path, verbose=True):
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
    for i, output in enumerate(outputs):
        if output == 2:
            neighbor_position, _ = neighbors[i]
            seen_positions.add(neighbor_position)
            good_path.extend(path)
            good_path.append(neighbor_position)
            founds.append(True)
        elif output == 1:
            neighbor_position, command = neighbors[i]
            seen_positions.add(neighbor_position)
            computer.inputs = [command]
            computer.run_til_output()
            out = computer.outputs.pop()
            assert out == 1, f"{out}"
            path.append(neighbor_position)
            founds.append(
                recurse_explore(
                    path, computer, seen_positions, good_path=good_path, verbose=verbose
                )
            )
        else:
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

    computer = Intcode(program)

    good_path = []

    recurse_explore(path, computer, seen_positions, good_path=good_path, verbose=verbose)
    return good_path


def cli():
    with open(os.path.join("data", "day15_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
    print(len(part1(codes)) - 1)


if __name__ == "__main__":
    cli()
