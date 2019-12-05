import os

import numpy as np


def part1(_codes, verbose=False):
    output = intcode_computer(_codes, _input=1, verbose=verbose)
    return output


def part2(_codes, verbose=True):
    output = intcode_computer(_codes, _input=5)
    return output


def intcode_computer(_codes, _input, verbose=True):
    codes = _codes.copy()
    point = 0
    _input = 1
    while True:
        instruction = codes[point]

        # Left-pad instruction with zeros to make it of length 4
        instruction = f"{instruction:05}"
        opcode = int(instruction[-2:])
        if verbose:
            print(f"Opcode {opcode}")

        if opcode in [1, 2]:
            skip = 4
            operand_1 = codes[point + 1]
            operand_1_mode = instruction[-3]
            if operand_1_mode == "0":
                operand_1_value = codes[operand_1]
            else:
                operand_1_value = operand_1

            operand_2 = codes[point + 2]
            operand_2_mode = instruction[-4]
            if operand_2_mode == "0":
                operand_2_value = codes[operand_2]
            else:
                operand_2_value = operand_2

            if opcode == 1:
                operation_result = operand_1_value + operand_2_value
            else:
                operation_result = operand_1_value * operand_2_value

            result = codes[point + 3]
            result_mode = instruction[-5]
            if result_mode != "0":
                print(instruction)
                print(result_mode)
                raise ValueError(
                    "Parameters that an instruction writes to will never be in immediate mode."
                )

            codes[result] = operation_result
            if verbose:
                print(f"Storing {operation_result} to address {result}")
        elif opcode in [3, 4]:
            skip = 2
            parameter = codes[point + 1]
            parameter_mode = instruction[-3]
            if opcode == 3:
                if parameter_mode != "0":
                    raise ValueError("Param mode not 0 for opcode 3")
                if verbose:
                    print(f"Storing input {_input} to address {parameter}")
                codes[parameter] = _input
            else:
                if parameter_mode == "0":
                    output = codes[parameter]
                else:
                    output = int(parameter)
                print(f"Output: {output}")
        elif opcode == 99:
            break
        else:
            raise
        point += skip
        if verbose:
            print(f"Skipping {skip} to {point}")
    return output


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
    with open(os.path.join("data", "day05_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        print(part1(codes))
