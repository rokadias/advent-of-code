#!/usr/bin/env python

import re
import sys
from functools import reduce
from operator import mul

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    games = map(parse_game, lines)
    games_powers = list(map(lambda g: calc_pulls_power(g[1]), games))
    print(f'games_powers: {games_powers}')
    power_sum = sum(games_powers)
    print(f'power_sum: {power_sum}')

def calc_pulls_power(pulls: list[list[tuple[int, str]]]) -> bool:
    max_per_color = {}
    for pull in pulls:
        for count, color in pull:
            if color in max_per_color:
                max_per_color[color] = max(max_per_color[color], count)
            else:
                max_per_color[color] = count

    return reduce(mul, max_per_color.values())

RE_PULL = r'([0-9]+) ([A-Za-z]+)'

def parse_pull(text: str) -> tuple[int, str]:
    m = re.match(RE_PULL, text.strip())
    return (int(m.group(1)), m.group(2))

RE_GAME = r'Game ([0-9]+): (.*)'

def parse_game(game_line: str) -> tuple[int, list[list[tuple[int,str]]]]:
    m = re.match(RE_GAME, game_line)
    game_idx = int(m.group(1))
    pulls = m.group(2).split(";")
    pulls = list(filter(lambda l: len(l) > 0, pulls))
    parsed_pulls = list(map(lambda pulls: list(map(parse_pull, pulls.split(','))), pulls))
    return (game_idx, parsed_pulls)

if __name__ == "__main__":
    main()
