import os


def part1(range_min, range_max):
    count = 0
    for i in range(range_min, range_max + 1):
        if meets_criteria(i):
            count += 1
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


if __name__ == "__main__":
    print(part1(130254, 678275))
