from typing import Callable, Optional

from sudoku_cli.commands import CommandParser
from sudoku_cli.generator import SudokuGenerator
from sudoku_cli.game import SudokuGame
from sudoku_cli.solver import SudokuSolver


def run_cli(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    seed: Optional[int] = None,
    generator: Optional[SudokuGenerator] = None,
) -> None:
    parser = CommandParser()
    generator = generator or SudokuGenerator(seed=seed)

    while True:
        generated = generator.generate()
        game = SudokuGame(generated=generated, solver=SudokuSolver(), seed=seed)

        output_fn("Welcome to Sudoku!\n")
        output_fn("Here is your puzzle:")
        output_fn(game.render_grid())

        while True:
            prompt = "\nEnter command (e.g., A3 4, C5 clear, hint, check, quit):\n"
            raw_command = input_fn(prompt)
            command = parser.parse(raw_command)
            result = game.handle_command(command)
            output_fn(result.message)

            if result.should_quit:
                return

            output_fn("\nCurrent grid:")
            output_fn(game.render_grid())

            if result.puzzle_completed:
                again = input_fn("Press Enter to play again or type 'quit' to exit:\n")
                if again.strip().lower() == "quit":
                    output_fn("Thanks for playing!")
                    return
                break
