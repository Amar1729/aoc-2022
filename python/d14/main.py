#! /usr/bin/env python3

import sys

from more_itertools import pairwise


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def resting_point(s):
    # gets resting point of falling sand, or none
    curr = (500, 0)
    assert curr not in s

    max_y = max(p[1] for p in s)

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

        if curr[1] >= max_y:
            return None


def part1(data) -> int:
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
    while True:
        p = resting_point(points.union(sand))
        if p is None:
            break
        else:
            sand.add(p)

    return len(sand)


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
