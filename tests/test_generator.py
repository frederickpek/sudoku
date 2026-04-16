from sudoku_cli.generator import SudokuGenerator
from sudoku_cli.solver import SudokuSolver


def test_generate_returns_consistent_puzzle_and_solution() -> None:
    solver = SudokuSolver()
    clues = 80
    generator = SudokuGenerator(solver=solver, seed=123, clues=clues, max_generation_attempts=5)

    generated = generator.generate()

    nonzero_cells = {
        (row, col)
        for row in range(9)
        for col in range(9)
        if generated.puzzle_grid[row][col] != 0
    }

    assert len(generated.pre_filled) == clues
    assert generated.pre_filled == nonzero_cells
    assert solver.first_violation(generated.solution_grid) is None
    assert solver.count_solutions(generated.puzzle_grid, limit=2) == 1


def test_generate_raises_when_max_attempts_exhausted() -> None:
    generator = SudokuGenerator(solver=SudokuSolver(), seed=123, max_generation_attempts=0)

    try:
        generator.generate()
    except RuntimeError as error:
        assert "Failed to generate a unique Sudoku puzzle" in str(error)
    else:
        raise AssertionError("Expected generator.generate() to raise RuntimeError")


def test_generate_full_solution_raises_when_fill_remaining_fails(monkeypatch) -> None:
    generator = SudokuGenerator(solver=SudokuSolver(), seed=123)

    monkeypatch.setattr(generator, "_fill_remaining", lambda grid: False)

    try:
        generator._generate_full_solution()
    except RuntimeError as error:
        assert "Failed to generate a complete Sudoku grid." in str(error)
    else:
        raise AssertionError("Expected _generate_full_solution() to raise RuntimeError")


def test_carve_unique_solution_grid_restores_cell_and_returns_none(solved_grid: list[list[int]]) -> None:
    generator = SudokuGenerator(solver=SudokuSolver(), seed=123, clues=80)

    def always_multiple_solutions(puzzle, limit=2) -> int:
        return 2

    generator._solver.count_solutions = always_multiple_solutions  # type: ignore[method-assign]

    carved = generator._carve_unique_solution_grid(solved_grid)

    assert carved is None
