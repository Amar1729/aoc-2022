#! /usr/bin/env python3

import string

import collections
import functools
import itertools
import sys


PRIORITIES = {
    c: idx
    for idx, c in itertools.chain(
        enumerate(string.ascii_lowercase, start=1), enumerate(string.ascii_uppercase, start=27)
    )
}


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def day1(data) -> int:
    total = 0

    for rucksack in data:
        size = int(len(rucksack) / 2)
        compartments = rucksack[:size], rucksack[size:]

        common = set(compartments[0]).intersection(set(compartments[1]))
        total += PRIORITIES[common.pop()]

    # todo

    return total


def day2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(day1(data))
    # print(day2(data))
