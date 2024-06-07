from python_package.preprocessing import Preprocessing
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv

class Sudoku(Preprocessing):
    def __init__(self, sudoku_path: str) -> None:
        super().__init__()
        self.sudoku_size: int
        self.set_tuples: dict[tuple: set] = self.csv_to_set_tuples(sudoku_path)
        self.update_constraints()

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
    
    
    def plot_grid(self, title=None) -> Figure:
        """ Plot the sudoku grid with the current set values"""

        fig, ax = plt.subplots(figsize=(6, 6))
        
        ax.set_xlim(0, self.sudoku_size)
        ax.set_ylim(0, self.sudoku_size)
        
        minor_ticks = range(0, self.sudoku_size + 1)
        major_ticks = range(0, self.sudoku_size + 1, int(self.sudoku_size**0.5))
        
        for tick in minor_ticks:
            ax.plot([tick, tick], [0, self.sudoku_size], 'k', linewidth=0.5)
            ax.plot([0, self.sudoku_size], [tick, tick], 'k', linewidth=0.5)
        
        for tick in major_ticks:
            ax.plot([tick, tick], [0, self.sudoku_size], 'k', linewidth=3)
            ax.plot([0, self.sudoku_size], [tick, tick], 'k', linewidth=3)
            
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add numbers to the grid from the dictionary
        for (i, j), value in self.set_tuples.items():
            ax.text(j + 0.5, self.sudoku_size -0.5 - i, str(next(iter(value))),
                    ha='center', va='center', fontsize=100/self.sudoku_size)
            
        if title:
            plt.title(title, fontsize=20)
        
        plt.close(fig)

        return fig
    