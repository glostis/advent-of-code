import os


def part1(layout):
    layout = border_layout(layout)
    new_layout = apply_rules(layout, num_adj_to_empty=4, max_radius=1)
    while new_layout != layout:
        layout = new_layout
        new_layout = apply_rules(layout, num_adj_to_empty=4, max_radius=1)

    return sum([el == "#" for line in new_layout for el in line])


def part2(layout):
    layout = border_layout(layout)
    max_radius = max(len(layout), len(layout[0]))
    new_layout = apply_rules(layout, num_adj_to_empty=5, max_radius=max_radius)
    while new_layout != layout:
        layout = new_layout
        new_layout = apply_rules(layout, num_adj_to_empty=5, max_radius=max_radius)

    return sum([el == "#" for line in new_layout for el in line])


def border_layout(layout):
    width = len(layout[0])
    border = [" " for _ in range(width + 2)]
    new_layout = [border]
    for line in layout:
        new_layout.append([" "] + line + [" "])
    new_layout.append(border)
    return new_layout


def to_str(layout):
    return "".join("".join(char for line in layout for char in line))


def apply_rules(layout, num_adj_to_empty, max_radius):
    new_layout = []

    for row, line in enumerate(layout[1:-1]):
        new_layout_line = []
        for col, position in enumerate(line[1:-1]):
            if position == ".":
                new_layout_line.append(".")
            elif position in ["L", "#"]:
                radius = 1
                seen_directions = set()
                occupied = 0
                while (
                    len(seen_directions) < 8
                    and occupied < num_adj_to_empty
                    and radius <= max_radius
                ):
                    left = col - radius
                    right = col + radius
                    upper = row - radius
                    bottom = row + radius
                    mapping = {
                        "l": (row, left),
                        "r": (row, right),
                        "u": (upper, col),
                        "b": (bottom, col),
                        "ul": (upper, left),
                        "bl": (bottom, left),
                        "ur": (upper, right),
                        "br": (bottom, right),
                    }
                    for direction, coords in mapping.items():
                        if direction in seen_directions:
                            pass
                        else:
                            r, c = coords
                            r += 1
                            c += 1
                            p = layout[r][c]
                            if p == ".":
                                pass
                            elif p in [" ", "L"]:
                                seen_directions.add(direction)
                            elif p == "#":
                                occupied += 1
                                seen_directions.add(direction)
                            else:
                                raise
                    radius += 1
                if occupied >= num_adj_to_empty and position == "#":
                    new_layout_line.append("L")
                elif occupied == 0 and position == "L":
                    new_layout_line.append("#")
                else:
                    new_layout_line.append(position)

        new_layout.append(new_layout_line)

    return border_layout(new_layout)


def main():
    with open(os.path.join("data", "day11.txt")) as f:
        layout = [list(line.strip()) for line in f]

    print(part1(layout))
    print(part2(layout))


if __name__ == "__main__":
    main()
