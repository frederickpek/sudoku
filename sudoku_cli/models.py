Grid = list[list[int]]
Coord = tuple[int, int]


class Board:
    def __init__(self, grid: Grid, pre_filled: set[Coord]) -> None:
        self._grid: Grid = [row[:] for row in grid]
        self._pre_filled: set[Coord] = set(pre_filled)

    @property
    def grid(self) -> Grid:
        return [row[:] for row in self._grid]

    @property
    def pre_filled(self) -> set[Coord]:
        return set[Coord](self._pre_filled)

    def get(self, row: int, col: int) -> int:
        return self._grid[row][col]

    def is_pre_filled(self, row: int, col: int) -> bool:
        return (row, col) in self._pre_filled

    def set_user_value(self, row: int, col: int, value: int) -> bool:
        if self.is_pre_filled(row, col):
            return False
        self._grid[row][col] = value
        return True

    def clear_user_value(self, row: int, col: int) -> bool:
        if self.is_pre_filled(row, col):
            return False
        self._grid[row][col] = 0
        return True

    def editable_empty_cells(self) -> list[Coord]:
        cells: list[Coord] = []
        for row in range(9):
            for col in range(9):
                if self._grid[row][col] == 0 and not self.is_pre_filled(row, col):
                    cells.append((row, col))
        return cells
