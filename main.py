import argparse
from sudoku_cli.cli import run_cli


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sudoku CLI")
    parser.add_argument("--seed", type=int, help="Seed for the random number generator")
    args = parser.parse_args()
    run_cli(seed=args.seed)
