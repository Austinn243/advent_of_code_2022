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


class ElfGroup(NamedTuple):
    """Represents a group of three elves with rucksacks."""

    first_rucksack: Rucksack
    second_rucksack: Rucksack
    third_rucksack: Rucksack


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


def create_elf_groups_from_rucksacks(rucksacks: list[Rucksack]) -> list[ElfGroup]:
    """Group the rucksacks into groups of three for the elves."""

    rucksack_groups = (rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3))
    elf_groups = [ElfGroup(*rucksack_group) for rucksack_group in rucksack_groups]

    return elf_groups


def get_badge_item(elf_group: ElfGroup) -> str:
    """Determine the badge item for a group of elves."""

    item_sets = []

    for elf_rucksack in elf_group:
        first_compartment, second_compartment = elf_rucksack
        distinct_items = set(first_compartment + second_compartment)
        item_sets.append(distinct_items)

    common_items = set.intersection(*item_sets)

    return common_items.pop()


def main() -> None:
    """Read the contents of each rucksack from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    rucksacks = read_rucksacks(file_path)

    misplaced_items = map(find_item_in_both_compartments, rucksacks)
    misplaced_item_priorities = [get_item_priority(item) for item in misplaced_items]
    misplaced_item_priority_sum = sum(misplaced_item_priorities)
    print(f"The priority sum of the misplaced items is {misplaced_item_priority_sum}")

    elf_groups = create_elf_groups_from_rucksacks(rucksacks)
    elf_group_badges = [get_badge_item(group) for group in elf_groups]
    badge_priority_sum = sum(get_item_priority(badge) for badge in elf_group_badges)
    print(f"The priority sum of the badge items is {badge_priority_sum}")


if __name__ == "__main__":
    main()
