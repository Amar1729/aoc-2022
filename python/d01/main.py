#! /usr/bin/env python3

import sys


def data(fname: str):
    with open(fname) as f:
        content = f.read()

    elves = [s.strip() for s in content.split("\n\n") if s.strip()]

    totals = [(idx, sum(map(int, e.split("\n")))) for idx, e in enumerate(elves, start=1)]

    return totals


def part1(f: str) -> int:
    totals = data(f)
    highest = max(totals, key=lambda t: t[1])
    return highest[1]


def part2(f: str) -> int:
    totals = sorted(data(f), key=lambda t: t[1])
    return sum(t[1] for t in totals[-3:])


if __name__ == "__main__":
    # print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))
