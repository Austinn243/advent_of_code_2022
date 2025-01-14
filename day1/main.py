"""
Advent of Code 2022, Day 1
Calorie Counting
https://adventofcode.com/2022/day/1
"""


from heapq import heappush, heappop, heappushpop
from os import path


INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def read_calories(file_path: str) -> list[list[int]]:
    """Read calorie information for each elf from a file."""

    calories = []
    with open(file_path, encoding="utf-8") as file:
        elf_calories = []

        for line in file:
            if line == "\n":
                calories.append(elf_calories)
                elf_calories = []
            else:
                elf_calories.append(int(line.strip()))

        if elf_calories:
            calories.append(elf_calories)

    return calories



def max_elf_calories(calories: list[list[int]]) -> int:
    """Find the maximum calories managed by any one elf."""

    max_calories = 0

    for elf_calories in calories:
        total_calories = sum(elf_calories)
        max_calories = max(max_calories, total_calories)

    return max_calories


def sum_top_three_calories(elf_calories: list[list[int]]) -> int:
    """Find the sum of the top three calorie counts for each elf."""
    
    top_three = []
    for elf in elf_calories:
        heappush(top_three, -sum(elf))

    total_calories = 0
    for _ in range(3):
        total_calories -= heappop(top_three)

    return total_calories


def main() -> None:
    """Read calorie information from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    calories = read_calories(file_path)
    print(calories)

    max_calories = max_elf_calories(calories)
    print(max_calories)

    top_three_total_calories = sum_top_three_calories(calories)
    print(top_three_total_calories)



if __name__ == "__main__":
    main()