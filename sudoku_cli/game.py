from dataclasses import dataclass

from sudoku_cli.commands import (
    CheckCommand,
    ClearCommand,
    Command,
    HintCommand,
    InvalidCommand,
    PlaceCommand,
    QuitCommand,
)
from sudoku_cli.models import Board, Coord
from sudoku_cli.generator import GeneratedPuzzle
from sudoku_cli.solver import SudokuSolver, Violation

@dataclass(frozen=True)
class GameResult:
    message: str
    should_quit: bool = False
    puzzle_completed: bool = False


class SudokuGame:
    def __init__(self, generated: GeneratedPuzzle, solver: SudokuSolver) -> None:
        self._board = Board(generated.puzzle_grid, generated.pre_filled)
        self._solution = [row[:] for row in generated.solution_grid]
        self._solver = solver

    def handle_command(self, command: Command) -> GameResult:
        if isinstance(command, QuitCommand):
            return GameResult("Thanks for playing!", should_quit=True)
        if isinstance(command, PlaceCommand):
            return self._handle_place(command.row, command.col, command.value)
        if isinstance(command, ClearCommand):
            return self._handle_clear(command.row, command.col)
        if isinstance(command, CheckCommand):
            return self._handle_check()
        if isinstance(command, HintCommand):
            return self._handle_hint()
        if isinstance(command, InvalidCommand):
            return GameResult(command.reason)
        return GameResult("Unknown command.")

    def render_grid(self) -> str:
        header = "    " + " ".join(str(col) for col in range(1, 10))
        rows = [header]
        for row in range(9):
            row_label = chr(ord("A") + row)
            rendered_values: list[str] = []
            for col in range(9):
                value = self._board.get(row, col)
                if value == 0:
                    token = " _"
                else:
                    token = f" {value}"
                rendered_values.append(token)
            rows.append(f"  {row_label}" + "".join(rendered_values))
        return "\n".join(rows)

    def _handle_place(self, row: int, col: int, value: int) -> GameResult:
        coord = self._coord_label((row, col))
        if self._board.is_pre_filled(row, col):
            return GameResult(f"Invalid move. {coord} is pre-filled.")

        self._board.set_user_value(row, col, value)
        if self._is_completed():
            return GameResult("You have successfully completed the Sudoku puzzle!", puzzle_completed=True)

        # same msg for updating value
        return GameResult("Move accepted.")

    def _handle_clear(self, row: int, col: int) -> GameResult:
        coord = self._coord_label((row, col))
        if self._board.is_pre_filled(row, col):
            return GameResult(f"Invalid move. {coord} is pre-filled.")
        self._board.clear_user_value(row, col)
        return GameResult(f"Cell {coord} cleared.")

    def _handle_check(self) -> GameResult:
        violation = self._solver.first_violation(self._board.grid)
        if not violation:
            return GameResult("No rule violations detected.")
        return GameResult(violation.message)

    def _handle_hint(self) -> GameResult:
        return GameResult("Hint not implemented.")

    def _is_completed(self) -> bool:
        return self._board.grid == self._solution

    def _coord_label(self, coord: Coord) -> str:
        row, col = coord
        return f"{chr(ord('A') + row)}{col + 1}"

