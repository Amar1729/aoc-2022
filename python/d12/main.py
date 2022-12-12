#! /usr/bin/env python3

# commonly-used built-in imports. not all of these are necessarily used each day.
import string
import sys
from enum import Enum
from typing import NamedTuple, Tuple

from more_itertools import peekable


class Color(Enum):
    red = "\033[31m"  # ]
    noc = "\033[0m"  # ]


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


DIRECTIONS = [
    Point(0, 1),
    Point(0, -1),
    Point(1, 0),
    Point(-1, 0),
]


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def print_path(g, final_p, path):
    """ print out the path debugging """
    print(final_p)
    g = [list(row) for row in g]
    p = peekable(path)
    for point in p:
        try:
            d = p.peek() - point
            if d == DIRECTIONS[0]:
                c = "3"
            elif d == DIRECTIONS[1]:
                c = "^"
            elif d == DIRECTIONS[2]:
                c = ">"
            elif d == DIRECTIONS[3]:
                c = "<"
            else:
                raise Exception
        except StopIteration:
            c = "0"
        g[point.y][point.x] = c

    print(
        "\n".join(
            [
                "".join(
                    [
                        Color.red.value + c + Color.noc.value
                        if c not in string.ascii_letters
                        else c
                        for c in row
                    ]
                )
                for row in g
            ]
        )
    )


def bfs(start, g, visited) -> list[Point]:
    max_x = len(g[0])
    max_y = len(g)

    def bounds(p: Point) -> bool:
        if p.x in range(0, max_x):
            if p.y in range(0, max_y):
                return True
        return False

    # starting queue
    q: list[Tuple[Point, Point]] = [(start, start + p) for p in DIRECTIONS]

    while q:
        parent, newp = q.pop(0)

        if newp not in visited and bounds(newp):
            if ord(g[newp.y][newp.x]) - ord(g[parent.y][parent.x]) in range(-26, 2):
                q.extend([(newp, newp + p) for p in DIRECTIONS])
                visited[newp] = visited[parent] + [parent]

            elif g[parent.y][parent.x] == "S" and g[newp.y][newp.x] in ("a", "b"):
                q.extend([(newp, newp + p) for p in DIRECTIONS])
                visited[newp] = visited[parent] + [parent]

            elif g[newp.y][newp.x] == "E" and g[parent.y][parent.x] in ("y", "z"):
                # done!
                visited[newp] = visited[parent] + [parent]
                return visited[newp]

    # if we get here, we haven't found a valid path. debug!
    for item in sorted(visited.items(), key=lambda i: len(i[1])):
        print_path(g, *item)

    return []


def part1(data) -> int:
    start = None

    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == "S":
                start = Point(x, y)

    visited = {start: []}
    path = bfs(start, data, visited)
    return len(path)


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
