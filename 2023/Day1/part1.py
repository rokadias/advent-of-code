#!/usr/bin/env python

import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    numerical_chars = list(map(lambda l: list(filter(lambda s: s.isdigit(), l)), lines))
    values = list(map(lambda nc: int(f"{nc[0]}{nc[-1]}"), numerical_chars))
    value_sum = sum(values)
    print(f'value_sum: {value_sum}')


if __name__ == "__main__":
    main()
