#!/usr/bin/env python

import re
import sys

from dataclasses import dataclass
from enum import auto, IntEnum
from functools import reduce
from operator import mul

RE_HAND = r'([TAJQK2-9]+)\s+([0-9]+)'

class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_CARD = auto()
    FULL_HOUSE = auto()
    FOUR_CARD = auto()
    FIVE_CARD = auto()

class CardOrder(IntEnum):
    NOT_APPLICABLE = auto()
    JACK = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()

CARD_ORDER_LOOKUP = {
    "2": CardOrder.TWO,
    "3": CardOrder.THREE,
    "4": CardOrder.FOUR,
    "5": CardOrder.FIVE,
    "6": CardOrder.SIX,
    "7": CardOrder.SEVEN,
    "8": CardOrder.EIGHT,
    "9": CardOrder.NINE,
    "T": CardOrder.TEN,
    "J": CardOrder.JACK,
    "Q": CardOrder.QUEEN,
    "K": CardOrder.KING,
    "A": CardOrder.ACE,
}

@dataclass
class Hand:
    cards: str
    bid: int

@dataclass
class HandClassification:
    hand_type: HandType
    card_order: list[CardOrder]
    bid: int

def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    contents = list(filter(None, content.split("\n")))
    hands = list(map(parse_hand, contents))

    hands_classified = list(map(classify_hand, hands))
    sorted_hands_classified = sorted(hands_classified, key=lambda hand_classification: sort_tuple(hand_classification))
    total_winnings = 0

    for idx, classification in enumerate(sorted_hands_classified):
        total_winnings += classification.bid * (idx + 1)

    print(f'total_winnings: {total_winnings}')
    

def parse_hand(content: str) -> Hand:
    hand_content = re.match(RE_HAND, content)
    assert hand_content is not None

    return Hand(
        cards=hand_content.group(1),
        bid=int(hand_content.group(2))
    )

def classify_hand(hand: Hand) -> HandClassification:
    hand_types = list(map(lambda r: get_hand_type(hand.cards.replace("J", r)), (r for r in CARD_ORDER_LOOKUP.keys() if r != "J")))
    hand_type = max(hand_types)

    return HandClassification(
        hand_type=hand_type,
        card_order=list(map(lambda card: CARD_ORDER_LOOKUP[card], hand.cards)),
        bid=hand.bid,
    )

def get_hand_type(cards: str) -> HandType:
    card_counts: dict[str, int] = {}

    for card in cards:
        count = card_counts.setdefault(card, 0)
        card_counts[card] = count + 1

    more_than_one_card = list(map(lambda card_count: card_count[0], filter(lambda card_count: card_count[1] > 1, card_counts.items())))
    more_than_one_card = sorted(more_than_one_card, key=lambda card: card_counts[card], reverse=True)
    assert len(more_than_one_card) < 3
    second_hand_type_order: CardOrder = CardOrder.NOT_APPLICABLE
    high_card: CardOrder = CardOrder.NOT_APPLICABLE
    if len(more_than_one_card) == 2:
        if card_counts[more_than_one_card[0]] == 3:
            hand_type = HandType.FULL_HOUSE
        else:
            hand_type = HandType.TWO_PAIR
    elif len(more_than_one_card) == 1:
        if card_counts[more_than_one_card[0]] == 5:
            hand_type = HandType.FIVE_CARD
        elif card_counts[more_than_one_card[0]] == 4:
            hand_type = HandType.FOUR_CARD
        elif card_counts[more_than_one_card[0]] == 3:
            hand_type = HandType.THREE_CARD
        else:
            assert card_counts[more_than_one_card[0]] == 2
            hand_type = HandType.ONE_PAIR
    else:
        assert len(more_than_one_card) == 0
        hand_type = HandType.HIGH_CARD

    return hand_type

def sort_tuple(classification: HandClassification) -> tuple[HandType, CardOrder, CardOrder, CardOrder, CardOrder, CardOrder]:
    assert len(classification.card_order) == 5
    return (classification.hand_type, classification.card_order[0], classification.card_order[1], classification.card_order[2], classification.card_order[3], classification.card_order[4])

if __name__ == "__main__":
    main()
