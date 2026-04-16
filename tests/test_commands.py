from sudoku_cli.commands import (
    CheckCommand,
    ClearCommand,
    CommandParser,
    HintCommand,
    InvalidCommand,
    PlaceCommand,
    QuitCommand,
)


def test_parse_place_command() -> None:
    command = CommandParser().parse("A3 4")

    assert isinstance(command, PlaceCommand)
    assert command.row == 0
    assert command.col == 2
    assert command.value == 4


def test_parse_clear_command_case_insensitive() -> None:
    command = CommandParser().parse(" c5 CLEAR ")

    assert isinstance(command, ClearCommand)
    assert command.row == 2
    assert command.col == 4


def test_parse_keyword_commands() -> None:
    parser = CommandParser()

    assert isinstance(parser.parse("hint"), HintCommand)
    assert isinstance(parser.parse("CHECK"), CheckCommand)
    assert isinstance(parser.parse("Quit"), QuitCommand)


def test_parse_invalid_command() -> None:
    command = CommandParser().parse("Z9 1")

    assert isinstance(command, InvalidCommand)
    assert "Invalid command format" in command.reason

    assert isinstance(CommandParser().parse(""), InvalidCommand)
    assert isinstance(CommandParser().parse("hint."), InvalidCommand)
    assert isinstance(CommandParser().parse("??"), InvalidCommand)
    assert isinstance(CommandParser().parse("oqwieuj"), InvalidCommand)
    assert isinstance(CommandParser().parse(" "), InvalidCommand)
