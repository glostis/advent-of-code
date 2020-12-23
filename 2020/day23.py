from tqdm import tqdm


def play_round(cups, current_cup, length=9):
    next_cups = []
    for _ in range(3):
        next_cup = cups[current_cup]
        next_cups.append(next_cup)
        cups[current_cup] = cups.pop(next_cup)

    destination_cup = ((current_cup - 1) - 1) % length + 1
    while destination_cup in next_cups:
        destination_cup = ((destination_cup - 1) - 1) % length + 1

    for cup in reversed(next_cups):
        link = cups[destination_cup]
        cups[destination_cup] = cup
        cups[cup] = link

    return cups[current_cup]


def part1(cups, current_cup, length):
    for _ in range(100):
        current_cup = play_round(cups, current_cup=current_cup, length=length)

    pointer = 1
    res = ""
    for _ in range(8):
        res += str(cups[pointer])
        pointer = cups[pointer]
    return res


def part2(cups, current_cup, length):
    for _ in tqdm(range(10000000)):
        current_cup = play_round(cups, current_cup=current_cup, length=length)

    res = cups[1] * cups[cups[1]]
    return res


def main():
    l = list(map(int, "123487596"))
    current_cup = l[0]
    length = len(l)
    cups = dict()
    for i, c in enumerate(l):
        cups[c] = l[(i + 1) % length]
    print(part1(cups, current_cup, length))
    l.extend(range(10, 1000001))
    length = len(l)
    cups = dict()
    for i, c in enumerate(l):
        cups[c] = l[(i + 1) % length]
    print(part2(cups, current_cup, length))


if __name__ == "__main__":
    main()
