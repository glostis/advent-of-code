import os


def part1(answers):
    count = 0
    for a in answers:
        count += len(set("".join(a)))
    return count


def part2(answers):
    count = 0
    for a in answers:
        s = set(a[0])
        for p in a:
            s = s.intersection(set(p))
        count += len(s)
    return count


def main():
    with open(os.path.join("data", "day06.txt")) as f:
        answers = [line.split("\n") for line in f.read().split("\n\n")]

    # Due to the line.split("\n"), the final element of answers looks like ["a", "b", ""]
    # so we remove that
    answers[-1] = answers[-1][:-1]

    print(part1(answers))
    print(part2(answers))


if __name__ == "__main__":
    main()
