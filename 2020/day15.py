def play_game(numbers, limit):
    mem = dict()
    for turn, number in enumerate(numbers, 1):
        mem[number] = [turn]

    while turn < limit:
        turn += 1
        previously_spoken = list(mem.get(number, []))
        if len(previously_spoken) < 2:
            number = 0
        else:
            last_last_spoken, last_spoken = previously_spoken[-2:]
            number = last_spoken - last_last_spoken

        if number in mem:
            m = mem[number][-2:]
            m.append(turn)
            mem[number] = m
        else:
            mem[number] = [turn]
    return number


def main():
    numbers = [7, 12, 1, 0, 16, 2]
    print(play_game(numbers, 2020))
    print(play_game(numbers, 30000000))


if __name__ == "__main__":
    main()
