import os

import numpy as np


def part1(_codes):
    codes = _codes.copy()
    for i, opcode in enumerate(codes[::4]):
        j = i * 4
        operand_indices = codes[j + 1 : j + 3]
        result_index = codes[j + 3]
        # print(opcode, operand_indices, result_index)
        if opcode == 1:
            result = codes[operand_indices[0]] + codes[operand_indices[1]]
            codes[result_index] = result
        elif opcode == 2:
            result = codes[operand_indices[0]] * codes[operand_indices[1]]
            codes[result_index] = result
        elif opcode == 99:
            break
        else:
            raise
    return codes[0]


def part2(codes):
    for noun in range(100):
        for verb in range(100):
            _codes = codes.copy()
            _codes[1] = noun
            _codes[2] = verb
            ret = part1(_codes)
            if ret == 19690720:
                return 100 * noun + verb


if __name__ == "__main__":
    with open(os.path.join("data", "day02_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        codes[1] = 12
        codes[2] = 2
        print(part1(codes))

    with open(os.path.join("data", "day02_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        print(part2(codes))
