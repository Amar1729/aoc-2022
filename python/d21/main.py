#! /usr/bin/env python3

import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    monkeys = {}

    # recursive on monkeys
    def get_monkey(name) -> int:
        return monkeys[name]()

    def l_flat(o: int):
        return lambda: o

    def l_mult(m1, op, m2):
        match op:
            case "+":
                return lambda: get_monkey(m1) + get_monkey(m2)
            case "-":
                return lambda: get_monkey(m1) - get_monkey(m2)
            case "*":
                return lambda: get_monkey(m1) * get_monkey(m2)
            case "/":
                return lambda: get_monkey(m1) // get_monkey(m2)

    for monkey in data:
        name, op = monkey.split(": ")

        try:
            op = int(op)
            monkeys[name] = l_flat(op)
        except ValueError:
            monkeys[name] = l_mult(*op.split(" "))

    return get_monkey("root")


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
