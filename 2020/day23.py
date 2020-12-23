from collections import deque


def play_round(cups, length=9):
    current_cup = cups.popleft()
    next_cups = tuple(cups.popleft() for _ in range(3))

    destination_cup = ((current_cup - 1) - 1) % length + 1
    while destination_cup in next_cups:
        destination_cup = ((destination_cup - 1) - 1) % length + 1

    cups.appendleft(current_cup)

    insertion_point = cups.index(destination_cup) + 1
    for cup in reversed(next_cups):
        cups.insert(insertion_point, cup)

    cups.rotate(-1)
    return cups


def main():
    cups = deque(map(int, "123487596"))
    length = len(cups)
    for _ in range(100):
        play_round(cups, length)
    res = "".join(map(str, [cups[(cups.index(1) + 1 + i) % len(cups)] for i in range(8)]))
    print(int(res))


if __name__ == "__main__":
    main()
