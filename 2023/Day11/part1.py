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

    contents = list(filter(None, content.split("\n")))
    column_count = len(contents[0])
    column_insert_offset = 0
    row_count = len(contents)
    row_insert_offset = 0
    new_grid: list[str] = contents.copy()
    empty_galaxy_additions = 1

    galaxies: list[tuple[int, int]] = []
    for idx, r in enumerate(new_grid):
        galaxy_indexes = [i for i, ltr in enumerate(r) if ltr == "#"]
        galaxies.extend([(idx, i) for i in galaxy_indexes])

    galaxy_rows = set(g[0] for g in galaxies)
    galaxy_columns = set(g[1] for g in galaxies)

    expanded_galaxies: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            expanded_galaxies.append((galaxies[i], galaxies[j]))

    total = 0
    for first, second in expanded_galaxies:
        min_r = min(first[0], second[0])
        max_r = max(first[0], second[0])
        min_c = min(first[1], second[1])
        max_c = max(first[1], second[1])

        r_diff = max_r - min_r
        c_diff = max_c - min_c

        r_diff += sum(empty_galaxy_additions for r in range(min_r, max_r) if r not in galaxy_rows)
        c_diff += sum(empty_galaxy_additions for c in range(min_c, max_c) if c not in galaxy_columns)

        diff_total = r_diff + c_diff
        total += diff_total

    print(f'total: {total}')


if __name__ == "__main__":
    main()
