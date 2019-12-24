import os


from intcode import Intcode


def part1(program, verbose=False):
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


def cli():
    with open(os.path.join("data", "day17_1.txt")) as f:
        program = [int(el) for el in f.readline().split(",")]
    print(part1(program))


if __name__ == "__main__":
    cli()
