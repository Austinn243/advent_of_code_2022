"""
Advent of Code 2022, Day 2
Rock Paper Scissors
https://adventofcode.com/2022/day/2
"""

from collections.abc import Callable
from enum import IntEnum
from os import path
from typing import NamedTuple

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


class EncryptedStrategy(NamedTuple):
    """An encrypted strategy for Rock Paper Scissors."""

    opponent_move: str
    player_outcome: str


DecryptedStrategy = tuple[Choice, Choice]
ChoiceScoreGuide = dict[Choice, int]
OutcomeScoreGuide = dict[Outcome, int]

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
        return [parse_encrypted_strategy(line.strip()) for line in file]


def parse_encrypted_strategy(line: str) -> EncryptedStrategy:
    """Parse an encrypted strategy from a line of text."""

    opponent_move, player_outcome = line.split()

    return EncryptedStrategy(opponent_move, player_outcome)


def get_opponent_choice(opponent_move: str) -> Choice:
    """Get the opponent's choice from an encrypted move."""

    match opponent_move:
        case "A":
            return Choice.ROCK
        case "B":
            return Choice.PAPER
        case "C":
            return Choice.SCISSORS
        case _:
            raise ValueError(f"Invalid opponent move: {opponent_move}")


def get_assumed_player_choice(encrypted_strategy: EncryptedStrategy) -> Choice:
    """Get the player's choice based on the player's original assumption."""

    player_outcome = encrypted_strategy.player_outcome

    match player_outcome:
        case "X":
            return Choice.ROCK
        case "Y":
            return Choice.PAPER
        case "Z":
            return Choice.SCISSORS
        case _:
            raise ValueError(f"Invalid player outcome: {player_outcome}")


def get_desired_outcome(player_outcome: str) -> Outcome:
    """Determine the desired outcome of the round."""

    match player_outcome:
        case "X":
            return Outcome.LOSE
        case "Y":
            return Outcome.DRAW
        case "Z":
            return Outcome.WIN
        case _:
            raise ValueError(f"Invalid player outcome: {player_outcome}")


def get_player_choice_by_desired_outcome(
    encrypted_strategy: EncryptedStrategy,
) -> Choice:
    """Get the player's choice based on the desired outcome."""

    desired_outcome = get_desired_outcome(encrypted_strategy.player_outcome)
    opponent_choice = get_opponent_choice(encrypted_strategy.opponent_move)

    if desired_outcome == Outcome.DRAW:
        return opponent_choice

    if desired_outcome == Outcome.WIN:
        return next(
            winning_choice
            for winning_choice, losing_choice in WINNING_MATCHUPS
            if losing_choice == opponent_choice
        )

    return next(
        losing_choice
        for winning_choice, losing_choice in WINNING_MATCHUPS
        if winning_choice == opponent_choice
    )


def decrypt_strategy(
    encrypted_strategy: EncryptedStrategy,
    get_player_choice: Callable[[EncryptedStrategy], Choice],
) -> DecryptedStrategy:
    """Decrypt an encrypted strategy using a cipher."""

    opponent_choice = get_opponent_choice(encrypted_strategy.opponent_move)
    player_choice = get_player_choice(encrypted_strategy)

    return (opponent_choice, player_choice)


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

    assumed_strategies = [
        decrypt_strategy(strategy, get_assumed_player_choice)
        for strategy in encrypted_strategies
    ]
    assumed_scores = [score_strategy(strategy) for strategy in assumed_strategies]
    total_score = sum(assumed_scores)
    print("While working under initial assumptions:")
    print(f"The total score is: {total_score}")
    print()

    desired_strategies = [
        decrypt_strategy(strategy, get_player_choice_by_desired_outcome)
        for strategy in encrypted_strategies
    ]
    desired_scores = [score_strategy(strategy) for strategy in desired_strategies]
    total_score = sum(desired_scores)
    print("While working under the actual desired outcomes:")
    print(f"The total score is: {total_score}")


if __name__ == "__main__":
    main()
