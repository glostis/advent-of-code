import itertools
import os

from intcode import Intcode


def part1(program):
    max_output = 0
    for phases in itertools.permutations(range(5)):
        input_signal = 0
        for phase in phases:
            computer = Intcode(program)
            computer.inputs = [phase, input_signal]
            computer.run_til_output()
            input_signal = computer.outputs[0]
        if input_signal > max_output:
            max_output = input_signal
    return max_output


def part2(program):
    max_output = 0
    for phases in itertools.permutations(range(5, 10)):
        input_signal = 0
        # Initialize amplifiers with their respective phase settings
        computers = []
        for phase in phases:
            computer = Intcode(program)
            computer.inputs.append(phase)
            computers.append(computer)

        i = 0
        while True:
            computer = computers[i]
            computer.inputs.append(input_signal)
            computer.run_til_output()
            if computer.opcode == 99:
                break
            input_signal = computer.outputs.pop()
            i += 1
            i = i % len(phases)

        if input_signal > max_output:
            max_output = input_signal
    return max_output


if __name__ == "__main__":
    with open(os.path.join("data", "day07_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        ret = part1(codes)
        assert ret == 929800
        print("part1 day07 OK")
        ret = part2(codes)
        assert ret == 15432220
        print("part2 day07 OK")
