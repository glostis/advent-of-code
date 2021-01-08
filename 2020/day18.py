import os
from collections import defaultdict


def part1(lines):
    total = 0
    for line in lines:
        ops = parse_line(line)
        ops = add_precedence(ops)
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
    return flatten_expr(chars, 1)


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
        if isinstance(ops[0], int):
            return ops[0]
        else:
            return compute_value(ops[0])
    operand1, operator, operand2 = ops[:3]
    if isinstance(operand1, list):
        operand1 = compute_value(operand1)
    if isinstance(operand2, list):
        print(operand2)
        operand2 = compute_value(operand2)
        print(operand2)
    value = operate(operand1, operator, operand2)
    return compute_value([value] + ops[3:])


def add_precedence(l):
    new_l = []
    i = 0
    while i < len(l):
        el = l[i]
        if el == "+":
            previous_operand = new_l.pop()
            next_operand = l[i + 1]
            if isinstance(next_operand, list):
                next_operand = add_precedence(next_operand)
            new_l.append([previous_operand, "+", next_operand])
            i += 1
        elif isinstance(el, list):
            new_l.append(add_precedence(el))
        else:
            new_l.append(el)
        i += 1
    return new_l


def main():
    with open(os.path.join("data", "day18.txt")) as f:
        lines = [f"({line.strip()})" for line in f]

    return part1(lines)


if __name__ == "__main__":
    main()
