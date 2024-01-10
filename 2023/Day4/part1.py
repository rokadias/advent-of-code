#!/usr/bin/env python

import re
import sys

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    lines = content.split("\n")
    lines = list(filter(lambda l: len(l) > 0, lines))
    cards = list(map(parse_card, lines))
    wins = list(map(count_wins, cards))
    print(f'wins: {wins}')
    points = list(map(lambda w: 2 ** (w - 1) if w > 0 else 0, wins))
    print(f'points: {points}')
    print(f'sum(points): {sum(points)}')

RE_CARD_GAME = r'Card\s+([0-9]+): ([^|]+) \| (.*)'

def count_wins(card: tuple[int, list[int], list[int]]) -> int:
    idx, winning_numbers, picking_numbers = card
    check = set(winning_numbers)
    return sum(1 for picked in picking_numbers if picked in check)

def parse_card(card_line: str) -> tuple[int, list[int], list[int]]:
    m = re.match(RE_CARD_GAME, card_line)
    if m is None:
        print(f'card_line: {card_line}')
    assert m is not None
    card_idx = int(m.group(1))
    winning_numbers = list(map(lambda num_text: int(num_text.strip()), m.group(2).split()))
    picked_numbers = list(map(lambda num_text: int(num_text.strip()), m.group(3).split()))
    return (card_idx, winning_numbers, picked_numbers)

if __name__ == "__main__":
    main()
