#!/usr/bin/env python

import re
import sys

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
    seeds = list(map(lambda x: int(x), seeds_content.group(1).split()))

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

    locations = list(map(lambda seed: reduce(resolve_value, maps, seed), seeds))
    soils = list(map(lambda seed: resolve_value(seed, soil_map), seeds))
    print(f'locations: {locations}')
    print(f'min(locations): {min(locations)}')

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

def resolve_value(value: int, mappings: list[ValueMapping]) -> int:
    for mapping in mappings:
        delta = value - mapping.source_start
        if delta > 0 and delta < mapping.value_count:
            return mapping.destination_start + delta

    return value

if __name__ == "__main__":
    main()
