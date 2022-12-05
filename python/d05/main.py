#! /usr/bin/env python3

import re
import collections
import functools
import itertools
import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.rstrip() for line in f.read().splitlines() if line.rstrip()]

    return lines


# assumes only up to 9 rows
# (because we use hard-coded indexes to get the crates in each column)
class Board:
    def __init__(self, content):
        # init will stop at the idx of the row line

        self.lines = []

        for idx, line in enumerate(content):
            if "[" not in line:  # ]
                self.row_idx = idx
                self.row = line
                break
            else:
                self.lines.append(line)

        self.crates = collections.defaultdict(list)
        for line in self.lines[::-1]:
            for col, letter in enumerate(line[1::4], start=1):
                if letter.strip():
                    self.crates[col].append(letter)

    def move(self, src, dst, amount):
        for _ in range(amount):
            self.crates[dst].append(self.crates[src].pop())

    def move2(self, src, dst, amount):
        to_move = self.crates[src][-amount:]
        self.crates[src] = self.crates[src][:-amount]
        self.crates[dst].extend(to_move)

    def top(self):
        return "".join([
            self.crates[i][-1]
            for i in sorted(self.crates.keys())
        ])


def part1(data, p2=False) -> str:
    board = Board(data)

    moves = []
    for line in data[board.row_idx + 1:]:
        moves.append(line)

        match = re.search(
            r"move (?P<amount>\d+) from (?P<src>\d+) to (?P<dst>\d+)", line
        )

        src = match.group("src")
        dst = match.group("dst")
        amount = match.group("amount")

        if p2:
            board.move2(int(src), int(dst), int(amount))
        else:
            board.move(int(src), int(dst), int(amount))

    return board.top()


def part2(data) -> str:
    return part1(data, True)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
