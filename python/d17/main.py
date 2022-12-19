#! /usr/bin/env python3

import copy
import sys

from typing import List, Set

# store shapes as list of indexes of their blocks
# note these are in reverse order
SHAPES = [
    [
        [0, 1, 2, 3],
    ],
    [
        [1],
        [0, 1, 2],
        [1],
    ],
    [
        [0, 1, 2],
        [2],
        [2],
    ],
    [
        [0],
        [0],
        [0],
        [0],
    ],
    [
        [0, 1],
        [0, 1],
    ],
]


def print_state(tower: List[Set[int]], height: int, shape: List[List[int]]):
    rows = [
        "+" + 7 * "-" + "+",
    ]

    max_h = max(len(tower), height + len(shape))

    for h in range(max_h):
        row = ["|"] + ["."] * 7 + ["|"]
        for c in range(7):
            if h < len(tower) and c in tower[h]:
                row[c + 1] = "#"
            elif (h - height in range(len(shape))) and c in shape[h - height]:
                row[c + 1] = "@"

        rows.insert(0, "".join(row))

    print("\n".join(rows))


def move(shape: List[List[int]], x: int, bounds: List[Set[int]]) -> bool:
    """move with a bounds check"""

    # include walls in bounds check
    while len(bounds) < len(shape):
        bounds.append(set([]))
    for b in range(len(bounds)):
        bounds[b] |= set([-1, 7])

    for row, bslice in zip(shape, bounds):
        for col in row:
            if col + x in bslice:
                return False

    for row_idx in range(len(shape)):
        for c_idx in range(len(shape[row_idx])):
            shape[row_idx][c_idx] += x

    # moved
    return True


def check_below(shape: List[List[int]], tower_slice: List[Set[int]]) -> bool:
    """check if below rows of the tower have a possible collision"""
    for shape_row, tower_row in zip(shape, tower_slice):
        if any(sc in tower_row for sc in shape_row):
            # can't fall one block
            return False

    # able to fall one block
    return True


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data, p2: bool = False) -> int:
    jetstream = list(data[0])
    jet_idx = 0

    tower = []

    # stupid part 2 elephants
    max_h = 2022 if not p2 else 1_000_000_000_000

    for block in range(max_h):
        # height of the falling block
        height = len(tower) + 3
        shape = copy.deepcopy(SHAPES[block % 5])

        # move entire shape to the right twice
        move(shape, 2, [])

        while True:
            jet = 1 if jetstream[jet_idx % len(jetstream)] == ">" else -1
            jet_idx += 1

            move(shape, jet, tower[height:height + len(shape)])

            if height > 0 and check_below(shape, tower[height - 1:height + len(shape)]):
                height -= 1
            else:
                while len(tower) < height + len(shape):
                    tower.append(set())
                for row_idx in range(len(shape)):
                    tower[height + row_idx] |= set(shape[row_idx])

                # done falling, go to next block
                break

    return len(tower)


def part2(data) -> int:
    return part1(data, True)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
