import os


def part1(numbers):
    preamble = 25
    for i, number in enumerate(numbers[preamble:], start=preamble):
        number_is_ok = False
        previous = numbers[i - preamble : i]
        for j in range(preamble):
            for k in range(j + 1, preamble):
                if previous[j] != previous[k] and previous[j] + previous[k] == number:
                    number_is_ok = True
        if not number_is_ok:
            return number


def part2(numbers, target):
    n = len(numbers)
    for i in range(n):
        total = numbers[i]
        j = i + 1
        while j < n and total <= target:
            total += numbers[j]
            j += 1
        if total == target:
            nums = numbers[i : j + 1]
            return min(nums) + max(nums)


def main():
    with open(os.path.join("data", "day09.txt")) as f:
    # with open("samp.txt") as f:
        numbers = [int(line.strip()) for line in f]

    target = part1(numbers)
    print(target)
    print(part2(numbers, target))


if __name__ == "__main__":
    main()
