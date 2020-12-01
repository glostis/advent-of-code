import os


from intcode import Intcode


def part1(program, verbose=True):
    computer = Intcode(program)
    computer.run_til_halt()
    ascii_codes = computer.outputs
    col, line = 0, 0
    scaffolds = set()
    for code in ascii_codes:
        if chr(code) == "#":
            scaffolds.add((col, line))
        col += 1

        if code == 10:
            line += 1
            col = 0

    cols = max(el[0] for el in scaffolds) + 1
    lines = max(el[1] for el in scaffolds) + 1

    camera = ""
    alignment_params = []
    for line in range(lines):
        for col in range(cols):
            if (col, line) in scaffolds:
                if (
                    (col + 1, line) in scaffolds
                    and (col - 1, line) in scaffolds
                    and (col, line + 1) in scaffolds
                    and (col, line - 1) in scaffolds
                ):
                    camera += "O"
                    alignment_params.append(col * line)
                else:
                    camera += "#"
            else:
                camera += " "
        camera += "\n"

    if verbose:
        print(camera)
    return sum(alignment_params)


def part2(program):
    computer = Intcode(program)
    computer.run_til_halt()
    ascii_codes = computer.outputs
    col, line = 0, 0
    scaffolds = set()
    for code in ascii_codes:
        if code == 10:
            line += 1
            col = 0
            continue

        if chr(code) == "#":
            scaffolds.add((col, line))
        elif chr(code) == ".":
            pass
        else:
            robot_line = line
            robot_col = col
        col += 1

    orientation = 0
    forward_count = 0
    command = ""
    while True:
        if orientation == 0:
            pos = (robot_col, robot_line - 1)
        elif orientation == 1:
            pos = (robot_col + 1, robot_line)
        elif orientation == 2:
            pos = (robot_col, robot_line + 1)
        elif orientation == 3:
            pos = (robot_col - 1, robot_line)
        else:
            raise ValueError(f"Bad orientation {orientation}")
        if pos in scaffolds:
            # We can move forward
            forward_count += 1
            robot_col, robot_line = pos
        else:
            # We cannot move forward, so we look in which direction we can turn
            if orientation in [0, 2]:
                if (robot_col - 1, robot_line) in scaffolds:
                    new_orientation = 3
                elif (robot_col + 1, robot_line) in scaffolds:
                    new_orientation = 1
                else:
                    break
            else:
                if (robot_col, robot_line - 1) in scaffolds:
                    new_orientation = 0
                elif (robot_col, robot_line + 1) in scaffolds:
                    new_orientation = 2
                else:
                    break

            if new_orientation - orientation == 1 or orientation == 3 and new_orientation == 0:
                command += f"{forward_count},R,"
            elif new_orientation - orientation == -1 or orientation == 0 and new_orientation == 3:
                command += f"{forward_count},L,"
            else:
                print(new_orientation, orientation)
                raise
            forward_count = 0
            orientation = new_orientation

    command = command[2:]  # Remove leading "0,"
    command = command[:-3]  # Remove trailing turn and comma
    command += (
        ",R,8"
    )  # Add "useless" commands at the end (without them, the end doesn't exactly match "B")
    A = "L,4,L,10,L,6"
    B = "L,6,L,4,R,8,R,8"
    C = "L,6,R,8,L,10,L,8,L,8"
    routine = command.replace(A, "A")
    routine = routine.replace(B, "B")
    routine = routine.replace(C, "C")
    for st in [routine, A, B, C]:
        assert len(st) <= 20

    program[0] = 2
    computer = Intcode(program)
    for string in [routine, A, B, C, "n"]:
        for char in string:
            computer.inputs.append(ord(char))
        computer.inputs.append(ord("\n"))
    computer.run_til_halt()
    return computer.outputs[-1]


def cli():
    with open(os.path.join("data", "day17_1.txt")) as f:
        program = [int(el) for el in f.readline().split(",")]
    print(part1(program))
    print(part2(program))


if __name__ == "__main__":
    cli()
