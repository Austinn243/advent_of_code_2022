"""
Advent of Code 2022, Day 5
Supply Stacks
https://adventofcode.com/2022/day/5
"""

import re
from os import path
from typing import Callable, NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


MOVE_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")


class Move(NamedTuple):
    """Represents a movement of supply stacks."""

    amount: int
    source: int
    destination: int


SupplyStack = list[str]


class Parameters(NamedTuple):
    """Represents the parameters of the supply stacks."""

    # NOTE: The stacks are 1-indexed in the input, so we need to ensure
    # that we decrement the stack numbers before using them as indices.

    initial_stacks: list[SupplyStack]
    rearrangement_procedure: list[Move]


def read_operation_parameters(file_path: str) -> Parameters:
    """Read the initial supply stacks and the rearrangement procedure from a file."""

    with open(file_path, encoding="utf-8") as file:
        lines = iter(file.readlines())

    # NOTE: The spacing is important for the lines related to the initial stacks
    # but not for the lines related to the rearrangement procedure. That's why we
    # avoid stripping the lines initially and only do it when necessary.

    stacks_lines = []
    while (line := next(lines)) != "\n":
        stacks_lines.append(line)

    initial_stacks = parse_initial_stacks(stacks_lines)
    rearrangement_procedure = [parse_move(line.strip()) for line in lines]

    return Parameters(initial_stacks, rearrangement_procedure)


def parse_initial_stacks(lines: list[str]) -> list[SupplyStack]:
    """Parse the initial supply stacks from a list of lines."""

    stack_numbers_line = lines.pop().strip()
    stack_count = int(stack_numbers_line[-1])

    line_length = len(lines[0])
    stacks = [[] for _ in range(stack_count)]
    for line in reversed(lines):
        for i in range(1, line_length, 4):
            crate = line[i]
            if crate == " ":
                continue

            stack_number = (i - 1) // 4
            stacks[stack_number].append(crate)

    return stacks


def parse_move(line: str) -> Move:
    """Parse a move from a line of text."""

    match = MOVE_REGEX.match(line)
    if not match:
        raise ValueError(f"Invalid move: {line}")

    amount, source, destination = map(int, match.groups())

    return Move(amount, source, destination)


def execute_rearrangement(
    initial_stacks: list[SupplyStack],
    rearrangement_procedure: list[Move],
    move_crates: Callable[[list[SupplyStack], Move], list[SupplyStack]],
) -> list[SupplyStack]:
    """Execute the rearrangement procedure on the initial supply stacks."""

    stacks = [stack.copy() for stack in initial_stacks]

    for move in rearrangement_procedure:
        move_crates(stacks, move)

    return stacks


def move_crates_one_by_one(stacks: list[SupplyStack], move: Move) -> list[SupplyStack]:
    """Move crates between stacks one by one."""

    amount, source, destination = move

    source_stack = stacks[source - 1]
    destination_stack = stacks[destination - 1]

    for _ in range(amount):
        crate = source_stack.pop()
        destination_stack.append(crate)

    return stacks


def move_crates_as_group(stacks: list[SupplyStack], move: Move) -> list[SupplyStack]:
    """Move crates between stacks as a group.

    This maintains their relative ordering when moving them.
    """

    amount, source, destination = move

    source_stack = stacks[source - 1]
    destination_stack = stacks[destination - 1]

    crates = source_stack[-amount:]
    source_stack[-amount:] = []

    destination_stack.extend(crates)

    return stacks


def combine_top_items(stacks: list[SupplyStack]) -> str:
    """Combine the top items of each stack into a single string."""

    return "".join(stack[-1] for stack in stacks)


def main() -> None:
    """Read information about the initial supply stacks and moves and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    initial_stacks, rearrangement_procedure = read_operation_parameters(file_path)

    final_stacks_with_one_by_one_movements = execute_rearrangement(
        initial_stacks,
        rearrangement_procedure,
        move_crates_one_by_one,
    )
    top_items_with_one_by_one_movements = combine_top_items(
        final_stacks_with_one_by_one_movements,
    )
    print("After moving the crates one by one:")
    print(f"The combined top items are: {top_items_with_one_by_one_movements}")

    final_stacks_with_group_movements = execute_rearrangement(
        initial_stacks,
        rearrangement_procedure,
        move_crates_as_group,
    )
    top_items_with_group_movements = combine_top_items(
        final_stacks_with_group_movements,
    )
    print("After moving the crates as a group:")
    print(f"The combined top items are: {top_items_with_group_movements}")


if __name__ == "__main__":
    main()
