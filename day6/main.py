"""
Advent of Code 2022, Day 6
Tuning Trouble
https://adventofcode.com/2022/day/6
"""

from collections import Counter
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


START_OF_MARKER_SIZE = 4


def read_data(file_path: str) -> str:
    """Read a data stream from a file."""

    with open(file_path, encoding="utf-8") as file:
        return file.read().strip()


def find_first_start_of_packet_marker_position(data_stream: str) -> int:
    """Find the position of the first start-of-packet marker in a data stream.

    The start-of-packet marker is indicated by string of four consecutive,
    distinct characters.
    """

    # NOTE: We explicitly handle the first three characters of the data stream
    # so that we can handle the fourth character in the loop rather than having
    # to handle it separately.

    recent_character_counts = Counter(data_stream[: START_OF_MARKER_SIZE - 1])
    index = START_OF_MARKER_SIZE - 1

    while index < len(data_stream):
        current_character = data_stream[index]
        recent_character_counts[current_character] += 1

        if len(recent_character_counts) == START_OF_MARKER_SIZE:
            return index + 1

        oldest_character = data_stream[index - START_OF_MARKER_SIZE + 1]
        recent_character_counts[oldest_character] -= 1
        if recent_character_counts[oldest_character] == 0:
            del recent_character_counts[oldest_character]

        index += 1

    raise ValueError("No start-of-packet marker found.")


def main() -> None:
    """Read a data stream from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    data_stream = read_data(file_path)

    start_of_packet_marker_position = find_first_start_of_packet_marker_position(
        data_stream,
    )
    print("The first SOP marker is at position: ", end="")
    print(start_of_packet_marker_position)


if __name__ == "__main__":
    main()
