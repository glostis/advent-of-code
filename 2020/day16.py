import os
import re
from copy import deepcopy


def part1(rules, tickets):
    upper = rules[0][1]
    for rule in rules:
        for number in rule[1:]:
            if number > upper:
                upper = number
    valid_numbers = [0] * (upper + 1)
    for rule in rules:
        min1, max1, min2, max2 = rule[1:]
        for i in range(min1, max1 + 1):
            valid_numbers[i] = 1
        for i in range(min2, max2 + 1):
            valid_numbers[i] = 1

    error_rate = 0
    valid_tickets = []
    for ticket in tickets:
        good_ticket = True
        for value in ticket:
            if value >= len(valid_numbers) or valid_numbers[value] == 0:
                error_rate += value
                good_ticket = False
        if good_ticket:
            valid_tickets.append(ticket)

    return error_rate, valid_tickets


def part2(rules, tickets, my_ticket):
    field_values = [[] for _ in range(len(tickets[0]))]
    for ticket in tickets:
        for i, value in enumerate(ticket):
            field_values[i].append(value)
    number_rules = len(rules)
    rules = {rule[0]: rule[1:] for rule in rules}
    fields = dict()
    while len(fields) != number_rules:
        for i, values in enumerate(field_values):
            copy_rules = deepcopy(rules)
            for field, (min1, max1, min2, max2) in rules.items():
                for value in values:
                    if not (min1 <= value <= max1 or min2 <= value <= max2):
                        copy_rules.pop(field, None)

            # There is only one rule that fits all values of this field,
            # so we remove it from the list of available rules for other fields
            if len(copy_rules) == 1:
                key = list(copy_rules.keys())[0]
                rules.pop(key)
                fields[key] = i

    total = 1
    for k, v in fields.items():
        if k.startswith("departure"):
            total *= my_ticket[v]
    return total


def main():
    with open(os.path.join("data", "day16.txt")) as f:
        line = None
        rules = []
        regex = re.compile(r"([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$")
        while True:
            line = f.readline().strip()
            if line == "":
                break
            field, min1, max1, min2, max2 = regex.match(line).groups()
            min1, max1, min2, max2 = int(min1), int(max1), int(min2), int(max2)
            rules.append((field, min1, max1, min2, max2))

        f.readline()
        my_ticket = [int(el) for el in f.readline().strip().split(",")]

        f.readline()
        f.readline()
        nearby_tickets = []
        while True:
            line = f.readline().strip()
            if line == "":
                break
            nearby_tickets.append([int(el) for el in line.split(",")])

        error_rate, good_tickets = part1(rules, nearby_tickets)
        print(error_rate)

        print(part2(rules, good_tickets, my_ticket))


if __name__ == "__main__":
    main()
