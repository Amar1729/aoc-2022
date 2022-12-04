#! /usr/bin/env python3

import collections
import functools
import itertools
import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    total = 0

    for line in data:
        parts = line.split(",")

        e1_range = set(range(
            int(parts[0].split("-")[0]),
            int(parts[0].split("-")[1]) + 1
        ))

        e2_range = set(range(
            int(parts[1].split("-")[0]),
            int(parts[1].split("-")[1]) + 1
        ))

        total += bool(e1_range.issubset(e2_range)) or e2_range.issubset(e1_range)

    return total


def part2(data) -> int:
    total = 0

    for line in data:
        parts = line.split(",")

        # my solution in p1 was a bit gross cause i was going fast, but
        # this is a bit cleaner
        def some_range(p):
            begin, end = map(int, p.split("-"))
            return set(range(begin, end+1))

        e1_range, e2_range = map(some_range, parts)

        total += len(e1_range.intersection(e2_range)) > 0

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
