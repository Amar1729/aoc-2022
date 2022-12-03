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


def part1(data) -> int:
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


def part2(data) -> int:
    score = 0

    for line in data:
        opponent, player = line.split(" ")

        # need to lose
        if player == "X":
            score += 0

            # rock
            if opponent == "A":
                # scissors
                score += 3
            # paper
            elif opponent == "B":
                # rock
                score += 1
            # scissors
            elif opponent == "C":
                # paper
                score += 2

        # need to draw
        elif player == "Y":
            score += 3

            # rock
            if opponent == "A":
                # rock
                score += 1
            # paper
            elif opponent == "B":
                # paper
                score += 2
            # scissors
            elif opponent == "C":
                # scissors
                score += 3

        # need to win
        elif player == "Z":
            score += 6

            # rock
            if opponent == "A":
                # paper
                score += 2
            # paper
            elif opponent == "B":
                # scissors
                score += 3
            # scissors
            elif opponent == "C":
                # rock
                score += 1

    return score


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
