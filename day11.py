import os
from collections import defaultdict


def part1(_codes, verbose=False):
    # Stores panels painted at least once
    painted = set()

    # Stores the color of each panel, indexed by its x, y position
    panels = defaultdict(int)

    # Stores the position of the robot
    x, y = 0, 0

    # Stores the direction in which the robot is facing
    heading = 0

    point = 0
    while True:
        try:
            # Get the color of the current panel
            inp = panels[(x, y)]

            # Run the intcode computer once to get the color that should be painted
            color, _codes, point, _ = intcode_computer(
                _codes, phase_setting=inp, point=point, return_on_code_4=True, verbose=verbose
            )
            assert color in [0, 1]

            # Paint the panel
            panels[(x, y)] = color

            # Store panel in painted panels
            painted.add((x, y))

        except OpCode99:
            break

        try:
            # Run the intcode computer again to get the new robot's heading
            heading_code, _codes, point, _ = intcode_computer(
                _codes, phase_setting=inp, point=point, return_on_code_4=True, verbose=verbose
            )
            assert heading_code in [0, 1]

            # Turn the robot
            if heading_code == 0:
                heading -= 90
            else:
                heading += 90
            if heading < 0:
                heading += 360
            if heading >= 360:
                heading -= 360

            # Move the robot forward
            if heading == 0:
                y += 1
            elif heading == 90:
                x += 1
            elif heading == 180:
                y -= 1
            elif heading == 270:
                x -= 1
            else:
                raise ValueError(f"Heading {heading}")

        except OpCode99:
            break

    return painted


class OpCode99(Exception):
    pass


class DynamicList(list):
    def __setitem__(self, key, value):
        if key >= len(self):
            for _ in range(len(self), key + 1):
                self.append(0)
        return super(DynamicList, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key >= len(self):
            for _ in range(len(self), key + 1):
                self.append(0)
        return super(DynamicList, self).__getitem__(key)


def parse_instruction(codes, point, relative_base):
    instruction = codes[point]

    # Left-pad instruction with zeros to make it of length 4
    instruction = f"{instruction:05}"

    # Parse opcode
    opcode = int(instruction[-2:])

    # Parse operand modes, and reverse them (so that they are read from left to right)
    operand_modes = instruction[:-2][::-1]

    if opcode in [1, 2, 5, 6, 7, 8]:
        nb_params = 2
    elif opcode in [4, 9]:
        nb_params = 1
    else:
        # Unknown opcode, or halting code 99
        nb_params = 0

    operands = []
    for i in range(nb_params):
        operand = codes[point + i + 1]
        if operand_modes[i] == "0":
            # Position mode
            operands.append(codes[operand])
        elif operand_modes[i] == "1":
            # Immediate mode
            operands.append(operand)
        elif operand_modes[i] == "2":
            # Relative mode
            operands.append(codes[operand + relative_base])
        else:
            raise ValueError(f"Unknown operation mode {operand_modes[i]}")

    if opcode in [1, 2, 7, 8]:
        result_pointer = point + 3
        mode = operand_modes[2]
    elif opcode in [3]:
        result_pointer = point + 1
        mode = operand_modes[0]

    if opcode in [1, 2, 3, 7, 8]:
        if mode == "0":
            result_address = codes[result_pointer]
        elif mode == "1":
            raise ValueError(
                "Parameters that an instruction writes to will never be in immediate mode."
            )
        elif mode == "2":
            result_address = codes[result_pointer] + relative_base
    else:
        result_address = None

    return opcode, operands, result_address


def intcode_computer(
    _codes,
    phase_setting=None,
    input_signal=None,
    point=0,
    input_counter=0,
    return_on_code_4=False,
    verbose=False,
):
    codes = DynamicList(_codes)
    relative_base = 0
    while True:
        opcode, operands, result_address = parse_instruction(codes, point, relative_base)
        if verbose:
            print()
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
                if return_on_code_4:
                    point += skip
                    return (output, codes, point, input_counter)
            point += skip
            if verbose:
                print(f"Skipping {skip} to {point}")

        elif opcode in [5, 6]:
            if opcode == 5:
                cond = operands[0] != 0
            else:
                cond = operands[0] == 0

            if verbose:
                print(f"Condition is {cond}")

            if cond:
                point = operands[1]
            else:
                point += 3
            if verbose:
                print(f"Setting pointer to {point}")

        elif opcode in [7, 8]:
            skip = 4
            if opcode == 7:
                res = 1 if operands[0] < operands[1] else 0
            else:
                res = 1 if operands[0] == operands[1] else 0

            codes[result_address] = res

            if verbose:
                print(f"Storing result {res} at address {result_address}")

            point += skip
            if verbose:
                print(f"Skipping {skip} to {point}")

        elif opcode in [9]:
            skip = 2
            relative_base += operands[0]

            if verbose:
                print(f"Setting relative_base to {relative_base}")

            point += skip

        elif opcode == 99:
            if return_on_code_4:
                raise OpCode99("Opcode 99 was reached")
            else:
                return output
        else:
            raise ValueError(f"Unknown opcode {opcode}")
    if verbose:
        print()


if __name__ == "__main__":
    with open(os.path.join("data", "day11_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        painted = part1(codes)
        print(len(painted))
