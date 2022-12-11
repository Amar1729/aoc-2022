#! /usr/bin/env python3

# commonly-used built-in imports. not all of these are necessarily used each day.
import re
import sys

from math import prod
from typing import Callable
from dataclasses import dataclass

from more_itertools import chunked


@dataclass
class Monkey:
    index: int
    items: list[int]
    op: Callable[[int], int]
    test: Callable[[int], bool]
    target_true: int
    target_false: int

    inspection_count: int

    # part2: time to get schwifty with number theory
    divisor: int = 0


def parse_monke(lines: list[str]) -> Monkey:

    m = re.match(r"Monkey (?P<index>(\d+))", lines[0])
    assert m is not None  # for type-checking
    index = int(m.group("index"))

    m = re.search(r"Starting items: (?P<items>(.*))", lines[1])
    assert m is not None  # for type-checking
    items = list(map(int, m.group("items").split(", ")))

    m = re.search(r"Operation: new = (?P<op>(.*))", lines[2])
    assert m is not None  # for type-checking
    op = m.group("op")
    operation = lambda old: eval(op)

    # assumes all are "divisible by " ?
    m = re.search(r"Test: divisible by (?P<div>(\d+))", lines[3])
    assert m is not None  # for type-checking
    div = int(m.group("div"))
    test = lambda x: x % div == 0

    m = re.search(r"If true: throw to monkey (?P<monkey>(\d+))", lines[4])
    assert m is not None  # for type-checking
    target_true = int(m.group("monkey"))

    m = re.search(r"If false: throw to monkey (?P<monkey>(\d+))", lines[5])
    assert m is not None  # for type-checking
    target_false = int(m.group("monkey"))

    return Monkey(
        index,
        items,
        operation,
        test,
        target_true,
        target_false,
        0,
        div,
    )


def parse(fname: str) -> list[Monkey]:
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return list(map(parse_monke, chunked(lines, 6)))


def part1(monkeys, rounds=20) -> int:
    # optimization!
    # notice that all the divisors are prime numbers

    # so what we do is mult all the divisors from the monkeys
    # and use that as a supermodulo for each operation done to an item
    # that way, the item values won't ever go past this product
    supermodulo = prod(m.divisor for m in monkeys)

    for _ in range(rounds):
        # do a round

        for m in monkeys:
            # do a monkey's turn

            for _ in range(len(m.items)):
                item = m.items.pop(0)

                # monkey inspects
                item = m.op(item)

                if rounds == 20:
                    # part1
                    # i'm relieved
                    item = item // 3
                else:
                    # part2
                    # i'm not relieved
                    pass

                item %= supermodulo

                # monkey tests and throws
                if m.test(item):
                    monkeys[m.target_true].items.append(item)
                else:
                    monkeys[m.target_false].items.append(item)

                m.inspection_count += 1

    # return product of two highest monkey's inspection_counts
    sm = sorted(monkeys, key=lambda m: m.inspection_count)
    return sm[-2].inspection_count * sm[-1].inspection_count


def part2(monkeys) -> int:
    return part1(monkeys, 10_000)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
