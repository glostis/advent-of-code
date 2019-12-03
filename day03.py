import os


def part1(lines):
    wire_1 = lines[0].split(",")
    wire_2 = lines[1].split(",")
    path_1 = make_path(wire_1)
    path_2 = make_path(wire_2)
    intersections = path_1.intersection(path_2)
    distances = [abs(x) + abs(y) for (x, y) in intersections]
    return min(distances)


def make_path(commands):
    path = set()
    x, y = 0, 0
    for command in commands:
        direction = command[0]
        number = int(command[1:])
        assert direction in ["U", "L", "R", "D"]
        sign = +1 if direction in ["U", "R"] else -1
        for _ in range(number):
            if direction in ["L", "R"]:
                x += sign
            else:
                y += sign
            path.add((x, y))
    return path


if __name__ == "__main__":
    with open(os.path.join("data", "day03_1.txt")) as f:
        lines = [line.strip() for line in f]
        print(part1(lines))
