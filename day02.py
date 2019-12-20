import os

from intcode import Intcode


def part1(program):
    computer = Intcode(program)
    computer.run_til_halt()
    return computer.program[0]


def part2(codes):
    for noun in range(100):
        for verb in range(100):
            codes[1] = noun
            codes[2] = verb
            ret = part1(codes)
            if ret == 19690720:
                return 100 * noun + verb


def main():
    with open(os.path.join("data", "day02_1.txt")) as f:
        program = [int(code) for code in f.read().split(",")]
        program[1] = 12
        program[2] = 2
    ret = part1(program)
    assert ret == 3306701
    print("part1 day02 OK")

    with open(os.path.join("data", "day02_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
    ret = part2(codes)
    assert ret == 7621
    print("part2 day02 OK")


if __name__ == "__main__":
    main()
