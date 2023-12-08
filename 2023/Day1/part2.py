#!/usr/bin/env python

import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    numerical_chars = list(map(text_to_digits, lines))
    values = list(map(lambda nc: int(f"{nc[0]}{nc[-1]}"), numerical_chars))
    value_sum = sum(values)
    print(f'value_sum: {value_sum}')


digit_map = {
    "0": ["0"],
    "1": ["1"],
    "2": ["2"],
    "3": ["3"],
    "4": ["4"],
    "5": ["5"],
    "6": ["6"],
    "7": ["7"],
    "8": ["8"],
    "9": ["9"],
    "zero": ["0"],
    "one": ["1"],
    "two": ["2"],
    "three": ["3"],
    "four": ["4"],
    "five": ["5"],
    "six": ["6"],
    "seven": ["7"],
    "eight": ["8"],
    "nine": ["9"],
    "ten": ["1","0"],
    "eleven": ["1","1"],
    "twelve": ["1","2"],
    "thirteen": ["1","3"],
    "fourteen": ["1","4"],
    "fiveteen": ["1","5"],
    "sixteen": ["1","6"],
    "seventeen": ["1","7"],
    "eighteen": ["1","8"],
    "nineteen": ["1","9"],
    "twenty": ["2","0"],
    "thirty": ["3","0"],
    "fourty": ["4","0"],
    "fivety": ["5","0"],
    "sixty": ["6","0"],
    "seventy": ["7","0"],
    "eighty": ["8","0"],
    "ninety": ["9","0"],
}

def text_to_digits(text: str) -> list[str]:
    result = []
    index = 0
    while index < len(text):
        k = next(
            filter(lambda value: text[index:index + len(value)] == value, digit_map.keys()),
            None
        )

        if k is not None:
            result.extend(digit_map[k])

        index += 1

    return result

if __name__ == "__main__":
    main()
