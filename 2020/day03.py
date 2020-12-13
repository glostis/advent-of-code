import os


def traverse_forest(forest, slope=(1, 3)):
    col, row = 0, 0
    forest_width = len(forest[0])
    trees = 0
    while row < len(forest):
        trees += forest[row][col] == "#"
        row += slope[0]
        col += slope[1]
        if col >= forest_width:
            col -= forest_width
    return trees


def main():
    with open(os.path.join("data", "day03.txt")) as f:
        forest = []
        for line in f:
            forest.append(line.strip())
    print(traverse_forest(forest))

    product = 1
    for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        trees = traverse_forest(forest, slope)
        product *= trees
    print(product)


if __name__ == "__main__":
    main()
