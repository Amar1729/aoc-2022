#! /usr/bin/env python3

import collections
import sys

from enum import Enum
from typing import NamedTuple
# from pprint import pprint


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)


class D(Enum):
    W = Point(-1, 0)
    E = Point(+1, 0)
    N = Point(0, -1)
    S = Point(0, +1)
    NW = Point(-1, -1)
    SW = Point(-1, +1)
    NE = Point(+1, -1)
    SE = Point(+1, +1)


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def print_grid(grid, dbg=True) -> int:
    # pprint(grid)
    min_x = min([p.x for p in grid])
    max_x = max([p.x for p in grid])
    min_y = min([p.y for p in grid])
    max_y = max([p.y for p in grid])

    empty = 0
    for y in range(min_y, max_y + 1):
        st = ""
        for x in range(min_x, max_x + 1):
            if Point(x, y) in grid:
                st += "#"
            else:
                st += "."
                empty += 1

        if dbg:
            print(st)

    return empty


def part1(data, p2=False) -> int:
    grid = set([
        Point(x, y)
        for y, row in enumerate(data)
        for x, c in enumerate(row)
        if c == "#"
    ])

    # print_grid(grid)

    directions = list({
        D.N: (D.N, D.NE, D.NW),
        D.S: (D.S, D.SE, D.SW),
        D.W: (D.W, D.NW, D.SW),
        D.E: (D.E, D.NE, D.SE),
    }.items())

    # first half: make decisions
    step = 1
    while True:
        # print("==== " * 4 + f"STEP {step}" + " ====" * 4)
        # print_grid(grid)

        new_points = set()

        # hold the new position and all old elf positions
        previous = collections.defaultdict(list)

        for p in grid:
            check = lambda d: p + d.value in grid
            cond = lambda i: all(not check(_d) for _d in directions[i][1])

            if all(p + d.value not in grid for d in list(D)):
                previous[p].append(p)

            elif cond(0):
                previous[p + directions[0][0].value].append(p)

            elif cond(1):
                previous[p + directions[1][0].value].append(p)

            elif cond(2):
                previous[p + directions[2][0].value].append(p)

            elif cond(3):
                previous[p + directions[3][0].value].append(p)

            else:
                # fallback: don't move
                previous[p].append(p)

        if all(k == v[0] for k, v in previous.items()):
            if p2:
                return step
            else:
                break

        for new_p, old_ps in previous.items():
            if len(old_ps) == 1:
                # print("succesfully moved", new_p, new_p - old_ps[0])
                assert new_p not in new_points
                new_points.add(new_p)
            else:
                # print("number of elves who would have moved:", len(old_ps))
                # print(new_p, old_ps)
                for x in old_ps:
                    assert x not in new_points
                    new_points.add(x)

        assert len(new_points) == len(grid)

        # rotate directions
        directions.append(directions.pop(0))
        # everybody moves
        grid = new_points

        step += 1

    # need number of empty ground tiles
    return print_grid(grid, False)


def part2(data) -> int:
    return part1(data, True)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
