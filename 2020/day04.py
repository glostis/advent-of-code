import re
import os


def is_valid_passport1(passport):
    required_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    keys = set()
    for blob in passport.split():
        key, _ = blob.split(":")
        keys.add(key)
    return required_fields.intersection(keys) == required_fields


def part1(passports):
    valid_passports = 0
    for passport in passports:
        valid_passports += is_valid_passport1(passport)
    return valid_passports


def is_valid_passport2(passport):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    regex = re.compile(r"^#[0-9a-f]{6}")

    required_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    keys = set()
    for blob in passport.split():
        key, value = blob.split(":")
        keys.add(key)
        try:
            if key == "byr":
                assert 1920 <= int(value) <= 2002
            elif key == "iyr":
                assert 2010 <= int(value) <= 2020
            elif key == "eyr":
                assert 2020 <= int(value) <= 2030
            elif key == "hgt":
                number, unit = value[:-2], value[-2:]
                assert unit in ["cm", "in"]
                if unit == "cm":
                    assert 150 <= int(number) <= 193
                else:
                    assert 59 <= int(number) <= 76
            elif key == "hcl":
                assert regex.match(value) is not None
            elif key == "ecl":
                assert value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            elif key == "pid":
                try:
                    int(value)
                except ValueError:
                    return False
                assert len(value) == 9
        except AssertionError:
            return False
    return required_fields.intersection(keys) == required_fields


def part2(passports):
    valid_passports = 0
    for passport in passports:
        valid_passports += is_valid_passport2(passport)
    return valid_passports


def main():
    passports = [""]
    with open(os.path.join("data", "day04.txt")) as f:
        for line in f:
            line = line.strip()
            if line == "":
                passports[-1] = passports[-1][1:]  # Strip leading whitespace
                passports.append("")
            else:
                passports[-1] = f"{passports[-1]} {line}"
    print(part1(passports))
    print(part2(passports))


if __name__ == "__main__":
    main()
