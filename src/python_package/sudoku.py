from python_package.preprocessing import Preprocessing
import csv

class Sudoku(Preprocessing):
    def __init__(self, sudoku_path: str) -> None:
        super().__init__()
        self.sudoku_size: int
        self.set_tuples: dict[tuple: set] = self.csv_to_set_tuples(sudoku_path)

    def csv_to_set_tuples(self, filename:str) -> dict[tuple: int]:
        """Create a dictionary containing the preset values of the sudoku and initialize
        the sudoku size"""

        set_tuples = {}
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            counter = 0
            for i, row in enumerate(reader):
                counter += 1
                for j, value in enumerate(row):
                    if value != "0":
                        set_tuples[(i, j)] = {int(value)}
            
        self.sudoku_size = counter

        return set_tuples
