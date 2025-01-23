"""
Advent of Code 2022, Day 3
Rucksack Reorganization
https://adventofcode.com/2022/day/3
"""

from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


class Rucksack(NamedTuple):
    """Represents a rucksack with two compartments."""

    first_compartment: list[str]
    second_compartment: list[str]


def read_rucksacks(file_path: str) -> list[Rucksack]:
    """Read information about rucksacks from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_rucksack(line) for line in file]


def parse_rucksack(line: str) -> Rucksack:
    """Parse a rucksack from a line of text."""

    contents = list(line.strip())

    left_contents = contents[: len(contents) // 2]
    right_contents = contents[len(contents) // 2 :]

    return Rucksack(left_contents, right_contents)


def find_item_in_both_compartments(rucksack: Rucksack) -> str:
    """Locate the item that was mistakenly placed in both compartments."""

    first_compartment, second_compartment = rucksack

    distinct_first_compartment_items = set(first_compartment)
    distinct_compartment_items = set(second_compartment)

    common_items = distinct_first_compartment_items & distinct_compartment_items

    return common_items.pop()


def get_item_priority(item: str) -> int:
    """Determine the priority of an item based on its identifier."""

    alphabet_position = ord(item.upper()) - ord("A") + 1
    priority = alphabet_position + 26 if item.isupper() else alphabet_position

    return priority


def main() -> None:
    """Read the contents of each rucksack from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    rucksacks = read_rucksacks(file_path)

    misplaced_items = [
        find_item_in_both_compartments(rucksack) for rucksack in rucksacks
    ]
    misplaced_item_priorities = [get_item_priority(item) for item in misplaced_items]
    priority_sum = sum(misplaced_item_priorities)
    print(f"The sum of the priority values of the misplaced items is {priority_sum}")


if __name__ == "__main__":
    main()
