#!/usr/bin/env python

import re
import sys

from dataclasses import dataclass
from functools import reduce
from operator import mul

RE_TIME = r'Time:\s+(.*)'
RE_DISTANCE = r'Distance:\s+(.*)'

@dataclass
class Race:
    time: int
    distance: int


def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    races: list[Race] = []
    contents = list(filter(None, content.split("\n")))
    assert len(contents) == 2

    content_idx = 0
    times_content = re.match(RE_TIME, contents[content_idx])
    assert times_content is not None
    times_text = re.sub(r"\s+", "", times_content.group(1))
    times = [int(times_text)]

    content_idx += 1
    distances_content = re.match(RE_DISTANCE, contents[content_idx])
    assert distances_content is not None
    distances_text = re.sub(r"\s+", "", distances_content.group(1))
    distances = [int(distances_text)]

    for time, distance in zip(times, distances):
        races.append(
            Race(
                time=time,
                distance=distance,
            )
        )

    winners = list(map(count_winners, races))
    print(f'winners: {winners}')
    product_winners = reduce(mul, winners)
    print(f'product_winners: {product_winners}')
    

def count_winners(race: Race) -> int:
    total_values = race.time + 1
    loser_count = 0

    while loser_count < total_values:
        distance = loser_count * (race.time - loser_count)
        if distance > race.distance:
            break

        loser_count += 1

    return min(total_values - (2 * loser_count), total_values) 


if __name__ == "__main__":
    main()
