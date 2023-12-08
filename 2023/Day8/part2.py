#!/usr/bin/env python

import re
import sys

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
    index_counts = [None] * len(ghost_nodes)
    while len(list(filter(lambda i: i is None, index_counts))) > 0 and index < 1000000000:
        index_to_use = nav_indexing[index % len(nav_indexing)]
        ghost_nodes = list(map(lambda n: nav_lookup[n][index_to_use], ghost_nodes))
        index += 1
        for i in range(len(ghost_nodes)):
            if index_counts[i] is None and ghost_nodes[i].endswith("Z"):
                index_counts[i] = index

    print(f'index_counts: {index_counts}')
    max_iterations = max(index_counts)

    multiplier = 1.0
    while not all(map(lambda ic: ((max_iterations * multiplier) % float(ic)) == 0, index_counts)) and multiplier < 1000000000:
        multiplier += 1.0

    print(f'multiplier: {multiplier}')
    print(f'max_iterations: {max_iterations}')
    print(f'max_iterations * multiplier: {max_iterations * multiplier}')

nav_map = {
    "L": 0,
    "R": 1,
}

def nav_flow(line: str) -> list[int]:
    return list(map(lambda c: nav_map[c], line))

RE_NAV_ROW = r'([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)'

def parse_line(line: str) -> tuple[str, list[str]]:
    m = re.match(RE_NAV_ROW, line)
    return (m.group(1), [m.group(2), m.group(3)])
    

if __name__ == "__main__":
    main()
