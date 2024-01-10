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
    copies_count = [1] * len(cards)
    for idx, card in enumerate(cards):
        count_wins(card, idx, copies_count)
    print(f'sum(copies_count): {sum(copies_count)}')

RE_CARD_GAME = r'Card\s+([0-9]+): ([^|]+) \| (.*)'

def count_wins(card: tuple[int, list[int], list[int]], current_index, copies_count: list[int]) -> None:
    total_copies = copies_count[current_index]
    idx, winning_numbers, picking_numbers = card
    check = set(winning_numbers)
    card_wins = sum(1 for picked in picking_numbers if picked in check)
    for win_card_index in range(card_wins):
        copies_count[win_card_index + current_index + 1] += total_copies

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
