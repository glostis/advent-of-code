import os

from intcode import Intcode


def part1(program):
    computer = Intcode(program)
    computer.inputs.append(1)
    computer.run_til_halt()
    assert len(computer.outputs) == 1
    output = computer.outputs[0]
    return output


def part2(program):
    computer = Intcode(program)
    computer.inputs.append(2)
    computer.run_til_halt()
    assert len(computer.outputs) == 1
    output = computer.outputs[0]
    return output


if __name__ == "__main__":
    with open(os.path.join("data", "day09_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        ret = part1(codes)
        assert ret == 2955820355
        print("part1 day09 OK")
        ret = part2(codes)
        assert ret == 46643
        print("part2 day09 OK")
