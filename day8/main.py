"""
Advent of Code 2022, Day 8
Treetop Tree House
https://adventofcode.com/2022/day/8
"""

from collections.abc import Iterable
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

MIN_HEIGHT = 0
MAX_HEIGHT = 9


class Position(NamedTuple):
    """Represents a position in a grid."""

    row: int
    col: int


HeightGrid = list[list[int]]


def read_tree_heights(file_path: str) -> HeightGrid:
    """Read the heights of a grid of trees from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_tree_heights(line.strip()) for line in file]


def parse_tree_heights(line: list[str]) -> list[int]:
    """Parse the heights of trees from a line of text."""

    return [int(char) for char in line]


def find_visible_trees(sequence: Iterable[int]) -> list[int]:
    """Find the trees that are visible from outside the grid in a sequence."""

    visible = []

    tallest_encountered_height = MIN_HEIGHT - 1
    for index, height in enumerate(sequence):
        if height <= tallest_encountered_height:
            continue

        visible.append(index)
        tallest_encountered_height = height

        if height == MAX_HEIGHT:
            break

    return visible


def count_visible_trees(tree_heights: HeightGrid) -> int:
    """Count the number of trees that are visible from outside the grid."""

    visible = set()

    for row, row_values in enumerate(tree_heights):
        columns = find_visible_trees(row_values)
        visible.update((row, col) for col in columns)

        columns = find_visible_trees(reversed(row_values))
        visible.update((row, len(row_values) - col - 1) for col in columns)

    for col, col_values in enumerate(zip(*tree_heights)):
        rows = find_visible_trees(col_values)
        visible.update((row, col) for row in rows)

        rows = find_visible_trees(reversed(col_values))
        visible.update((len(col_values) - row - 1, col) for row in rows)

    return len(visible)


def main() -> None:
    """Read the heights of a grid of trees and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    tree_heights = read_tree_heights(file_path)
    print(tree_heights)

    visible_tree_count = count_visible_trees(tree_heights)
    print(f"{visible_tree_count} trees are visible from outside the grid.")


if __name__ == "__main__":
    main()
