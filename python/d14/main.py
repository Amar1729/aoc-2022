#! /usr/bin/env python3

import sys

from more_itertools import pairwise


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def resting_point(s, max_y: int, p2=False):
    # gets resting point of falling sand, or none
    curr = (500, 0)
    assert curr not in s

    while True:
        if (curr[0], curr[1] + 1) not in s:
            curr = (curr[0], curr[1] + 1)
        elif (curr[0] - 1, curr[1] + 1) not in s:
            curr = curr[0] - 1, curr[1] + 1
        elif (curr[0] + 1, curr[1] + 1) not in s:
            curr = curr[0] + 1, curr[1] + 1
        else:
            # reached resting point
            return curr

        if p2 and curr[1] == max_y - 1:
            # this is the greatest possible for part2
            return curr

        if curr[1] >= max_y:
            assert not p2
            return None


def part1(data, p2=False) -> int:
    points = set()

    for line in data:
        coords = line.split(" -> ")
        for start, end in pairwise(coords):
            xi, yi = map(int, start.split(","))
            xf, yf = map(int, end.split(","))

            if xi == xf:
                for y in range(min(yi, yf), max(yi, yf) + 1):
                    points.add((xi, y))
            elif yi == yf:
                for x in range(min(xi, xf), max(xi, xf) + 1):
                    points.add((x, yi))

            else:
                raise Exception("diagonal line")

    # simulate falling sand
    # sand falls from 500, 0
    sand = set()
    max_y = max(p[1] for p in points)
    if p2:
        max_y += 2

    while True:
        p = resting_point(points.union(sand), max_y, p2)
        if p is None:
            break
        else:
            sand.add(p)

        # last particle of sand to fall
        if p2 and p == (500, 0):
            return len(sand)

    return len(sand)


def part2(data) -> int:
    return part1(data, True)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
