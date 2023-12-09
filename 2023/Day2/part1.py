#!/usr/bin/env python

import re
import sys

max_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    games = map(parse_game, lines)
    valid_games = list(filter(lambda g: all(map(valid_pull, g[1])), games))
    valid_games_indexs = list(map(lambda g: g[0], valid_games))
    print(f'valid_games_indexs: {valid_games_indexs}')
    valid_sum = sum(valid_games_indexs)
    print(f'valid_sum: {valid_sum}')

def valid_pull(pulls: list[tuple[int, str]]) -> bool:
    validity = map(lambda pull: pull[0] <= max_cubes[pull[1]], pulls)
    return all(validity)

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
