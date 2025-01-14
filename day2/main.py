"""
Advent of Code 2022, Day 2
Rock Paper Scissors
https://adventofcode.com/2022/day/2
"""

from enum import IntEnum
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"



class Choice(IntEnum):
    """Choices for Rock Paper Scissors."""

    ROCK = 1 
    PAPER = 2
    SCISSORS = 3


class Outcome(IntEnum):
    """Outcomes for Rock Paper Scissors."""

    WIN = 1
    LOSE = 2
    DRAW = 3

Cipher = dict[str, Choice]
DecryptedStrategy = tuple[Choice, Choice]
EncryptedStrategy = tuple[str, str]
ChoiceScoreGuide = dict[Choice, int]
OutcomeScoreGuide = dict[Outcome, int]

CIPHER: Cipher = {
    "A": Choice.ROCK,
    "B": Choice.PAPER,
    "C": Choice.SCISSORS,
    "X": Choice.ROCK,
    "Y": Choice.PAPER,
    "Z": Choice.SCISSORS,
}

DEFAULT_CHOICE_SCORE_GUIDE: ChoiceScoreGuide = {
    Choice.ROCK: 1,
    Choice.PAPER: 2,
    Choice.SCISSORS: 3,
}

DEFAULT_OUTCOME_SCORE_GUIDE: OutcomeScoreGuide = {
    Outcome.LOSE: 0,
    Outcome.DRAW: 3,
    Outcome.WIN: 6,
}

WINNING_MATCHUPS = {
    (Choice.ROCK, Choice.SCISSORS),
    (Choice.PAPER, Choice.ROCK),
    (Choice.SCISSORS, Choice.PAPER),
}


def read_strategy_guide(file_path: str) -> list[EncryptedStrategy]:
    """Read an encrypted strategy guide from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [tuple(line.strip().split(" ")) for line in file]


def decrypt_strategy(encrypted_strategy: EncryptedStrategy, cipher: Cipher) -> DecryptedStrategy:
    """Decrypt an encrypted strategy using a cipher."""

    return tuple(cipher[move] for move in encrypted_strategy)


def get_outcome(player_choice: Choice, opponent_choice: Choice) -> Outcome:
    """Determine the outcome of a Rock Paper Scissors game."""

    if player_choice == opponent_choice:
        return Outcome.DRAW

    if (player_choice, opponent_choice) in WINNING_MATCHUPS:
        return Outcome.WIN
    
    return Outcome.LOSE


def score_strategy(
    decrypted_strategy: DecryptedStrategy,
    choice_score_guide: ChoiceScoreGuide = DEFAULT_CHOICE_SCORE_GUIDE,
    outcome_score_guide: OutcomeScoreGuide = DEFAULT_OUTCOME_SCORE_GUIDE,
) -> int:
    """Score a strategy based on the choices and outcomes."""

    opponent_choice, player_choice = decrypted_strategy
    outcome = get_outcome(player_choice, opponent_choice)

    return choice_score_guide[player_choice] + outcome_score_guide[outcome]



def main() -> None:
    """Read an encrypted strategy guide from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    encrypted_strategies = read_strategy_guide(file_path)
    print(encrypted_strategies)

    decrypted_strategies = [decrypt_strategy(strategy, CIPHER) for strategy in encrypted_strategies]
    print(decrypted_strategies)

    scores = [score_strategy(strategy) for strategy in decrypted_strategies]
    total_score = sum(scores)
    print(total_score)


if __name__ == "__main__":
    main()