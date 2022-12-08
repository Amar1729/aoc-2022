#! /usr/bin/env python3

# commonly-used built-in imports. not all of these are necessarily used each day.
import collections
import functools
import sys

from typing import Dict, Tuple, Set, Union


DIRECTIONS = [
    0 + 1j,
    0 - 1j,
    1 + 0j,
    -1 + 0j,
]


COLORS = {
    "blue": "\033[34m",  # ]
    "yellow": "\033[33m",  # ]
    "green": "\033[32m",  # ]
    "red": "\033[31m",  # ]
    "noc": "\033[0m",  # ]
}


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def pgrid(g, visible):
    """ dbg: print out the graph """
    max_x = int(sorted(g, key=lambda e: int(e.real))[-1].real) + 1
    max_y = int(sorted(g, key=lambda e: int(e.imag))[-1].imag) + 1

    def col(c):
        return COLORS["blue"] + str(c) + COLORS["noc"]

    print("\n".join([
        str(y % 10) + " " + "".join([
            col(g[x + y * 1j]) if (x + y * 1j) in visible else str(g[x + y * 1j])
            for x in range(max_x)
        ])
        for y in range(max_y)
    ]))


def part1(data, part2=False) -> Union[int, Tuple[Dict, Set]]:
    """
    post-challenge note:
        i did this function this way because i was trying to come up with a
        more efficient way than going through and checking each point. this
        approach goes from the edges of the grid and iterates inward for each
        of the four directions, breaking once it encounters a tree of max
        height 9.

        however, i'm not convinced that the naive solution - just checking
        each tree in all four directions outward, and breaking when necessary -
        would have been too slow, given that's roughly what problem 2 ended
        up asking for.
    """
    visible = set()

    grid = {
        x + y * 1j: int(t)
        for y, row in enumerate(data)
        for x, t in enumerate(row)
    }

    max_x = len(data[0]) - 1
    max_y = len(data) - 1

    outside = set()
    for x in range(0, max_x + 1):
        outside.add(x + 0j)
        outside.add(x + max_y * 1j)

    for y in range(0, max_y + 1):
        outside.add(0 + y * 1j)
        outside.add(max_x + y * 1j)

    # top-down
    for x in range(1, max_x):
        y = 1

        p = x + y * 1j
        max_h = grid[p - 1j]
        while round(p.imag) < max_y and max_h < 9:
            if grid[p] > max_h:
                visible.add(p)
                max_h = grid[p]
            p += 1j

    # bottom-up
    for x in range(1, max_x):
        y = max_y - 1

        p = x + y * 1j
        max_h = grid[p + 1j]
        while round(p.imag) > 0 and max_h < 9:
            if grid[p] > max_h:
                visible.add(p)
                max_h = grid[p]
            p -= 1j

    # left-right
    for y in range(1, max_y):
        x = 1

        p = x + y * 1j
        max_h = grid[p - 1]
        while round(p.real) < max_x and max_h < 9:
            if grid[p] > max_h:
                visible.add(p)
                max_h = grid[p]
            p += 1

    # right-left
    for y in range(1, max_y):
        x = max_x - 1

        p = x + y * 1j
        max_h = grid[p + 1]
        while round(p.real) > 0 and max_h < 9:
            if grid[p] > max_h:
                visible.add(p)
                max_h = grid[p]
            p -= 1

    if part2:
        return grid, visible

    return len(outside) + len(visible)


def part2(data) -> int:
    ret = part1(data, True)
    assert not isinstance(ret, int)
    grid, visible = ret

    scenic_score = 0

    for p in visible:
        scenic = collections.defaultdict(int)
        for d in DIRECTIONS:
            curr_p = p + d
            while curr_p in grid:
                # print(p, curr_p, scenic[d], d)
                scenic[d] += 1
                if grid[p] <= grid[curr_p]:
                    break
                curr_p += d

        scenic_score = max(scenic_score, functools.reduce(lambda x, y: x * y, scenic.values(), 1))

    return scenic_score


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
