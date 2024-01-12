#!/usr/bin/env python

import re
import sys

from collections import deque
from dataclasses import dataclass

from functools import reduce

RE_SEEDS = r'seeds: (.*)'
RE_TO_SOIL = r'seed-to-soil map:'
RE_TO_FERTILIZER = r'soil-to-fertilizer map:'
RE_TO_WATER = r'fertilizer-to-water map:'
RE_TO_LIGHT = r'water-to-light map:'
RE_TO_TEMPERATURE = r'light-to-temperature map:'
RE_TO_HUMIDITY = r'temperature-to-humidity map:'
RE_TO_LOCATION = r'humidity-to-location map:'

@dataclass
class ValueMapping:
    source_start: int
    destination_start: int
    value_count: int

@dataclass
class SeedRange:
    start: int
    count: int


def main() -> None:
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        content = f.read()

    maps: list[list[ValueMapping]] = []

    contents = content.split("\n\n")
    assert len(contents) == 8

    content_idx = 0
    seeds_content = re.match(RE_SEEDS, contents[content_idx])
    assert seeds_content is not None
    seed_counts = list(map(lambda x: int(x), seeds_content.group(1).split()))
    seed_ranges: list[list[SeedRange]] = []
    for idx in range(0, len(seed_counts), 2):
        start = seed_counts[idx]
        count = seed_counts[idx + 1]
        seed_ranges.append(
            [SeedRange(
                start=start,
                count=count,
            )]
        )

    content_idx += 1
    dict_content = re.match(RE_TO_SOIL, contents[content_idx])
    assert dict_content is not None
    soil_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(soil_map)

    content_idx += 1
    dict_content = re.match(RE_TO_FERTILIZER, contents[content_idx])
    assert dict_content is not None
    fertilizer_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(fertilizer_map)

    content_idx += 1
    dict_content = re.match(RE_TO_WATER, contents[content_idx])
    assert dict_content is not None
    water_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(water_map)

    content_idx += 1
    dict_content = re.match(RE_TO_LIGHT, contents[content_idx])
    assert dict_content is not None
    light_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(light_map)

    content_idx += 1
    dict_content = re.match(RE_TO_TEMPERATURE, contents[content_idx])
    assert dict_content is not None
    temp_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(temp_map)

    content_idx += 1
    dict_content = re.match(RE_TO_HUMIDITY, contents[content_idx])
    assert dict_content is not None
    humidity_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(humidity_map)

    content_idx += 1
    dict_content = re.match(RE_TO_LOCATION, contents[content_idx])
    assert dict_content is not None
    location_map = lines_to_dict(contents[content_idx].split("\n")[1:])
    maps.append(location_map)

    print(f'seed_ranges: {seed_ranges}')
    locations = list(map(lambda seed_range: reduce(resolve_value, maps, seed_range), seed_ranges))
    print(f'locations: {locations}')
    print(f'min(locations): {min(map(lambda location: min(map(lambda l: l.start, location)), locations))}')

RE_RANGE_MAP = r'([0-9]+) ([0-9]+) ([0-9]+)'

def lines_to_dict(lines: list[str]) -> list[ValueMapping]:
    result = []
    for line in filter(None, lines):
        matches = re.match(RE_RANGE_MAP, line)
        assert matches is not None
        destination_start = int(matches.group(1))
        source_start = int(matches.group(2))
        value_count = int(matches.group(3))

        result.append(ValueMapping(
            destination_start=destination_start,
            source_start=source_start,
            value_count=value_count,
        ))

    return result

def resolve_value(seed_ranges: list[SeedRange], mappings: list[ValueMapping]) -> list[SeedRange]:
    results = []
    for seed_range in seed_ranges:
        results.extend(evalutate_range(seed_range, mappings))

    return results

def evalutate_range(seed_range: SeedRange, mappings: list[ValueMapping]) -> list[SeedRange]:
    result = []
    taken_care_of_ranges: list[SeedRange] = []
    for mapping in mappings:
        delta = seed_range.start - mapping.source_start
        range_end = (seed_range.start + seed_range.count - 1)
        ending_delta = range_end - mapping.source_start
        if delta >= 0 and (delta - 1) <= mapping.value_count:
            if mapping.value_count >= (seed_range.count + delta - 1):
                result.append(
                    SeedRange(
                        start=mapping.destination_start + delta,
                        count=seed_range.count,
                    )
                )
                return result
            else:
                result.append(
                    SeedRange(
                        start=mapping.destination_start + delta,
                        count=mapping.value_count - delta,
                    )
                )
                taken_care_of_ranges.append(
                    SeedRange(
                        start=seed_range.start,
                        count=mapping.value_count - delta,
                    )
                )
        elif ending_delta >= 0 and delta <= 0:
            if ending_delta <= mapping.value_count:
                result.append(
                    SeedRange(
                        start=mapping.destination_start,
                        count=ending_delta + 1,
                    )
                )
                taken_care_of_ranges.append(
                    SeedRange(
                        start=mapping.source_start,
                        count=ending_delta + 1,
                    )
                )
            else:
                result.append(
                    SeedRange(
                        start=mapping.destination_start,
                        count=mapping.value_count
                    )
                )
                taken_care_of_ranges.append(
                    SeedRange(
                        start=mapping.source_start,
                        count=mapping.value_count,
                    )
                )

    sorted_taken_care_of = sorted(taken_care_of_ranges, key=lambda sr: sr.start)
    remaining_range: SeedRange | None = seed_range

    while len(sorted_taken_care_of) != 0 and remaining_range is not None:
        taken_care_of = sorted_taken_care_of.pop(0)
        if remaining_range.start != taken_care_of.start:
            count = taken_care_of.start - remaining_range.start
            result.append(
                SeedRange(
                    start=remaining_range.start,
                    count=taken_care_of.start - remaining_range.start
                )
            )
            remaining_range = SeedRange(
                start=taken_care_of.start,
                count=remaining_range.count - taken_care_of.count
            )

        assert remaining_range.start == taken_care_of.start
        remaining_range = SeedRange(
            start=taken_care_of.start + taken_care_of.count,
            count=remaining_range.count - taken_care_of.count
        )
        if remaining_range.count <= 0:
            remaining_range = None
            break

    if remaining_range is not None and len(sorted_taken_care_of) == 0:
        result.append(remaining_range)

    return result
            

if __name__ == "__main__":
    main()
