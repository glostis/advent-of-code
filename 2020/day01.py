import os


def part1(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            x, y = nums[i], nums[j]
            if x + y == 2020:
                return x * y


def part2(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = nums[i], nums[j], nums[k]
                if x + y + z == 2020:
                    return x * y * z


def main():
    with open(os.path.join("data", "day01.txt")) as f:
        nums = [int(line.strip()) for line in f]
        print(part1(nums))
        print(part2(nums))


if __name__ == "__main__":
    main()
