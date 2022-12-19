#! /usr/bin/env python3

import sys

from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)


ORTHOGONAL = [
    Point(-1, 0, 0),
    Point(+1, 0, 0),
    Point(0, -1, 0),
    Point(0, +1, 0),
    Point(0, 0, -1),
    Point(0, 0, +1),
]


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    points = set()

    for line in data:
        points.add(Point(*map(int, line.split(","))))

    uncovered = 0
    for point in points:
        uncovered += 6 - sum(point + orth in points for orth in ORTHOGONAL)

    return uncovered


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
