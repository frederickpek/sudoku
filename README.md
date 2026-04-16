# Sudoku CLI

A Command-line Sudoku game with puzzle generation and validation.

## Environment

- Python 3.10+ (tested on Linux)

## Features

- Generates a full Sudoku board randomly
- Removes 51 cells while preserving exactly one solution.
- Starts each game with 30 pre-filled cells (`_` for empties).
- Supports commands:
  - `B3 7` (place number)
  - `C5 clear` (clear user cell)
  - `hint` (reveal one correct value)
  - `check` (validate duplicate-rule violations)
  - `quit` (exits the application)
- Prevents editing/clearing original revealed cells.

## Setup

Enter project root.

```bash
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run The Game

```bash
python main.py
```

To generate the same puzzle again for debugging or sharing, pass a seed:

```bash
python main.py -s 123
```

## Run Tests

```bash
pytest
```
