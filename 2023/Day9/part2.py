#!/usr/bin/env python

import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    number_lines = list(map(lambda l: list(map(lambda v: int(v), l.split())), lines))
    next_values = list(map(calculate_next_value, number_lines))
    print(f'next_values: {next_values}')
    next_values_sum = sum(next_values)
    print(f'next_values_sum: {next_values_sum}')

def calculate_next_value(numbers: list[int]) -> int:
    break_down = create_break_down(numbers)
    for idx in reversed(range(len(break_down))):
        evaluating_line = break_down[idx]
        if idx == (len(break_down) - 1):
            evaluating_line.insert(0, 0)
        else:
            evaluating_line.insert(0, evaluating_line[0] - break_down[idx + 1][0])

    return break_down[0][0]

def create_break_down(numbers: list[int]) -> list[list[int]]:
    results = [numbers]
    evaluating_line = numbers
    while any(map(lambda n: n != 0, evaluating_line)):
        new_line = []
        for idx in range(len(evaluating_line) - 1):
            new_line.append(evaluating_line[idx + 1] - evaluating_line[idx])

        results.append(new_line)
        evaluating_line = new_line

    return results

if __name__ == "__main__":
    main()
