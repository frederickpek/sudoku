from sudoku_cli.generator import SudokuGenerator

generator = SudokuGenerator()
generated_puzzle = generator.generate()

for row in generated_puzzle.puzzle_grid:
    print(row)
print()
for row in generated_puzzle.solution_grid:
    print(row)
print()
for coord in generated_puzzle.pre_filled:
    print(coord)
