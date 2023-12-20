#!/usr/bin/env python

import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    all_numbers = list()
    for y in range(0, len(lines)):
        all_numbers.extend(read_valid_numbers_from_line(y=y, line=lines[y], lines=lines))
    print(f'all_numbers: {all_numbers}')
    print(f'sum(all_numbers): {sum(all_numbers)}')


def read_valid_numbers_from_line(y: int, line: str, lines: list[str]) -> list[int]:
    result: list[int] = []
    has_adjaceny = False
    number_buffer = ""
    for x in range(0, len(line)):
        char_to_evaluate = line[x]
        if char_to_evaluate.isdigit():
            number_buffer += char_to_evaluate
            if not has_adjaceny:
                has_adjaceny = is_adjacent_to_symbol(x=x, y=y, lines=lines)
        else:
            if len(number_buffer) > 0 and has_adjaceny:
                result.append(int(number_buffer))
            number_buffer = ""
            has_adjaceny = False

    if len(number_buffer) > 0 and has_adjaceny:
        result.append(int(number_buffer))


    return result

def is_adjacent_to_symbol(x: int, y:int, lines: list[str]) -> bool:
    coordinates_to_check: list[tuple[int, int]] = []
    for x_adjustment in [-1, 0, 1]:
        for y_adjustment in [-1, 0, 1]:
            new_y = y + y_adjustment
            new_x = x + x_adjustment
            if x_adjustment == 0 and y_adjustment == 0:
                continue

            if new_y < 0 or new_x < 0 or new_y >= len(lines):
                continue

            if new_x >= len(lines[new_y]):
                continue

            coordinates_to_check.append((new_x, new_y))

    return any(map(lambda coordinates: not lines[coordinates[1]][coordinates[0]].isdigit() and lines[coordinates[1]][coordinates[0]] != ".", coordinates_to_check))


if __name__ == "__main__":
    main()
