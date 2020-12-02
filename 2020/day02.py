import re
import os


def is_good_pwd(lower, upper, letter, pwd):
    count = 0
    for let in pwd:
        if let == letter:
            count += 1
        if count > upper:
            return False
    if count < lower:
        return False
    else:
        return True


def part1(data):
    good = 0
    for lower, upper, letter, pwd in data:
        if is_good_pwd(lower, upper, letter, pwd):
            good += 1
    return good


def is_good_pwd_2(pos1, pos2, letter, pwd):
    let1 = pwd[pos1 - 1]
    let2 = pwd[pos2 - 1]
    if (let1 == letter) or (let2 == letter):
        if not (let1 == let2):
            return True
    return False


def part2(data):
    good = 0
    for pos1, pos2, letter, pwd in data:
        if is_good_pwd_2(pos1, pos2, letter, pwd):
            good += 1
    return good


def main():
    regex = re.compile(r"^([0-9]*)-([0-9]*) ([a-z]): ([a-z]*)$")
    data = []
    with open(os.path.join("data", "day02.txt")) as f:
        for line in f:
            lower, upper, letter, pwd = regex.match(line).groups()
            lower, upper = int(lower), int(upper)
            data.append((lower, upper, letter, pwd))
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
