from typing import Optional
from dataclasses import dataclass

from sudoku_cli.models import Coord, Grid


@dataclass(frozen=True)
class Violation:
    message: str


class SudokuSolver:
    def first_violation(self, grid: Grid) -> Optional[Violation]:
        row_violation = self._row_violation(grid)
        if row_violation:
            return row_violation

        col_violation = self._column_violation(grid)
        if col_violation:
            return col_violation

        return self._subgrid_violation(grid)

    def _row_violation(self, grid: Grid) -> Optional[Violation]:
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

    def _column_violation(self, grid: Grid) -> Optional[Violation]:
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

    def _subgrid_violation(self, grid: Grid) -> Optional[Violation]:
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

    def is_safe(self, grid: Grid, row: int, col: int, num: int) -> bool:
        if any(grid[row][idx] == num for idx in range(9)):
            return False
        if any(grid[idx][col] == num for idx in range(9)):
            return False

        row_start = row - row % 3
        col_start = col - col % 3
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if grid[r][c] == num:
                    return False
        return True

    def _find_empty(self, grid: Grid) -> Optional[Coord]:
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return row, col
        return None

    def count_solutions(self, grid: Grid, limit: int = 2) -> int:
        work_grid = [row[:] for row in grid]
        return self._count_solutions_in_place(work_grid, limit=limit, count=0)
    
    def _count_solutions_in_place(self, grid: Grid, limit: int, count: int) -> int:
        if count >= limit:
            return count

        empty = self._find_empty(grid)
        if empty is None:
            return count + 1

        row, col = empty
        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                count = self._count_solutions_in_place(grid, limit, count)
                grid[row][col] = 0
                if count >= limit:
                    break
        return count
