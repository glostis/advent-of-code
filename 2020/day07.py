import os
import re


def part1(rules):
    return len(who_can_contain("shiny gold", rules))


def who_can_contain(color, rules):
    colors = set()
    for rule in rules:
        containing, contained = rule
        contained_colors = [el[1] for el in contained]
        if color in contained_colors:
            colors.add(containing)
            for c in who_can_contain(containing, rules):
                colors.add(c)
    return colors


def part2(rules):
    return contains_how_many("shiny gold", rules)


def contains_how_many(color, rules):
    how_many = 0
    for rule in rules:
        containing, contained = rule
        if containing == color:
            if contained is not None:
                for number, c in contained:
                    how_many += number * 1
                    how_many += number * contains_how_many(c, rules)
    return how_many


def parse_rules(rules):
    ret = []
    regex1 = re.compile(r"(?P<containing>\w+ \w+) bags contain (?P<contained>.*)$")
    regex2 = re.compile(r"(?P<number>\d+) (?P<color>\w+ \w+) bags?")
    for rule in rules:
        m = regex1.match(rule)
        containing_color, contained = m.group("containing"), m.group("contained")
        contained_colors = []
        for s in contained.split(", "):
            m = regex2.match(s)
            if m:
                number = int(m.group("number"))
                color = m.group("color")
                contained_colors.append((number, color))
        ret.append((containing_color, contained_colors))
    return ret


def main():
    with open(os.path.join("data", "day07.txt")) as f:
        rules = [line.strip() for line in f]
    rules = parse_rules(rules)

    print(part1(rules))
    print(part2(rules))


if __name__ == "__main__":
    main()
