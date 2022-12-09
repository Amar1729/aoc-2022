#! /usr/bin/env python3

import sys


DIRECTIONS = {
    "R": 1 + 0j,
    "L": -1 + 0j,
    "U": 0 + -1j,
    "D": 0 + 1j,
}


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    head = tail = 0 + 0j
    visited = set([tail])

    for line in data:
        action, d = line.split(" ")
        for _ in range(int(d)):
            head += DIRECTIONS[action]

            sep = head - tail

            match int(sep.real), int(sep.imag):
                # head/tail are cardinal direction away
                case [0 as x, y] | [x, 0 as y]:
                    if abs(y) == 2 or abs(x) == 2:
                        tail += DIRECTIONS[action]

                # tail needs to move diagonally to catch up
                case [x, 2 as y] | [x, -2 as y]:
                    tail += x + (y // 2) * 1j
                case [2 as x, y] | [-2 as x, y]:
                    tail += (x // 2) + y * 1j

                case _:
                    # print("tail stays in same spot: ", sep)
                    pass

            visited.add(tail)

    return len(visited)


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
