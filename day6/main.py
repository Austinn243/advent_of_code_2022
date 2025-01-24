"""
Advent of Code 2022, Day 6
Tuning Trouble
https://adventofcode.com/2022/day/6
"""

from collections import Counter
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


START_OF_MESSAGE_MARKER_SIZE = 14
START_OF_PACKET_MARKER_SIZE = 4


def read_data(file_path: str) -> str:
    """Read a data stream from a file."""

    with open(file_path, encoding="utf-8") as file:
        return file.read().strip()


def find_first_marker_position(data_stream: str, marker_size: int) -> int:
    """Find the position of the first marker of the given size in a data stream.

    Markers of size N are indicated by a sequence of N distinct, consecutive characters.
    """

    # NOTE: We explicitly handle the first three characters of the data stream
    # so that we can handle the fourth character in the loop rather than having
    # to handle it separately.

    recent_character_counts = Counter(data_stream[: marker_size - 1])
    index = marker_size - 1

    while index < len(data_stream):
        current_character = data_stream[index]
        recent_character_counts[current_character] += 1

        if len(recent_character_counts) == marker_size:
            return index + 1

        oldest_character = data_stream[index - marker_size + 1]
        recent_character_counts[oldest_character] -= 1
        if recent_character_counts[oldest_character] == 0:
            del recent_character_counts[oldest_character]

        index += 1

    raise ValueError("No start-of-packet marker found.")


def main() -> None:
    """Read a data stream from a file and process it."""

    input_file = TEST_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    data_stream = read_data(file_path)

    start_of_packet_marker_position = find_first_marker_position(
        data_stream,
        START_OF_PACKET_MARKER_SIZE,
    )
    print("The first start of packet marker is at position: ", end="")
    print(start_of_packet_marker_position)

    start_of_message_marker_position = find_first_marker_position(
        data_stream,
        START_OF_MESSAGE_MARKER_SIZE,
    )
    print("The first start of message marker is at position: ", end="")
    print(start_of_message_marker_position)


if __name__ == "__main__":
    main()
