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
        lines = [line.rstrip() for line in f.read().splitlines() if line.rstrip()]

    return lines


class Node:
    def __init__(self, name, size: int = 0) -> None:
        self.name = name
        # self.parent = parent  # ?
        self.children = []
        self._size = size

    def size(self) -> int:
        if self._size == 0 and self.children:
            self._size = sum(c.size() for c in self.children)
        return self._size

    def nodes_lt(self, limit):
        if not self.children:
            return

        if self.size() <= limit:
            yield self.size()

        for c in self.children:
            yield from c.nodes_lt(limit)

    def __str__(self, depth=0):
        return "".join([
            "  " * depth,
            f"{self.name} (size={self.size()})",
            "\n" if self.children else "",
            "\n".join([c.__str__(depth+2) for c in self.children])
        ])


def parse_lines(data):
    tree = Node("/")
    curdir = []

    for line in data:
        match line.split(" "):
            case ["$", "cd", ".."]:
                curdir.pop()

            case ["$", "cd", target]:
                curdir.append(target)

            case ["$", "ls"]:
                # return "ls", ""
                pass

            case [x, fname]:
                cur = tree
                for d in curdir[1:]:
                    target = next(filter(lambda n: n.name == d, cur.children))
                    cur = target

                if x == "dir":
                    cur.children.append(Node(fname, 0))
                else:
                    cur.children.append(Node(fname, int(x)))

            case _:
                raise Exception(line)

    return tree


def part1(data, limit=100_000) -> int:
    root = parse_lines(data)
    # print(root)
    return sum(root.nodes_lt(limit))


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
