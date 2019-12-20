# pylint: disable=redefined-outer-name
import os

from intcode import Intcode


def part1(program):
    tiles, _ = get_tiles(program)
    return len([el for el in tiles if el[2] == 2])


def part2(program):
    program[0] = 2
    _, score = get_tiles(program, play=True)
    return score


def sign(a):
    return 1 if a > 0 else -1 if a < 0 else 0


def get_tiles(program, play=False):
    count = 0
    outputs = []

    computer = Intcode(program)

    if play:
        joystick = 1
        ball_x = 0
        paddle_x = 0
    else:
        joystick = 0

    while True:
        computer.inputs = [joystick]
        computer.run_til_output()
        if computer.opcode == 99:
            break
        output = computer.outputs.pop()
        if play:
            if count == 2:
                if output == 4:
                    ball_x = outputs[-2]
                elif output == 3:
                    paddle_x = outputs[-2]
                joystick = sign(ball_x - paddle_x)
            count += 1
            count = count % 3
        outputs.append(output)

    tiles = []
    score = None
    for x, y, tile in zip(outputs[0::3], outputs[1::3], outputs[2::3]):
        if x == -1 and y == 0:
            score = tile
        else:
            tiles.append((x, y, tile))

    return tiles, score


if __name__ == "__main__":
    with open(os.path.join("data", "day13_1.txt")) as f:
        codes = [int(code) for code in f.read().split(",")]
        ret = part1(codes)
        assert ret == 258
        print("part1 day13 OK")
        ret = part2(codes)
        assert ret == 12765
        print("part2 day13 OK")
