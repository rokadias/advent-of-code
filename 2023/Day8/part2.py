#!/usr/bin/env python

import re
import sys
import math
from operator import mul
from functools import reduce

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    nav_indexing = nav_flow(lines[0])
    lines = list(filter(lambda l: len(l.strip()) > 0, lines))
    nav_lookup = dict(map(parse_line, lines[1:]))
    index = 0
    ghost_nodes = list(filter(lambda k: k.endswith("A"), nav_lookup.keys()))
    first_index_counts = [None] * len(ghost_nodes)
    first_loop_index_counts = [None] * len(ghost_nodes)
    while len(list(filter(lambda i: i is None, first_loop_index_counts))) > 0 and index < 1000000000:
        index_to_use = nav_indexing[index % len(nav_indexing)]
        ghost_nodes = list(map(lambda n: nav_lookup[n][index_to_use], ghost_nodes))
        index += 1
        for i in range(len(ghost_nodes)):
            if first_index_counts[i] is None and ghost_nodes[i].endswith("Z"):
                first_index_counts[i] = index
            elif first_loop_index_counts[i] is None and ghost_nodes[i].endswith("Z"):
                first_loop_index_counts[i] = index

    print(f'first_index_counts: {first_index_counts}')
    print(f'first_loop_index_counts: {first_loop_index_counts}')
    print(f'list(map(lambda x: x * 2, first_index_counts)): {list(map(lambda x: x * 2, first_index_counts))}')
    iteration_counts = list(map(lambda idx: first_loop_index_counts[idx] - first_index_counts[idx], range(len(first_index_counts))))
    max_iterations = max(iteration_counts)
    max_iterations_index = next(filter(lambda idx: iteration_counts[idx] == max_iterations, range(len(first_index_counts))))

    multiplier = 0.0
    lcm = lcmm(*iteration_counts)
    print(f'lcm: {lcm}')

nav_map = {
    "L": 0,
    "R": 1,
}

def lcm(a: int, b: int) -> int:
    gcd = math.gcd(a, b)
    return abs(a * b) // gcd

def lcmm(*args):
    return reduce(lcm, args)

def nav_flow(line: str) -> list[int]:
    return list(map(lambda c: nav_map[c], line))

RE_NAV_ROW = r'([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)'

def parse_line(line: str) -> tuple[str, list[str]]:
    m = re.match(RE_NAV_ROW, line)
    return (m.group(1), [m.group(2), m.group(3)])
    

if __name__ == "__main__":
    main()
