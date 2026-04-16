from sudoku_cli.models import Board


def test_board_properties_return_copies() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    pre_filled = {(0, 0)}
    board = Board(grid, pre_filled)

    copied_grid = board.grid
    copied_prefilled = board.pre_filled
    copied_grid[0][0] = 9
    copied_prefilled.clear()

    assert board.get(0, 0) == 5
    assert board.is_pre_filled(0, 0)


def test_set_and_clear_user_values_respect_prefilled() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    board = Board(grid, {(0, 0)})

    assert board.set_user_value(0, 0, 9) is False
    assert board.clear_user_value(0, 0) is False

    assert board.set_user_value(0, 1, 4) is True
    assert board.get(0, 1) == 4
    assert board.clear_user_value(0, 1) is True
    assert board.get(0, 1) == 0


def test_editable_empty_cells_excludes_prefilled_and_filled_cells() -> None:
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    grid[0][1] = 3
    board = Board(grid, {(0, 0), (0, 1)})
    board.set_user_value(0, 2, 7)

    empties = board.editable_empty_cells()

    assert (0, 0) not in empties
    assert (0, 1) not in empties
    assert (0, 2) not in empties
    assert (1, 1) in empties
