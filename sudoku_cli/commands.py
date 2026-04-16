import re
from sudoku_cli.models import Coord


class Command:
    pass


class PlaceCommand(Command):
    def __init__(self, row: int, col: int, value: int) -> None:
        self.row = row
        self.col = col
        self.value = value


class ClearCommand(Command):
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col


class HintCommand(Command):
    pass


class CheckCommand(Command):
    pass


class QuitCommand(Command):
    pass


class InvalidCommand(Command):
    def __init__(self, reason: str) -> None:
        self.reason = reason


class CommandParser:
    _place_pattern = re.compile(r"^\s*([A-Ia-i])([1-9])\s+([1-9])\s*$")
    _clear_pattern = re.compile(r"^\s*([A-Ia-i])([1-9])\s+clear\s*$", re.IGNORECASE)

    def parse(self, raw_text: str) -> Command:
        text = raw_text.strip()
        if text.lower() == "hint":
            return HintCommand()
        if text.lower() == "check":
            return CheckCommand()
        if text.lower() == "quit":
            return QuitCommand()

        clear_match = self._clear_pattern.match(text)
        if clear_match:
            row, col = self._parse_coord(clear_match.group(1), clear_match.group(2))
            return ClearCommand(row=row, col=col)

        place_match = self._place_pattern.match(text)
        if place_match:
            row, col = self._parse_coord(place_match.group(1), place_match.group(2))
            return PlaceCommand(row=row, col=col, value=int(place_match.group(3)))

        return InvalidCommand("Invalid command format. Use e.g., A3 4, C5 clear, hint, check, quit.")

    def _parse_coord(self, row_char: str, col_char: str) -> Coord:
        row = ord(row_char.upper()) - ord("A")
        col = int(col_char) - 1
        return row, col

