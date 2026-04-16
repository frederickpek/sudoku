from sudoku_cli.cli import run_cli
from sudoku_cli.commands import CheckCommand, ClearCommand, Command, HintCommand, InvalidCommand, PlaceCommand
from sudoku_cli.game import SudokuGame
from sudoku_cli.generator import GeneratedPuzzle
from sudoku_cli.solver import SudokuSolver
from sudoku_cli.models import Coord, Grid


def _generated_from_solution(
    solution: Grid, blank_cells: set[Coord]
) -> GeneratedPuzzle:
    puzzle = [row[:] for row in solution]
    for row, col in blank_cells:
        puzzle[row][col] = 0
    pre_filled = {
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle[row][col] != 0
    }
    return GeneratedPuzzle(puzzle_grid=puzzle, solution_grid=[row[:] for row in solution], pre_filled=pre_filled)


def test_place_on_prefilled_cell_is_rejected(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    result = game.handle_command(PlaceCommand(0, 0, 9))

    assert result.message == "Invalid move. A1 is pre-filled."
    assert result.puzzle_completed is False


def test_place_can_complete_puzzle(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    result = game.handle_command(PlaceCommand(0, 1, solved_grid[0][1]))

    assert result.message == "You have successfully completed the Sudoku puzzle!"
    assert result.puzzle_completed is True


def test_check_reports_no_violations_for_valid_partial_grid(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1), (1, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    result = game.handle_command(CheckCommand())

    assert result.message == "No rule violations detected."


def test_check_reports_violation_message(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1), (1, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)
    game.handle_command(PlaceCommand(0, 1, 5))

    result = game.handle_command(CheckCommand())

    assert "already exists in Row A." in result.message


def test_hint_rejected_when_there_is_violation(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1), (1, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)
    game.handle_command(PlaceCommand(0, 1, 5))

    result = game.handle_command(HintCommand())

    assert result.message == "Hint: There exists a violation."


def test_hint_when_single_empty_cell(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    result = game.handle_command(HintCommand())

    assert result.message == "Hint: You don't need a hint for this one!"


def test_hint_fills_one_of_multiple_empty_cells(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1), (1, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)
    before = game.render_grid().count("_")

    result = game.handle_command(HintCommand())
    after = game.render_grid().count("_")

    assert result.message.startswith("Hint: Cell ")
    assert after == before - 1


def test_hint_when_no_empty_cells_available(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells=set())
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    result = game.handle_command(HintCommand())

    assert result.message == "Hint: No empty cells available."


def test_clear_command_branches(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    prefilled_result = game.handle_command(ClearCommand(0, 0))
    editable_result = game.handle_command(ClearCommand(0, 1))

    assert prefilled_result.message == "Invalid move. A1 is pre-filled."
    assert editable_result.message == "Cell A2 cleared."


def test_invalid_and_unknown_commands(solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})
    game = SudokuGame(generated, solver=SudokuSolver(), seed=0)

    invalid_result = game.handle_command(InvalidCommand("bad input"))
    unknown_result = game.handle_command(Command())

    assert invalid_result.message == "bad input"
    assert unknown_result.message == "Unknown command."


def test_run_cli_quit_flow(monkeypatch, solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1), (1, 1)})

    def fake_generate(self) -> GeneratedPuzzle:
        return generated

    monkeypatch.setattr("sudoku_cli.cli.SudokuGenerator.generate", fake_generate)

    prompts: list[str] = []
    outputs: list[str] = []
    inputs = iter(["quit"])

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(inputs)

    run_cli(input_fn=fake_input, output_fn=outputs.append, seed=10)

    assert prompts
    assert any("Enter command" in prompt for prompt in prompts)
    assert outputs[0].startswith("Welcome to Sudoku!")
    assert outputs[-1] == "Thanks for playing!"


def test_run_cli_complete_puzzle_then_quit(monkeypatch, solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})

    def fake_generate(self) -> GeneratedPuzzle:
        return generated

    monkeypatch.setattr("sudoku_cli.cli.SudokuGenerator.generate", fake_generate)

    prompts: list[str] = []
    outputs: list[str] = []
    inputs = iter(["A2 3", "quit"])

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(inputs)

    run_cli(input_fn=fake_input, output_fn=outputs.append, seed=10)

    assert any("Enter command" in prompt for prompt in prompts)
    assert any("Press Enter to play again" in prompt for prompt in prompts)
    assert "You have successfully completed the Sudoku puzzle!" in outputs
    assert "\nCurrent grid:" in outputs
    assert outputs[-1] == "Thanks for playing!"


def test_run_cli_complete_puzzle_then_play_again(monkeypatch, solved_grid: Grid) -> None:
    generated = _generated_from_solution(solved_grid, blank_cells={(0, 1)})

    def fake_generate(self) -> GeneratedPuzzle:
        return generated

    monkeypatch.setattr("sudoku_cli.cli.SudokuGenerator.generate", fake_generate)

    prompts: list[str] = []
    outputs: list[str] = []
    inputs = iter(["A2 3", "", "quit"])

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(inputs)

    run_cli(input_fn=fake_input, output_fn=outputs.append, seed=10)

    assert any("Press Enter to play again" in prompt for prompt in prompts)
    assert outputs.count("Welcome to Sudoku!\n") == 2
    assert outputs[-1] == "Thanks for playing!"
