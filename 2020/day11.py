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
    return "\n".join(["".join(char for char in line) for line in layout])


def contaminate_neighbors(row, col, layout, occupied_neighbors, max_radius):
    radius = 1
    seen_directions = set()
    while len(seen_directions) < 8 and radius <= max_radius:
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
            if direction not in seen_directions:
                r, c = coords
                p = layout[r + 1][c + 1]
                if p in [" ", "L", "#"]:
                    seen_directions.add(direction)
                    if p != " ":
                        occupied_neighbors[r][c] += 1
        radius += 1


def apply_rules(layout, num_adj_to_empty, max_radius):
    occupied_neighbors = [[0 for _ in range(len(layout[0]) - 2)] for _ in range(len(layout) - 2)]
    new_layout = [[char for char in line] for line in layout]

    for row, line in enumerate(layout[1:-1]):
        for col, position in enumerate(line[1:-1]):
            if position == "#":
                contaminate_neighbors(row, col, layout, occupied_neighbors, max_radius)

    for row, line in enumerate(layout[1:-1]):
        for col, position in enumerate(line[1:-1]):
            if position == "#" and occupied_neighbors[row][col] >= num_adj_to_empty:
                new_layout[row + 1][col + 1] = "L"
            elif position == "L" and occupied_neighbors[row][col] == 0:
                new_layout[row + 1][col + 1] = "#"

    return new_layout


def main():
    with open(os.path.join("data", "day11.txt")) as f:
        layout = [list(line.strip()) for line in f]

    print(part1(layout))
    print(part2(layout))


if __name__ == "__main__":
    main()
