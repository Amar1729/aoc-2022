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
    # take the complement (i.e. negative space) of our shape
    # then flood-fill all the surrounding white space
    # so this _should_ leave us with only inner complement cubes

    points = set()

    for line in data:
        points.add(Point(*map(int, line.split(","))))

    # find outer bounds of droplets
    xp = sorted(p.x for p in points)
    xr = range(xp[0] - 1, xp[-1] + 2)

    yp = sorted(p.y for p in points)
    yr = range(yp[0] - 1, yp[-1] + 2)

    zp = sorted(p.z for p in points)
    zr = range(zp[0] - 1, zp[-1] + 2)

    # find negative space of our shape
    complement = set()
    for x in xr:
        for y in yr:
            for z in zr:
                p = Point(x, y, z)
                if p not in points:
                    complement.add(p)

    # flood-fill remove all points on the outside of our shape
    # so this flood-fill should NOT be able to reach any points inside
    # (this approach helps us avoid what i think could be gnarly bounds checking
    # for looking for "contained" cubes inside?)
    first_point = Point(xr[0], yr[0], zr[0])
    to_remove = set([first_point])
    while to_remove:
        tr = to_remove.pop()
        complement.remove(tr)

        for orth in ORTHOGONAL:
            if tr + orth in complement:
                to_remove.add(tr + orth)

    # count up the faces adjacent to negative space
    hidden = sum(
        sum(point + orth in points for orth in ORTHOGONAL)
        for point in complement
    )

    uncovered = sum(
        6 - sum(point + orth in points for orth in ORTHOGONAL)
        for point in points
    )

    return uncovered - hidden


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
