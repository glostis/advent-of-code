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


OPCODES = {
    1: "Add",
    2: "Multiply",
    3: "Input",
    4: "Output",
    5: "Jump-if-true",
    6: "Jump-if-false",
    7: "Less-than",
    8: "Equals",
    9: "Change-base",
}


class Intcode:
    def __init__(self, program, pointer=0, relative_base=0):
        self.program = DynamicList(program)
        self.pointer = pointer
        self.relative_base = relative_base

        self.inputs = []
        self.outputs = []

        self.opcode = None
        self.operands = None
        self.result_address = None

    def parse_instruction(self):
        instruction = self.program[self.pointer]

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
            operand = self.program[self.pointer + i + 1]
            if operand_modes[i] == "0":
                # Position mode
                operands.append(self.program[operand])
            elif operand_modes[i] == "1":
                # Immediate mode
                operands.append(operand)
            elif operand_modes[i] == "2":
                # Relative mode
                operands.append(self.program[operand + self.relative_base])
            else:
                raise ValueError(f"Unknown operation mode {operand_modes[i]}")

        if opcode in [1, 2, 7, 8]:
            result_pointer = self.pointer + 3
            mode = operand_modes[2]
        elif opcode in [3]:
            result_pointer = self.pointer + 1
            mode = operand_modes[0]

        if opcode in [1, 2, 3, 7, 8]:
            if mode == "0":
                result_address = self.program[result_pointer]
            elif mode == "1":
                raise ValueError(
                    "Parameters that an instruction writes to will never be in immediate mode."
                )
            elif mode == "2":
                result_address = self.program[result_pointer] + self.relative_base
        else:
            result_address = None

        self.opcode = opcode
        self.operands = operands
        self.result_address = result_address

    def run_instruction(self, verbose=False):
        self.parse_instruction()

        if verbose:
            print()
            print(f"Opcode {self.opcode} - {OPCODES.get(self.opcode)}")

        if self.opcode in [1, 2]:
            skip = 4
            if self.opcode == 1:
                operation_result = self.operands[0] + self.operands[1]
            else:
                operation_result = self.operands[0] * self.operands[1]

            self.program[self.result_address] = operation_result
            if verbose:
                print(f"Storing {operation_result} to address {self.result_address}")
            self.pointer += skip

        elif self.opcode in [3, 4]:
            skip = 2
            if self.opcode == 3:
                # Take first element from list of inputs
                _input = self.inputs.pop(0)
                if verbose:
                    print(f"Storing input {_input} to address {self.result_address}")
                self.program[self.result_address] = _input
            else:
                output = self.operands[0]
                self.outputs.append(output)
                if verbose:
                    print(f"Output: {output}")
            self.pointer += skip

        elif self.opcode in [5, 6]:
            if self.opcode == 5:
                cond = self.operands[0] != 0
            else:
                cond = self.operands[0] == 0

            if verbose:
                print(f"Condition is {cond}")

            if cond:
                self.pointer = self.operands[1]
            else:
                self.pointer += 3
            if verbose:
                print(f"Setting pointer to {self.pointer}")

        elif self.opcode in [7, 8]:
            skip = 4
            if self.opcode == 7:
                res = 1 if self.operands[0] < self.operands[1] else 0
            else:
                res = 1 if self.operands[0] == self.operands[1] else 0

            self.program[self.result_address] = res

            if verbose:
                print(f"Storing result {res} at address {self.result_address}")

            self.pointer += skip

        elif self.opcode in [9]:
            skip = 2
            self.relative_base += self.operands[0]

            if verbose:
                print(f"Setting relative_base to {self.relative_base}")

            self.pointer += skip

        elif self.opcode == 99:
            pass

        else:
            raise ValueError(f"Unknown opcode {self.opcode}")

    def run_til_halt(self, verbose=False):
        while self.opcode != 99:
            self.run_instruction(verbose=verbose)

    def run_til_output(self, verbose=False):
        while self.opcode != 4:
            self.run_instruction(verbose=verbose)
