#! /usr/bin/env python3

import sys


DIRECTIONS = {
    "R": 1 + 0j,
    "L": -1 + 0j,
    "U": 0 + -1j,
    "D": 0 + 1j,
}


# dbg
def pg(s):
    xs = [int(e.real) for e in s]
    ys = [int(e.imag) for e in s]

    shifted = set(map(lambda p: p - min(xs) - (min(ys) * 1j), s))

    for y in range(max(ys) + 1 - min(ys)):
        st = "".join([
            "#" if (x + y * 1j) in shifted else "."
            for x in range(max(xs) + 1 - min(xs))
        ])

        print(st)


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def calc_move(k1: complex, k2: complex) -> complex:
    """Given two knots, calculate the movement necessary for k2 to catch up"""
    sep = k1 - k2

    match int(sep.real), int(sep.imag):
        # head/tail are cardinal direction away
        case [0 as x, y] | [x, 0 as y]:
            if abs(y) == 2 or abs(x) == 2:
                return (x // 2) + (y // 2) * 1j

        # tail needs to move diagonally to catch up
        case [x, 2 as y] | [x, -2 as y] | [2 as x, y] | [-2 as x, y]:
            # 0, 1, -1
            cx = x if (x // 2) == 0 else (x // 2)
            cy = y if (y // 2) == 0 else (y // 2)

            return cx + cy * 1j

    # print("tail stays in same spot: ", sep)
    return 0


def part1(data) -> int:
    head = tail = 0 + 0j
    visited = set([tail])

    for line in data:
        action, d = line.split(" ")
        for _ in range(int(d)):
            head += DIRECTIONS[action]

            tail += calc_move(head, tail)
            visited.add(tail)

    return len(visited)


def part2(data) -> int:
    knots = [0 + 0j] * 10
    visited = set([knots[-1]])

    for line in data:
        action, d = line.split(" ")
        for _ in range(int(d)):
            knots[0] += DIRECTIONS[action]

            for i in range(9):
                knots[i + 1] += calc_move(knots[i], knots[i + 1])

            visited.add(knots[-1])

        print()
        pg(visited)

    return len(visited)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
