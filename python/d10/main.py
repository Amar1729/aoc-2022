#! /usr/bin/env python3

import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    # now that we know what register represents from pt2, we know it can't be 0
    wanted = {c: 0 for c in range(20, 221, 40)}

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

        for k in sorted(wanted.keys()):
            if wanted[k] == 0:
                if cycle == k:
                    wanted[k] = x
                elif cycle == k + 1:
                    wanted[k] = x - prev
                break

    return sum(k * v for k, v in wanted.items())


def part2(data):
    x = 1
    row = []

    # gross
    def render():
        print("".join(row))
        for _ in range(len(row)):
            row.pop(0)

    # gross
    def draw():
        if len(row) == 40:
            render()

        # protip use " " instead of ".", makes reading the output slightly easier
        c = "#" if abs(x - len(row)) <= 1 else " "
        row.append(c)

    for line in data:

        match line.split(" "):
            case ["noop"]:
                draw()
            case ["addx", d]:
                draw()
                draw()

                x += int(d)

    # print out last row if there's anything left
    if row:
        render()


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    part2(data)
