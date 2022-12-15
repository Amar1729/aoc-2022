#! /usr/bin/env python3

import collections
import sys

from aoc_tools import Point


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def parse_devices(data):
    d = {}
    for line in data:
        s_sensor, s_beacon = line.split(": ")
        s_coord = s_sensor.split(", y=")
        s_x = int(s_coord[0].split("x=")[1])
        s_y = int(s_coord[1])

        sensor = Point(s_x, s_y)

        b_coord = s_beacon.split(", y=")
        b_x = int(b_coord[0].split("x=")[1])

        beacon = Point(b_x, int(b_coord[1]))

        d[sensor] = beacon

    return d


def manhattan_range(s: Point, b: Point):
    distance = abs(s.x - b.x) + abs(s.y - b.y)

    for y in range(distance + 1):
        x = distance - y
        yield (s.x - x, s.x + x, s.y - y)
        yield (s.x - x, s.x + x, s.y + y)


class DisjointSet:
    def __init__(self):
        self.ranges = []

    def __add__(self, tup):
        self.update(*tup)
        d = DisjointSet()
        d.ranges = self.ranges
        return d

    def update(self, i: int, f: int):
        # somewhat gross impl, sorry
        c = 0
        while True:
            if c >= len(self.ranges):
                break

            # special case: join adjacent ranges?
            if i == self.ranges[c][1] + 1:
                p = self.ranges.pop(c)
                self.update(p[0], f)
                return
            elif f == self.ranges[c][0] - 1:
                p = self.ranges.pop(c)
                self.update(i, p[1])
                return

            if i > self.ranges[c][1]:
                # try next-highest pair
                c += 1
            elif i == self.ranges[c][1]:
                p = self.ranges.pop(c)
                self.update(p[0], f)
                return
            elif self.ranges[c][0] < i < self.ranges[c][1]:
                p = self.ranges.pop(c)
                self.update(p[0], max(f, p[1]))
                return
            elif self.ranges[c][0] <= f <= self.ranges[c][1]:
                p = self.ranges.pop(c)
                self.update(min(i, p[0]), max(f, p[1]))
                return
            elif f < self.ranges[c][0]:
                self.ranges.insert(c, (i, f))
                return
            elif i <= self.ranges[c][0] and f >= self.ranges[c][1]:
                self.ranges.pop(c)
                self.update(i, f)
            else:
                raise Exception

        self.ranges.append((i, f))

    def __repr__(self) -> str:
        # dbg
        return "\n".join([f"<{i}, {f}>" for i, f in self.ranges])

    def __str__(self) -> str:
        # dbg
        length = len(self.ranges)
        i = self.ranges[0][0]
        f = self.ranges[-1][1]
        return f"{length} splits: <{i}, {f}>"


def part1(data) -> int:
    sensors = set()
    beacons = set()

    # set of blocked points
    blocked = collections.defaultdict(DisjointSet)

    # sample data
    # target = 10
    target = 2_000_000

    for sensor, beacon in data.items():
        for xi, xf, y in manhattan_range(sensor, beacon):
            # look only at the points our problem wants?
            if y != target:
                continue

            blocked[y] += (xi, xf)

    # screw around a little bit
    actual_points = set()

    for i, f in blocked[target].ranges:
        for x in range(i, f + 1):
            p = Point(x, target)
            if p not in sensors and p not in beacons:
                actual_points.add(p)
    return len(actual_points)


def part2(data) -> int:
    # set of blocked points
    blocked = collections.defaultdict(DisjointSet)

    # sample data
    # m = 20
    m = 4_000_000

    for sensor, beacon in data.items():
        # will this help with efficiency during initial calc?
        for dev in (sensor, beacon):
            if dev.x in range(0, m + 1) and dev.y in range(0, m + 1):
                blocked[dev.y] += (dev.x, dev.x)

        for xi, xf, y in manhattan_range(sensor, beacon):
            # look only at the points our problem wants?

            if xi > m or xf < 0 or y not in range(0, m + 1):
                continue

            xi = max(0, xi)
            xf = min(xf, m)

            blocked[y] += (xi, xf)

    for y, ds in blocked.items():
        if len(ds.ranges) > 1:
            return y + (ds.ranges[0][1] + 1) * m

    # none found
    raise Exception


if __name__ == "__main__":
    data = parse(sys.argv[1])
    devices = parse_devices(data)

    # print(part1(devices))
    print(part2(devices))
