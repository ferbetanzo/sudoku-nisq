from sudoku import Sudoku
from preprocessing import pre_tuples, find_open_tuples, preprocess
from preprocessing import size

puzzle = Sudoku(size,seed=100).difficulty(0.62)

print("Original tuple:")
puzzle.show()

preprocess(puzzle)
print("Preprocessed tuple:")
puzzle.show()

preset_tuples = pre_tuples(puzzle.board)
open_tuples = find_open_tuples(puzzle.board)
print(f"Preset tuples: {preset_tuples}")
print(f"Open tuples: {open_tuples}")