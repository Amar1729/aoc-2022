#! /usr/bin/env python3

import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def shuffle(d):
    for i in range(len(d)):
        idx, (_, step) = next(filter(lambda p: p[1][0] == i, enumerate(d)))
        while step != 0:
            if step > 0:
                d[idx], d[(idx + 1) % len(d)] = d[(idx + 1) % len(d)], d[idx]
                step -= 1
                idx = (idx + 1) % len(d)
            elif step < 0:
                d[idx], d[(idx - 1) % len(d)] = d[(idx - 1) % len(d)], d[idx]
                step += 1
                idx = (idx - 1) % len(d)

    return [(idx, step) for idx, (_, step) in enumerate(d)]


def part1(data) -> int:
    d = [(k, v) for k, v in enumerate(map(int, data))]

    d = shuffle(d)

    idx, _ = next(filter(lambda p: p[1][1] == 0, enumerate(d)))

    return sum(
        d[(idx + g) % len(d)][1]
        for g in range(1000, 3001, 1000)
    )


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
