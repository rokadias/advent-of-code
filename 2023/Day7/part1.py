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
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
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
    hand_type_order: CardOrder
    bid: int
    second_hand_type_order: CardOrder = CardOrder.NOT_APPLICABLE
    high_card: CardOrder = CardOrder.NOT_APPLICABLE

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
    card_counts: dict[str, int] = {}

    for card in hand.cards:
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
            hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[0]]
            second_hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[1]]
        else:
            hand_type = HandType.TWO_PAIR
            hand_type_order = CARD_ORDER_LOOKUP[max(more_than_one_card)]
            second_hand_type_order = CARD_ORDER_LOOKUP[min(more_than_one_card)]
            high_card = max(map(lambda card: CARD_ORDER_LOOKUP[card], filter(lambda card: card not in more_than_one_card, hand.cards)))
    elif len(more_than_one_card) == 1:
        if card_counts[more_than_one_card[0]] == 5:
            hand_type = HandType.FIVE_CARD
            hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[0]]
        elif card_counts[more_than_one_card[0]] == 4:
            hand_type = HandType.FOUR_CARD
            hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[0]]
            high_card = max(map(lambda card: CARD_ORDER_LOOKUP[card], filter(lambda card: card not in more_than_one_card, hand.cards)))
        elif card_counts[more_than_one_card[0]] == 3:
            hand_type = HandType.THREE_CARD
            hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[0]]
            high_card = max(map(lambda card: CARD_ORDER_LOOKUP[card], filter(lambda card: card not in more_than_one_card, hand.cards)))
        else:
            assert card_counts[more_than_one_card[0]] == 2
            hand_type = HandType.ONE_PAIR
            hand_type_order = CARD_ORDER_LOOKUP[more_than_one_card[0]]
            high_card = max(map(lambda card: CARD_ORDER_LOOKUP[card], filter(lambda card: card not in more_than_one_card, hand.cards)))
    else:
        assert len(more_than_one_card) == 0
        hand_type = HandType.HIGH_CARD
        high_card = max(map(lambda card: CARD_ORDER_LOOKUP[card], filter(lambda card: card not in more_than_one_card, hand.cards)))
        hand_type_order = high_card
        
    return HandClassification(
        hand_type=hand_type,
        card_order=list(map(lambda card: CARD_ORDER_LOOKUP[card], hand.cards)),
        hand_type_order=hand_type_order,
        second_hand_type_order=second_hand_type_order,
        high_card=high_card,
        bid=hand.bid,
    )

def sort_tuple(classification: HandClassification) -> tuple[HandType, CardOrder, CardOrder, CardOrder, CardOrder, CardOrder]:
    assert len(classification.card_order) == 5
    return (classification.hand_type, classification.card_order[0], classification.card_order[1], classification.card_order[2], classification.card_order[3], classification.card_order[4])

if __name__ == "__main__":
    main()
