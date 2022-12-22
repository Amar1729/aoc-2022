#! /usr/bin/env python3

import re
import sys

from enum import Enum
from typing import NamedTuple

# see parent directory
# from aoc_tools import *


class Point(NamedTuple):
    """Commonly-used grid math

    Yes i know about complex(), but with that you have to do int() casts all over
    to use imag or real components as indices.
    """
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)


class D(Enum):
    L = Point(-1, 0)
    R = Point(+1, 0)
    U = Point(0, -1)
    D = Point(0, +1)


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line for line in f.read().splitlines()]

    # return the map and then the directions
    directions = [s.group() for s in re.finditer(r"(\d+)|([A-Z])", lines[-1])]
    return lines[:-2], directions


def turn(current: D, d: str) -> D:
    match (current.name, d):
        case ["L", "L"]:
            return D.D
        case ["D", "L"]:
            return D.R
        case ["R", "L"]:
            return D.U
        case ["U", "L"]:
            return D.L

        case ["L", "R"]:
            return D.U
        case ["U", "R"]:
            return D.R
        case ["R", "R"]:
            return D.D
        case ["D", "R"]:
            return D.L

    raise Exception


def part1(lines, directions) -> int:
    mapping = {}

    max_x = max(len(line) for line in lines)
    max_y = len(lines)

    # pad array???
    for idx in range(max_y):
        while len(lines[idx]) < max_x:
            lines[idx] += " "

    def find(p: Point, d: D) -> Point:
        curr = p
        while True:
            curr += d.value

            # loop around
            if curr.x < 0:
                curr = Point(max_x - 1, curr.y)
            elif curr.x >= max_x:
                curr = Point(0, curr.y)
            elif curr.y < 0:
                curr = Point(curr.x, max_y - 1)
            elif curr.y >= max_y:
                curr = Point(curr.x, 0)

            if lines[curr.y][curr.x] == "#":
                return p
            elif lines[curr.y][curr.x] == ".":
                return curr
            elif lines[curr.y][curr.x] == " ":
                pass

    curr = []
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c == ".":
                # first starting point
                if not curr:
                    curr.append((Point(x, y), D.R))
                for d in list(D):
                    p = Point(x, y)
                    mapping[(p, d)] = find(p, d)

    for gd in directions:
        if gd in ["L", "R"]:
            p, d = curr[0]
            curr[0] = (p, turn(d, gd))
        else:
            for _ in range(int(gd)):
                p, d = curr[0]
                curr[0] = (mapping[(p, d)], d)

    facing = {
        "R": 0,
        "D": 1,
        "L": 2,
        "U": 3,
    }

    p, d = curr[0]
    assert len(curr) == 1
    return sum([
        1000 * (p.y + 1),
        4 * (p.x + 1),
        facing[d.name]
    ])


def part2(lines, directions) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(*data))
    # print(part2(*data))
