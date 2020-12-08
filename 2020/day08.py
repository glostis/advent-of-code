import os
import re


def part1(instructions):
    accumulator, normal_finish = execute_instructions(instructions)
    assert normal_finish
    return accumulator


def part2(instructions):
    for pointer, (operation, argument) in enumerate(instructions):
        if operation == "nop":
            instructions[pointer] = ("jmp", argument)
            accumulator, normal_finish = execute_instructions(instructions)
            instructions[pointer] = ("nop", argument)
        elif operation == "jmp":
            instructions[pointer] = ("nop", argument)
            accumulator, normal_finish = execute_instructions(instructions)
            instructions[pointer] = ("jmp", argument)
        else:
            normal_finish = True
        if not normal_finish:
            return accumulator


def execute_instructions(instructions):
    accumulator = 0
    visited_instructions = set()
    pointer = 0
    while pointer not in visited_instructions:
        visited_instructions.add(pointer)
        try:
            operation, argument = instructions[pointer]
        except IndexError:
            return accumulator, False
        if operation == "acc":
            accumulator += argument
            pointer += 1
        elif operation == "jmp":
            pointer += argument
        elif operation == "nop":
            pointer += 1
        else:
            raise
    return accumulator, True


def main():
    regex = re.compile(r"(\w+) ([+-]\d+)")
    with open(os.path.join("data", "day08.txt")) as f:
        instructions = []
        for line in f:
            m = regex.match(line)
            operation, argument = m.groups()
            argument = int(argument)
            instructions.append((operation, argument))

    print(part1(instructions))
    print(part2(instructions))


if __name__ == "__main__":
    main()
