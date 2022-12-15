#! /usr/bin/env python3


from enum import Enum
from typing import NamedTuple


class Color(Enum):
    red = "\033[31m"  # ]
    noc = "\033[0m"  # ]


def colorize(s: str) -> str:
    """Colorize an input string"""
    return Color.red.value + s + Color.noc.value


class Point(NamedTuple):
    """Commonly-used grid math

    Yes i know about complex(), but with that you have to do int() casts all over
    to use imag or real components as indices.
    """
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)


ORTHOGONAL = [
    Point(+1, 0),
    Point(-1, 0),
    Point(0, +1),
    Point(0, -1),
]


DIAGONAL = [
    Point(-1, -1),
    Point(-1, +1),
    Point(+1, -1),
    Point(+1, +1),
]


def inclusive_range(m1, m2):
    """needs a range including both endpoints, possibly with unordered arguments"""
    yield from range(min(m1, m2), max(m1, m2) + 1)
