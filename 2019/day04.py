import re


def part1(range_min, range_max):
    count = 0
    for i in range(range_min, range_max + 1):
        if meets_criteria(i):
            count += 1
    return count


def part2(range_min, range_max):
    count = 0
    for i in range(range_min, range_max + 1):
        if meets_criteria(i):
            if meets_new_criteria(i):
                count += 1
            else:
                # print(i)
                pass
    return count


def meets_criteria(number):
    answer = True
    # 6-digit number
    if len(str(number)) != 6:
        answer = False

    # Digits never decrease
    diffs = [int(j) - int(i) for (i, j) in zip(str(number), str(number)[1:])]
    if sum([i for i in diffs if i < 0]) < 0:
        answer = False

    # Two adjacent digits are the same
    if len([i for i in diffs if i == 0]) == 0:
        answer = False

    return answer


def meets_new_criteria(number):
    number = str(number)
    for i in range(0, 10):
        if (
            re.match(fr"^{i}{i}[^{i}].*", number)
            or re.match(fr".*[^{i}]{i}{i}$", number)
            or re.match(fr".*[^{i}]{i}{i}[^{i}].*", number)
        ):
            return True
    return False


if __name__ == "__main__":
    print(part1(130254, 678275))
    print(part2(130254, 678275))
