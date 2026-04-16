import random
from typing import Optional
from dataclasses import dataclass

from sudoku_cli.models import Coord, Grid
from sudoku_cli.solver import SudokuSolver


@dataclass(frozen=True)
class GeneratedPuzzle:
    puzzle_grid: Grid
    solution_grid: Grid
    pre_filled: set[Coord]


class SudokuGenerator:
    def __init__(self, solver: SudokuSolver, seed: Optional[int] = None, clues: int = 30, max_generation_attempts: int = 30) -> None:
        self._random = random.Random(seed)
        self._clues = clues
        self._solver = solver
        self._max_generation_attempts = max_generation_attempts

    def generate(self) -> GeneratedPuzzle:
        for _ in range(self._max_generation_attempts):
            solution = self._generate_full_solution()
            puzzle = self._carve_unique_solution_grid(solution)
            if puzzle is not None:
                pre_filled = {
                    (row, col)
                    for row in range(9)
                    for col in range(9)
                    if puzzle[row][col] != 0
                }
                return GeneratedPuzzle(
                    puzzle_grid=[row[:] for row in puzzle],
                    solution_grid=[row[:] for row in solution],
                    pre_filled=pre_filled,
                )
        raise RuntimeError(f"Failed to generate a unique Sudoku puzzle after multiple attempts.")

    def _generate_full_solution(self) -> Grid:
        grid: Grid = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_diagonal_boxes(grid)
        if not self._fill_remaining(grid):
            raise RuntimeError("Failed to generate a complete Sudoku grid.")
        return grid

    def _fill_diagonal_boxes(self, grid: Grid) -> None:
        for idx in range(0, 9, 3):
            self._fill_box(grid, idx, idx)

    def _fill_box(self, grid: Grid, row_start: int, col_start: int) -> None:
        numbers = list(range(1, 10))
        self._random.shuffle(numbers)
        pointer = 0
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                grid[row][col] = numbers[pointer]
                pointer += 1

    def _fill_remaining(self, grid: Grid) -> bool:
        empty = self._find_empty(grid)
        if empty is None:
            return True

        row, col = empty
        numbers = list(range(1, 10))
        self._random.shuffle(numbers)
        for num in numbers:
            if self._solver.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self._fill_remaining(grid):
                    return True
                grid[row][col] = 0
        return False

    def _find_empty(self, grid: Grid) -> Optional[Coord]:
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return row, col
        return None

    def _carve_unique_solution_grid(self, grid: Grid) -> Optional[Grid]:
        puzzle = [row[:] for row in grid]
        cells = [(row, col) for row in range(9) for col in range(9)]
        self._random.shuffle(cells)

        target_remove = 81 - self._clues
        removed = 0

        for row, col in cells:
            if removed >= target_remove:
                break

            backup = puzzle[row][col]
            puzzle[row][col] = 0
            solutions = self._solver.count_solutions(puzzle, limit=2)
            if solutions == 1:
                removed += 1
            else:
                puzzle[row][col] = backup

        if removed == target_remove:
            return puzzle
        return None

