import os

from intcode import Intcode


def part1(program):
    computer = Intcode(program)
    computer.inputs.append(1)
    computer.run_til_halt()
    output = computer.outputs.pop()
    assert all([el == 0 for el in computer.outputs])
    return output


def part2(program):
    computer = Intcode(program)
    computer.inputs.append(5)
    computer.run_til_halt()
    assert len(computer.outputs) == 1
    output = computer.outputs.pop()
    return output


if __name__ == "__main__":
    with open(os.path.join("data", "day05_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        ret = part1(codes)
        assert ret == 7259358
        print("part1 day05 OK")
        ret = part2(codes)
        assert ret == 11826654
        print("part2 day05 OK")
