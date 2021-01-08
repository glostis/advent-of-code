import math
import os
import re


def part2(tiles):
    image_tiles = order_adjust_tiles(tiles)
    image = []
    for tiles_ in image_tiles:
        for i in range(len(tiles_[0].tile_borderless)):
            line = "".join(tile.tile_borderless[i] for tile in tiles_)
            image.append(line)

    sea_monster = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
    sea_monster = [list(el) for el in sea_monster.split("\n")]

    nb_monsters = 0
    tile = Tile(1, image)
    nb_monsters += find_monsters(tile.tile, sea_monster)
    for _ in range(3):
        tile.rotate_anticlockwise()
        nb_monsters += find_monsters(tile.tile, sea_monster)
    tile.flip("vertical")
    nb_monsters += find_monsters(tile.tile, sea_monster)
    for _ in range(3):
        tile.rotate_anticlockwise()
        nb_monsters += find_monsters(tile.tile, sea_monster)

    sea_roughness = sum(char == "#" for line in image for char in line) - nb_monsters * sum(
        char == "#" for line in sea_monster for char in line
    )
    return sea_roughness


def find_monsters(image, sea_monster):
    nb_monsters = 0
    for c in range(len(image) - len(sea_monster[0])):
        for r in range(len(image) - len(sea_monster)):
            matches = True
            for i, line in enumerate(sea_monster):
                for j, char in enumerate(line):
                    if char == "#" and image[r + i][c + j] != char:
                        matches = False
            if matches:
                nb_monsters += 1
    return nb_monsters


def order_adjust_tiles(tiles):
    corner_tile = None
    for tile in tiles:
        matching_borders, _ = tile.get_matching_borders(tiles)
        if sum(matching_borders) == 2:
            corner_tile = tile
            break
    corner_tile.flip("horizontal")
    while corner_tile.get_matching_borders(tiles)[0] != [False, True, True, False]:
        corner_tile.rotate_anticlockwise()
    size = int(math.sqrt(len(tiles)))
    image = [[] for _ in range(size)]
    image[0].append(corner_tile)
    for i in range(size):
        for _ in range(size - 1):
            ref_tile = image[i][-1]
            border = ref_tile.right
            rev_border = "".join(reversed(border))
            for tile in tiles:
                if tile.id != ref_tile.id and (
                    border in tile.borders or rev_border in tile.borders
                ):
                    break
            tile.adjust(border, 3)
            image[i].append(tile)
        if i < size - 1:
            ref_tile = image[i][0]
            border = ref_tile.bottom
            rev_border = "".join(reversed(border))
            for tile in tiles:
                if tile.id != ref_tile.id and (
                    border in tile.borders or rev_border in tile.borders
                ):
                    break
            tile.adjust(border, 0)
            image[i + 1].append(tile)
    return image


class Tile:
    def __init__(self, _id, tile):
        self.id = _id
        self.tile = tile

    @property
    def tile_borderless(self):
        return [line[1:-1] for line in self.tile[1:-1]]

    @property
    def top(self):
        return self.tile[0]

    @property
    def right(self):
        return "".join(el[-1] for el in self.tile)

    @property
    def bottom(self):
        return self.tile[-1]

    @property
    def left(self):
        return "".join(el[0] for el in self.tile)

    @property
    def borders(self):
        return [self.top, self.right, self.bottom, self.left]

    def flip(self, direction):
        if direction == "vertical":
            new_tile = list(reversed(self.tile))
        if direction == "horizontal":
            new_tile = []
            for line in self.tile:
                new_tile.append("".join(reversed(line)))
        self.tile = new_tile

    def rotate_anticlockwise(self):
        size = len(self.tile)
        new_tile = [list(line) for line in self.tile]
        for i, line in enumerate(self.tile):
            for j, char in enumerate(line):
                new_tile[size - j - 1][i] = char
        new_tile = ["".join(line) for line in new_tile]
        self.tile = new_tile

    def get_matching_borders(self, tiles):
        all_borders = [border for tile in tiles for border in tile.borders]
        matching_borders = [False, False, False, False]
        matching_reversed = [False, False, False, False]
        for i, b in enumerate(self.borders):
            if all_borders.count(b) > 1 or all_borders.count("".join(reversed(b))) > 0:
                matching_borders[i] = True
                if not all_borders.count(b) > 1:
                    matching_reversed[i] = True
        return matching_borders, matching_reversed

    def adjust(self, border, position, verbose=False):
        matching = None
        for i, b in enumerate(self.borders):
            if b == border or "".join(reversed(b)) == border:
                matching = i
        number_quarter_turns = (matching - position) % 4
        if verbose:
            print(f"Rotating {number_quarter_turns} times")
        for _ in range(number_quarter_turns):
            self.rotate_anticlockwise()

        if "".join(reversed(self.borders[position])) == border:
            if position in [0, 2]:
                direction = "horizontal"
            else:
                direction = "vertical"
            if verbose:
                print(f"Flipping {direction}ly")
            self.flip(direction)

        assert self.borders[position] == border

    def __repr__(self):
        return f"Tile({self.id})"

    def __str__(self):
        string = ""
        for line in self.tile:
            string += line
            string += "\n"
        return string


def main():
    with open(os.path.join("data", "day20.txt")) as f:
    # with open("t.txt") as f:
        tiles = []
        tile_id = None
        tile = []
        for line in f:
            line = line.strip()
            if line == "":
                tiles.append(Tile(tile_id, tile))
                tile = []
                continue

            m = re.match(r"Tile (\d+):$", line)
            if m is not None:
                tile_id = int(m.group(1))
            else:
                tile.append(line)
    # return tiles
    return part2(tiles)


if __name__ == "__main__":
    main()
