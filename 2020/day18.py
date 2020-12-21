import os
from collections import defaultdict


def part1(lines):
    total = 0
    for line in lines:
        chars = parse_line(line)
        ops = flatten_expr(chars, 1)
        value = compute_value(ops)
        total += value
    return total


def parse_line(line):
    level = 0
    chars = defaultdict(list)
    accum = []
    for char in line:
        if char == "(":
            accum.append("?")
            chars[level].append(accum)
            level += 1
            accum = []
        elif char == ")":
            chars[level].append(accum)
            level -= 1
            accum = chars[level].pop(-1)
        elif char != " ":
            try:
                char = int(char)
            except ValueError:
                pass
            accum.append(char)
    return chars


def operate(operand1, operator, operand2):
    if operator == "+":
        return operand1 + operand2
    else:
        return operand1 * operand2


def flatten_expr(chars, offset):
    ops = chars[offset].pop(0)
    new_ops = []
    for char in ops:
        if char == "?":
            new_ops.append(flatten_expr(chars, offset + 1))
        else:
            new_ops.append(char)
    return new_ops


def compute_value(ops):
    if len(ops) == 1:
        return ops[0]
    operand1, operator, operand2 = ops[:3]
    if isinstance(operand1, list):
        operand1 = compute_value(operand1)
    if isinstance(operand2, list):
        operand2 = compute_value(operand2)
    value = operate(operand1, operator, operand2)
    return compute_value([value] + ops[3:])


def main():
    with open(os.path.join("data", "day18.txt")) as f:
        lines = [f"({line.strip()})" for line in f]

    print(part1(lines))


if __name__ == "__main__":
    main()
