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
    parsed = list(map(read_contents, contents))
    print(f'parsed: {parsed}')
    counted = list(map(lambda p: count_arrangements(p[0], p[1]), parsed))
    print(f'counted: {counted}')
    print(f'sum(counted): {sum(counted)}')
    

def read_contents(content: str) -> tuple[list[str], list[int]]:
    parts = list(filter(None, content.split(" ")))
    assert len(parts) == 2
    vals = list(filter(None, parts[0].split(".")))
    counts = list(map(lambda c: int(c), filter(None, parts[1].split(","))))

    return vals, counts


def count_arrangements(starting_val: list[str], damage_counts: list[int]) -> int:
    processing = [("", starting_val, damage_counts.copy())]
    total = 0
    already_accounted_for: set[tuple[str, int]] = set()

    while processing:
        existing_val, val, current_damage_count = processing.pop()
        copy_dc = current_damage_count.copy()
        next_val = val.copy()

        print()
        print(f'existing_val: {existing_val}')
        print(f'val: {val}')
        print(f'current_damage_count: {current_damage_count}')

        if len(val) > 0 and len(copy_dc) > 0 and copy_dc[0] > len(val[0]):
            next_val.pop(0)
            if len(next_val) == 0:
                continue
            else:
                processing.append((existing_val + ".", next_val, copy_dc))
                continue

        if len(val) > 0:
            match val[0][0]:
                case "#":
                    if copy_dc[0] > 0:
                        copy_dc[0] = copy_dc[0] - 1

                    existing_val += "#"
                    new_str_val = val[0][1:]
                    if copy_dc[0] == 0:
                        copy_dc.pop(0)
                        if len(new_str_val) > 0 and new_str_val[0] == "#":
                            # Ignore, since it doesn't match the damage_counts
                            continue
                        elif len(new_str_val) > 0 and new_str_val[0] == "?":
                            new_str_val = val[0][2:]
                            existing_val += "."
                    else:
                        if len(new_str_val) == 0:
                            # Ignore, since it doesn't match the damage_counts
                            continue

                    if len(new_str_val) == 0:
                        next_val.pop(0)
                        existing_val += "."
                    else:
                        next_val[0] = new_str_val

                    if len(copy_dc) == 0 and (len(next_val) == 0 or len(next_val[0].replace("?", "")) == 0):
                        print(f'existing_val: {existing_val}')
                        print(f'next_val: {next_val}')
                        total += 1
                        print(f'total: {total}')
                        continue
                    elif len(copy_dc) == 0:
                        continue
                    else:
                        processing.append((existing_val, next_val, copy_dc))
                case "?":
                    hash_val = val.copy()
                    dot_val = val.copy()
                    hash_val[0] = "#" + val[0][1:]
                    dot_val[0] = val[0][1:]
                    if len(dot_val[0]) == 0:
                        dot_val.pop(0)

                    if len(copy_dc) == 0 and len(dot_val) == 0:
                        total += 1
                    elif len(existing_val) == 0 or existing_val[-1] == ".":
                        processing.append((existing_val + ".", dot_val, copy_dc))

                    processing.append((existing_val, hash_val, copy_dc))
                case _:
                    assert False

    return total
                    

if __name__ == "__main__":
    main()
