#! /usr/bin/env python3

# commonly-used built-in imports. not all of these are necessarily used each day.
import collections
import functools
import itertools
import re
import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data, length=4) -> int:
    buf = list(data[0][:length-1])
    for idx, c in enumerate(data[0][length-1:], start=length):
        if len(set(buf + [c])) == length:
            return idx
        else:
            buf.pop(0)
            buf.append(c)

    return 0


def part2(data) -> int:
    return part1(data, 14)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
