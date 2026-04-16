from dataclasses import dataclass

from sudoku_cli.models import Grid


@dataclass(frozen=True)
class Violation:
    message: str


class SudokuSolver:
    def first_violation(self, grid: Grid) -> Violation | None:
        row_violation = self._row_violation(grid)
        if row_violation:
            return row_violation

        col_violation = self._column_violation(grid)
        if col_violation:
            return col_violation

        return self._subgrid_violation(grid)

    def _row_violation(self, grid: Grid) -> Violation | None:
        for row in range(9):
            seen: set[int] = set()
            for col in range(9):
                value = grid[row][col]
                if value == 0:
                    continue
                if value in seen:
                    return Violation(f"Number {value} already exists in Row {chr(ord('A') + row)}.")
                seen.add(value)
        return None

    def _column_violation(self, grid: Grid) -> Violation | None:
        for col in range(9):
            seen: set[int] = set()
            for row in range(9):
                value = grid[row][col]
                if value == 0:
                    continue
                if value in seen:
                    return Violation(f"Number {value} already exists in Column {col + 1}.")
                seen.add(value)
        return None

    def _subgrid_violation(self, grid: Grid) -> Violation | None:
        for row_start in range(0, 9, 3):
            for col_start in range(0, 9, 3):
                seen: set[int] = set()
                for row in range(row_start, row_start + 3):
                    for col in range(col_start, col_start + 3):
                        value = grid[row][col]
                        if value == 0:
                            continue
                        if value in seen:
                            return Violation(f"Number {value} already exists in the same 3x3 subgrid.")
                        seen.add(value)
        return None
