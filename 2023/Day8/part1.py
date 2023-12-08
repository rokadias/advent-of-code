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
    current_node = "AAA"
    while current_node != "ZZZ" and index < 100000:
        index_to_use = nav_indexing[index % len(nav_indexing)]
        nav = nav_lookup[current_node]
        current_node = nav[index_to_use]
        index += 1

    print(f'index: {index}')

nav_map = {
    "L": 0,
    "R": 1,
}

def nav_flow(line: str) -> list[int]:
    return list(map(lambda c: nav_map[c], line))

RE_NAV_ROW = r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)'

def parse_line(line: str) -> tuple[str, list[str]]:
    m = re.match(RE_NAV_ROW, line)
    return (m.group(1), [m.group(2), m.group(3)])
    

if __name__ == "__main__":
    main()
