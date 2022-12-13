#! /usr/bin/env python3

# commonly-used built-in imports. not all of these are necessarily used each day.
import itertools
import sys
from ast import literal_eval
from typing import Iterable, Optional, Union

from more_itertools import chunked


# recursive type
RecList = Union[int, Iterable["RecList"]]


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def compare_parts(lhs: RecList, rhs: RecList) -> Optional[bool]:
    # each case will shadow lhs/rhs (`as lhs`) for type-checker sanity
    match lhs, rhs:
        case (int() as lhs, int() as rhs):
            if lhs < rhs:
                return True
            elif lhs == rhs:
                # if these are the same, fall back to checking next element in the list
                return None
            else:
                return False

        case (list() as lhs, int() as rhs):
            return compare_parts(lhs, [rhs])

        case (int() as lhs, list() as rhs):
            return compare_parts([lhs], rhs)

        case (list() as lhs, list() as rhs):
            for l, r in itertools.zip_longest(lhs, rhs):
                if l is None:
                    return True

                elif r is None:
                    return False

                ret = compare_parts(l, r)
                if ret is None:
                    # continue to check next elem
                    pass
                else:
                    return ret

            return None

    raise Exception


def part1(data) -> int:
    # lol because i can
    return sum(
        map(
            lambda p: p[0],
            filter(
                lambda p: p[1],
                (
                    (index, compare_parts(*map(literal_eval, packets)))
                    for index, packets in enumerate(chunked(data, 2), start=1)
                ),
            ),
        )
    )


def part2(data) -> int:
    # ... am i actually going to bubble sort???
    packets = [literal_eval(data[0])]

    for packet in map(lambda d: literal_eval(d), data[1:] + ["[[2]]"] + ["[[6]]"]):
        for idx in range(len(packets)):
            if compare_parts(packet, packets[idx]):
                packets.insert(idx, packet)
                break
        else:
            # runs if loop wasn't broken
            packets.append(packet)

    return (1 + packets.index([[2]])) * (1 + packets.index([[6]]))


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
