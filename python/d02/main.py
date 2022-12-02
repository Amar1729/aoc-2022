#! /usr/bin/env python3

import collections
import functools
import itertools
import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def day1(data) -> int:
    score = 0

    for line in data:
        opponent, player = line.split(" ")

        # rock
        if player == "X":
            score += 1

            # rock
            if opponent == "A":
                # draw
                score += 3
            # paper
            elif opponent == "B":
                # loss
                score += 0
            # scissors
            elif opponent == "C":
                # win
                score += 6

        # paper
        elif player == "Y":
            score += 2

            # rock
            if opponent == "A":
                # win
                score += 6
            # paper
            elif opponent == "B":
                # draw
                score += 3
            # scissors
            elif opponent == "C":
                # loss
                score += 0

        # scissors
        elif player == "Z":
            score += 3

            # rock
            if opponent == "A":
                # loss
                score += 0
            # paper
            elif opponent == "B":
                # win
                score += 6
            # scissors
            elif opponent == "C":
                # draw
                score += 3

    return score


def day2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(day1(data))
    print(day2(data))
