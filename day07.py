import itertools
import os


def part1(_codes, verbose=False):
    max_output = 0
    for phases in itertools.permutations(range(5)):
        input_signal = 0
        for phase in phases:
            output = intcode_computer(_codes, phase, input_signal, verbose=verbose)
            input_signal = output
        if output > max_output:
            max_output = output
    return max_output


class OpCode99(Exception):
    pass


def part2(_codes, verbose=False):
    max_output = 0
    for phases in itertools.permutations(range(5, 10)):
        input_signal = 0
        # Initialize amplifiers with their respective phase settings
        states = dict()
        for phase in phases:
            output, __codes, point, input_counter = intcode_computer(
                _codes, phase, input_signal, return_on_output=True, verbose=verbose
            )
            states[phase] = (__codes.copy(), point, input_counter)
            input_signal = output
        i = 0
        while True:
            __codes, point, input_counter = states[phases[i]]
            try:
                o = intcode_computer(
                    __codes,
                    input_signal=input_signal,
                    point=point,
                    input_counter=input_counter,
                    return_on_output=True,
                    verbose=verbose,
                )
            except OpCode99:
                break
            input_signal, __codes, point, input_counter = o
            states[phases[i]] = (__codes, point, input_counter)
            i += 1
            if i == 5:
                i = 0
        if input_signal > max_output:
            max_output = input_signal
    return max_output


def parse_instruction(codes, point):
    instruction = codes[point]

    # Left-pad instruction with zeros to make it of length 4
    instruction = f"{instruction:05}"

    # Parse opcode
    opcode = int(instruction[-2:])

    # Parse operand modes, and reverse them (so that they are read from left to right)
    operand_modes = instruction[:-2][::-1]

    if opcode in [1, 2, 5, 6, 7, 8]:
        nb_params = 2
    elif opcode in [4]:
        nb_params = 1
    else:
        # Unknown opcode, or halting code 99
        nb_params = 0

    operands = []
    for i in range(nb_params):
        operand = codes[point + i + 1]
        if operand_modes[i] == "0":
            # Address mode
            operands.append(codes[operand])
        elif operand_modes[i] == "1":
            # Immediate mode
            operands.append(operand)
        else:
            raise ValueError(f"Unknown operation mode {operand_modes[i]}")

    if opcode in [1, 2]:
        result_address = codes[point + 3]
        if operand_modes[2] != "0":
            raise ValueError(
                "Parameters that an instruction writes to will never be in immediate mode."
            )
    elif opcode in [3]:
        result_address = codes[point + 1]
        if operand_modes[0] != "0":
            raise ValueError(
                "Parameters that an instruction writes to will never be in immediate mode."
            )
    else:
        result_address = None

    return opcode, instruction, operands, result_address


def intcode_computer(
    _codes,
    phase_setting=None,
    input_signal=None,
    point=0,
    input_counter=0,
    return_on_output=False,
    verbose=False,
):
    codes = _codes.copy()
    while True:
        opcode, instruction, operands, result_address = parse_instruction(codes, point)
        if verbose:
            print(f"Opcode {opcode}")

        if opcode in [1, 2]:
            skip = 4
            if opcode == 1:
                operation_result = operands[0] + operands[1]
            else:
                operation_result = operands[0] * operands[1]

            codes[result_address] = operation_result
            if verbose:
                print(f"Storing {operation_result} to address {result_address}")
            point += skip
            if verbose:
                print(f"Skipping {skip} to {point}")

        elif opcode in [3, 4]:
            skip = 2
            if opcode == 3:
                if input_counter == 0:
                    _input = phase_setting
                else:
                    _input = input_signal
                input_counter += 1
                if verbose:
                    print(f"Storing input {_input} to address {result_address}")
                codes[result_address] = _input
            else:
                output = operands[0]
                if verbose:
                    print(f"Output: {output}")
                if return_on_output:
                    point += skip
                    return (output, codes, point, input_counter)
            point += skip
            if verbose:
                print(f"Skipping {skip} to {point}")

        elif opcode in [5, 6]:
            param1 = codes[point + 1]
            param1_mode = instruction[-3]
            if param1_mode == "0":
                param1_value = codes[param1]
            else:
                param1_value = param1

            param2 = codes[point + 2]
            param2_mode = instruction[-4]
            if param2_mode == "0":
                param2_value = codes[param2]
            else:
                param2_value = param2

            if opcode == 5:
                cond = param1_value != 0
            else:
                cond = param1_value == 0

            if cond:
                point = param2_value
            else:
                point += 3

        elif opcode in [7, 8]:
            skip = 4
            param1 = codes[point + 1]
            param1_mode = instruction[-3]
            if param1_mode == "0":
                param1_value = codes[param1]
            else:
                param1_value = param1

            param2 = codes[point + 2]
            param2_mode = instruction[-4]
            if param2_mode == "0":
                param2_value = codes[param2]
            else:
                param2_value = param2

            param3 = codes[point + 3]
            param3_mode = instruction[-5]
            if param3_mode != "0":
                raise ValueError(
                    "Parameters that an instruction writes to will never be in immediate mode."
                )

            if opcode == 7:
                res = 1 if param1_value < param2_value else 0
            else:
                res = 1 if param1_value == param2_value else 0

            codes[param3] = res
            point += skip
            if verbose:
                print(f"Skipping {skip} to {point}")

        elif opcode == 99:
            if return_on_output:
                raise OpCode99("Opcode 99 was reached")
            else:
                return output
        else:
            raise
    if verbose:
        print()


if __name__ == "__main__":
    with open(os.path.join("data", "day07_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        print(part1(codes))
        print(part2(codes))
