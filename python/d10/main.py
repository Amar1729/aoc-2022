#! /usr/bin/env python3

import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    wanted = {c: None for c in range(20, 221, 40)}

    x = 1
    cycle = 1
    for line in data:
        prev = 0
        match line.split(" "):
            case ["noop"]:
                cycle += 1
            case ["addx", d]:
                cycle += 2
                prev = int(d)
                x += int(d)

        # print(line, cycle, x)

        if cycle > 180:
            print(line, cycle, x, prev)

        for k in sorted(wanted.keys()):
            if wanted[k] is None:
                if cycle == k:
                    wanted[k] = x
                elif cycle == k + 1:
                    wanted[k] = x - prev
                break

    return sum(k * v for k, v in wanted.items())


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
