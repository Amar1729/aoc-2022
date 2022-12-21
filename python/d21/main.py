#! /usr/bin/env python3

import sys

import z3


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
    # lets do this with z3 cause i'm trying to learn to use it

    # NOTE! you want Optimize() here, NOT Solver()
    # does Solver() just return the first difference it finds, not best?
    # i don't actually know difference, but was getting wrong answer w/ Solver
    solver = z3.Optimize()

    monkeys = {}

    for monkey in data:
        name, op = monkey.split(": ")

        if name == "humn":
            continue
        elif name == "root":
            m1, _, m2 = op.split(" ")
            m1 = monkeys.setdefault(m1, z3.Int(m1))
            m2 = monkeys.setdefault(m2, z3.Int(m2))
            solver.add(m1 == m2)
            continue

        match (op.split(" ")):
            case [n]:
                m = monkeys.setdefault(name, z3.Int(name))
                solver.add(m == n)
            case [m1, "+", m2]:
                m = monkeys.setdefault(name, z3.Int(name))
                m1 = monkeys.setdefault(m1, z3.Int(m1))
                m2 = monkeys.setdefault(m2, z3.Int(m2))
                solver.add(m == (m1 + m2))
            case [m1, "-", m2]:
                m = monkeys.setdefault(name, z3.Int(name))
                m1 = monkeys.setdefault(m1, z3.Int(m1))
                m2 = monkeys.setdefault(m2, z3.Int(m2))
                solver.add(m == (m1 - m2))
            case [m1, "*", m2]:
                m = monkeys.setdefault(name, z3.Int(name))
                m1 = monkeys.setdefault(m1, z3.Int(m1))
                m2 = monkeys.setdefault(m2, z3.Int(m2))
                solver.add(m == (m1 * m2))
            case [m1, "/", m2]:
                m = monkeys.setdefault(name, z3.Int(name))
                m1 = monkeys.setdefault(m1, z3.Int(m1))
                m2 = monkeys.setdefault(m2, z3.Int(m2))
                solver.add(m2 != 0)
                solver.add(m == (m1 / m2))

    if solver.check() != z3.sat:
        raise Exception

    humn = monkeys["humn"]
    model = solver.model()
    return model[humn].as_long()


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
