"""
Advent of Code 2022, Day 4
Camp Cleanup
https://adventofcode.com/2022/day/4
"""

from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


class Assignment(NamedTuple):
    """Represents a cleanup assignment for a camper."""

    start_section: int
    end_section: int


class AssignmentPair(NamedTuple):
    """Represents a pair of cleanup assignments for two campers."""

    camper1_assignment: Assignment
    camper2_assignment: Assignment


def read_assignment_pairs(file_name: str) -> list[AssignmentPair]:
    """Read the assignment pairs from the given file."""

    with open(file_name, encoding="utf-8") as file:
        return [parse_assignment_pair(line.strip()) for line in file]


def parse_assignment_pair(line: str) -> AssignmentPair:
    """Parse a pair of assignments from a line of text."""

    camper1_segment, camper2_segment = line.split(",")

    camper1_start, camper1_end = camper1_segment.split("-")
    camper2_start, camper2_end = camper2_segment.split("-")

    camper1_assignment = Assignment(int(camper1_start), int(camper1_end))
    camper2_assignment = Assignment(int(camper2_start), int(camper2_end))

    return AssignmentPair(camper1_assignment, camper2_assignment)


def assignments_have_full_overlap(assignment_pair: AssignmentPair) -> bool:
    """Check if one assignment completely overlaps the other."""

    start1, end1 = assignment_pair.camper1_assignment
    start2, end2 = assignment_pair.camper2_assignment

    assignment1_overlaps_2 = start1 <= start2 <= end2 <= end1
    assignment2_overlaps_1 = start2 <= start1 <= end1 <= end2

    return assignment1_overlaps_2 or assignment2_overlaps_1


def count_assignment_pairs_with_full_overlap(
    assignment_pairs: list[AssignmentPair],
) -> int:
    """Count the number of assignment pairs with full overlap."""

    return sum(assignments_have_full_overlap(pair) for pair in assignment_pairs)


def main() -> None:
    """Read information about the cleanup assignments from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    assignment_pairs = read_assignment_pairs(file_path)
    print(assignment_pairs)

    full_overlap_count = count_assignment_pairs_with_full_overlap(assignment_pairs)
    print(full_overlap_count)


if __name__ == "__main__":
    main()
