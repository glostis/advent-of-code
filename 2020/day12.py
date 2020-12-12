import math
import os
import re


def part1(inst):
    orientation = 90
    lon, lat = 0, 0

    dir_orient = {0: "N", 90: "E", 180: "S", 270: "W"}
    for action, value in inst:
        if action == "F":
            action = dir_orient[orientation % 360]

        if action == "L":
            orientation -= value
        elif action == "R":
            orientation += value
        elif action == "N":
            lat += value
        elif action == "S":
            lat -= value
        elif action == "W":
            lon -= value
        elif action == "E":
            lon += value
    return abs(lon) + abs(lat)


def part2(inst):
    s_lon, s_lat = 0, 0
    w_d_lon, w_d_lat = 10, 1

    for action, value in inst:
        if action == "F":
            s_lon += w_d_lon * value
            s_lat += w_d_lat * value

        if action in ["L", "R"]:
            if value == 180:
                w_d_lon, w_d_lat = -w_d_lon, -w_d_lat
            elif (value == 90 and action == "L") or (value == 270 and action == "R"):
                old_lon, old_lat = w_d_lon, w_d_lat
                w_d_lon, w_d_lat = -old_lat, old_lon
            elif (value == 270 and action == "L") or (value == 90 and action == "R"):
                old_lon, old_lat = w_d_lon, w_d_lat
                w_d_lon, w_d_lat = old_lat, -old_lon
            else:
                raise
        elif action == "N":
            w_d_lat += value
        elif action == "S":
            w_d_lat -= value
        elif action == "W":
            w_d_lon -= value
        elif action == "E":
            w_d_lon += value
    return abs(s_lon) + abs(s_lat)


def main():
    regex = re.compile(r"([NSEWLRF])(\d+)")
    with open(os.path.join("data", "day12.txt")) as f:
        inst = [regex.match(line).groups() for line in f]

    inst = [(action, int(value)) for action, value in inst]

    print(part1(inst))
    print(part2(inst))


if __name__ == "__main__":
    main()
