#!/usr/bin/env python

import re
import sys

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from math import ceil
from operator import mul

class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    contents = list(filter(None, content.split("\n")))
    starting_index = next(filter(lambda x: x[1] >= 0, map(lambda content: (content[0], content[1].find("S")), enumerate(contents))))
    counted = min(filter(lambda count: count > 0, map(lambda d: count_spaces(contents, move_in_direction(starting_index, d), d), (d for d in Direction))))
    print(f'counted: {counted}')
    steps = ceil(counted / 2.0)
    print(f'steps: {steps}')

def count_spaces(tiles: list[str], location: tuple[int, int], direction: Direction, count: int = 0) -> int:
    new_count = count
    loc = location

    while True:
        new_count += 1
        current_char = tiles[loc[0]][loc[1]]
    
        new_direction = None
        match current_char:
            case "S": 
                return new_count
            case "|":
                if direction == Direction.NORTH or direction == Direction.SOUTH:
                    new_direction = direction
                else:
                    return -1
            case "-":
                if direction == Direction.WEST or direction == Direction.EAST:
                    new_direction = direction
                else:
                    return -1
            case "L":
                if direction == Direction.WEST:
                    new_direction = Direction.NORTH
                elif direction == Direction.SOUTH:
                    new_direction = Direction.EAST
                else:
                    return -1
            case "J":
                if direction == Direction.EAST:
                    new_direction = Direction.NORTH
                elif direction == Direction.SOUTH:
                    new_direction = Direction.WEST
                else:
                    return -1
            case "7":
                if direction == Direction.EAST:
                    new_direction = Direction.SOUTH
                elif direction == Direction.NORTH:
                    new_direction = Direction.WEST
                else:
                    return -1
            case "F":
                if direction == Direction.WEST:
                    new_direction = Direction.SOUTH
                elif direction == Direction.NORTH:
                    new_direction = Direction.EAST
                else:
                    return -1
            case ".":
                return -1

        match new_direction:
            case Direction.NORTH:
                if loc[0] == 0:
                    return -1
            case Direction.SOUTH:
                if loc[0] == len(tiles):
                    return -1
            case Direction.WEST:
                if loc[1] == 0:
                    return -1
            case Direction.EAST:
                if loc[0] == len(tiles[loc[0]]):
                    return -1

        assert new_direction is not None
        loc = move_in_direction(loc, new_direction)
        direction = new_direction

    assert False

def move_in_direction(loc: tuple[int, int], direction: Direction) -> tuple[int, int]:
    match direction:
        case Direction.NORTH:
            return (loc[0] - 1, loc[1])
        case Direction.SOUTH:
            return (loc[0] + 1, loc[1])
        case Direction.WEST:
            return (loc[0], loc[1] - 1)
        case Direction.EAST:
            return (loc[0], loc[1] + 1)


if __name__ == "__main__":
    main()
