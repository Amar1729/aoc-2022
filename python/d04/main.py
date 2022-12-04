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

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
