from typing import Callable, Optional

from sudoku_cli.commands import CommandParser
from sudoku_cli.generator import SudokuGenerator



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

        output_fn("Welcome to Sudoku!\n")
        output_fn("Here is your puzzle:")
        output_fn(generated.puzzle_grid)

        while True:
            prompt = "\nEnter command (e.g., A3 4, C5 clear, hint, check, quit): "
            raw_command = input_fn(prompt)
            command = parser.parse(raw_command)
            # handle command

            # check if should quit or if puzzle done

            output_fn("\nCurrent grid:")
            output_fn(generated.puzzle_grid)

