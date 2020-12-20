import re
import os


def part1(rules, messages):
    regex = re.compile(r"[ab|\s()]+$")
    rule_zero = rules.pop("0")
    while not regex.match(rule_zero):
        new_rule_zero = []
        for rule_number in rule_zero.split(" "):
            if rule_number in rules:
                new_rule_zero.append(f"( {rules[rule_number]} )")
            else:
                new_rule_zero.append(rule_number)
        rule_zero = " ".join(new_rule_zero)
    rule_zero = rule_zero.replace(" ", "")
    regex = re.compile(fr"{rule_zero}$")
    count = 0
    for message in messages:
        if regex.match(message):
            count += 1
    return count


def part2(rules, messages):
    regex = re.compile(r"[ab|\s()]+$")
    rule_42 = rules.pop("42")
    while not regex.match(rule_42):
        new_rule = []
        for rule_number in rule_42.split(" "):
            if rule_number in rules:
                new_rule.append(f"( {rules[rule_number]} )")
            else:
                new_rule.append(rule_number)
        rule_42 = " ".join(new_rule)

    rule_31 = rules.pop("31")
    while not regex.match(rule_31):
        new_rule = []
        for rule_number in rule_31.split(" "):
            if rule_number in rules:
                new_rule.append(f"( {rules[rule_number]} )")
            else:
                new_rule.append(rule_number)
        rule_31 = " ".join(new_rule)

    rule_42 = rule_42.replace(" ", "")
    rule_31 = rule_31.replace(" ", "")
    regex_42 = re.compile(fr"{rule_42}")
    regex_31 = re.compile(fr"{rule_31}")
    count = 0
    for message in messages:
        m = regex_42.match(message)
        if m is None:
            continue
        c_42 = 0
        while m is not None:
            message = message[m.span()[-1]:]
            m = regex_42.match(message)
            c_42 += 1
        m = regex_31.match(message)
        if m is None:
            continue
        c_31 = 0
        while m is not None:
            message = message[m.span()[-1]:]
            m = regex_31.match(message)
            c_31 += 1
        if c_42 >= c_31 + 1 and message == "":
            count += 1
    return count


def main():
    with open(os.path.join("data", "day19.txt")) as f:
    # with open("t.txt") as f:
        rules = dict()
        while True:
            line = f.readline().strip()
            if line == "":
                break
            rule_number, rule = line.split(": ")
            rules[rule_number] = rule.replace('"', "")

        messages = [line.strip() for line in f]

    print(part2(rules, messages))


if __name__ == "__main__":
    main()
