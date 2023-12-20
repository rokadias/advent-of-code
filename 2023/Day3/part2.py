#!/usr/bin/env python

import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    gear_ratios: dict[tuple[int, int], list[int]] = dict()
    for y in range(0, len(lines)):
        gears = read_gear_ratios_from_line(y=y, line=lines[y], lines=lines)
        for coor, numbers in gears.items():
            ratios = gear_ratios.setdefault(coor, [])
            ratios.extend(numbers)

    products = list(map(lambda numbers: numbers[0] * numbers[1], filter(lambda numbers: len(numbers) == 2,gear_ratios.values())))
    print(f'products: {products}')
    print(f'sum(products): {sum(products)}')


def read_gear_ratios_from_line(y: int, line: str, lines: list[str]) -> dict[tuple[int, int], list[int]]:
    result: dict[tuple[int, int], list[int]] = {}
    adjacent_ratio_symbols: set[tuple[int, int]] = set()
    number_buffer = ""
    for x in range(0, len(line)):
        char_to_evaluate = line[x]
        if char_to_evaluate.isdigit():
            number_buffer += char_to_evaluate
            adjacent_symbols = get_adjacent_to_ratio_symbol(x=x, y=y, lines=lines)
            adjacent_ratio_symbols.update(adjacent_symbols)
        else:
            if len(number_buffer) > 0 and len(adjacent_ratio_symbols) > 0:
                number = int(number_buffer)
                for symbol_x, symbol_y in adjacent_ratio_symbols:
                    gear_ratios = result.setdefault((symbol_x, symbol_y), [])
                    gear_ratios.append(number)

            number_buffer = ""
            adjacent_ratio_symbols = set()

    if len(number_buffer) > 0 and len(adjacent_ratio_symbols) > 0:
        number = int(number_buffer)
        for symbol_x, symbol_y in adjacent_ratio_symbols:
            gear_ratios = result.setdefault((symbol_x, symbol_y), [])
            gear_ratios.append(number)


    return result

def get_adjacent_to_ratio_symbol(x: int, y:int, lines: list[str]) -> list[tuple[int, int]]:
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

    return list(filter(lambda coordinates: lines[coordinates[1]][coordinates[0]] == "*", coordinates_to_check))


if __name__ == "__main__":
    main()
