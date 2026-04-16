from sudoku_cli.solver import SudokuSolver
from sudoku_cli.models import Grid


def test_first_violation_prefers_row_violations() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 1
    grid[0][5] = 1
    grid[1][0] = 2
    grid[2][0] = 2

    violation = SudokuSolver().first_violation(grid)

    assert violation is not None
    assert violation.message == "Number 1 already exists in Row A."


def test_first_violation_detects_column_violation() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 7
    grid[4][0] = 7

    violation = SudokuSolver().first_violation(grid)

    assert violation is not None
    assert violation.message == "Number 7 already exists in Column 1."


def test_first_violation_detects_subgrid_violation() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 9
    grid[1][1] = 9

    violation = SudokuSolver().first_violation(grid)

    assert violation is not None
    assert violation.message == "Number 9 already exists in the same 3x3 subgrid."


def test_is_safe_checks_row_column_and_subgrid(solved_grid: Grid) -> None:
    solver = SudokuSolver()
    grid = [row[:] for row in solved_grid]
    grid[0][0] = 0

    assert solver.is_safe(grid, 0, 0, 3) is False
    assert solver.is_safe(grid, 0, 0, 6) is False
    assert solver.is_safe(grid, 0, 0, 9) is False
    assert solver.is_safe(grid, 0, 0, 5) is True


def test_count_solutions_returns_one_and_does_not_mutate_grid(
    solved_grid: Grid,
) -> None:
    solver = SudokuSolver()
    puzzle = [row[:] for row in solved_grid]
    puzzle[0][0] = 0
    expected_after = [row[:] for row in puzzle]

    count = solver.count_solutions(puzzle, limit=2)

    assert count == 1
    assert puzzle == expected_after


def test_count_solutions_returns_zero_when_limit_is_zero(solved_grid: Grid) -> None:
    solver = SudokuSolver()

    count = solver.count_solutions(solved_grid, limit=0)

    assert count == 0


def test_count_solutions_stops_when_limit_reached() -> None:
    solver = SudokuSolver()
    empty_grid = [[0] * 9 for _ in range(9)]

    count = solver.count_solutions(empty_grid, limit=1)

    assert count == 1
