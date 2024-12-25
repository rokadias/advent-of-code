#!/usr/bin/env python

import re
import sys

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from math import ceil
from operator import mul

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    patterns = []
    contents = list(content.split("\n"))

    pattern: list[str] = []
    for content in contents:
        if content is None or len(content) == 0:
            patterns.append(pattern)
            pattern = []
            continue

        pattern.append(content)

    if len(pattern) > 0:
        patterns.append(pattern)

    mirrors = list(map(find_vertical_mirror, pattern))

    print(f'mirrors: {mirrors}')

def read_contents(content: str) -> tuple[list[str], list[int]]:
    parts = list(filter(None, content.split(" ")))
    assert len(parts) == 2
    vals = list(filter(None, parts[0].split(".")))
    counts = list(map(lambda c: int(c), filter(None, parts[1].split(","))))

    return vals, counts

def find_vertical_mirror(pattern: list[str]) -> int | None:
    first_pattern = pattern[0]
    for i in range(len(first_pattern) / 2, len(first_pattern)):
        if is_vertical_mirror(first_pattern, i):
            if all(map(lambda p: is_vertical_mirror(p, i), pattern[1:])):
                return i

    return None

def is_vertical_mirror(line: str, left_start: int) -> bool:
    left =  left_start
    right = left + 1
    while right < len(line):
        if line[left] != line[right]:
            return False
        left -= 1
        right += 1

    return True
        


if __name__ == "__main__":
    main()
