import matplotlib.pyplot as plt


class Preprocessing:
    def __init__(self) -> None:
        self.rows_constrictions: dict[tuple: set] = {}
        self.columns_constrictions: dict[tuple: set] = {}
        self.subunit_constrictions: dict[tuple: set] = {}
        self.open_tuples: dict[tuple: set] = {}
        
    
    def update_constrictions(self, fixed_tuples: dict[tuple : int]) -> None:
        """Update the row, column and subunit constrictions for each cell given the 
        fixed values"""
    
        for row in range(self.sudoku_size):
            for column in range(self.sudoku_size):        
                if (row, column) in fixed_tuples:
                    subunit = (int(row//self.sudoku_size**0.5), int(column//self.sudoku_size**0.5))

                    if row in self.rows_constrictions:
                        self.rows_constrictions[row].update(fixed_tuples[(row, column)])
                    else:
                        self.rows_constrictions[row] = fixed_tuples[(row, column)].copy()
                        
                    if column in self.columns_constrictions:
                        self.columns_constrictions[column].update(fixed_tuples[(row, column)])
                    else:
                        self.columns_constrictions[column] = fixed_tuples[(row, column)].copy()

                    if subunit in self.subunit_constrictions:
                        self.subunit_constrictions[subunit].update(fixed_tuples[(row, column)])
                    else: 
                        self.subunit_constrictions[subunit] = fixed_tuples[(row, column)].copy()


    def find_invalid_values(self, row: int, column: int) -> set:
        """Create a set containing the invalid values for the cell in the specified row
         and column given the row, column and subunit constrictions"""

        subunit = (int(row//self.sudoku_size**0.5), int(column//self.sudoku_size**0.5))
        invalid_values = set()
        if row in self.rows_constrictions:
            invalid_values = invalid_values | self.rows_constrictions[row]
        if column in self.columns_constrictions:
            invalid_values = invalid_values | self.columns_constrictions[column]
        if subunit in self.subunit_constrictions:
            invalid_values = invalid_values | self.subunit_constrictions[subunit]

        return invalid_values
    
    
    def general_preprocessing(self) -> None:
        """Performs an iteration of the general preprocessing algorithm, finds new set values
        if exist and updates the constrictions"""
    
        self.update_constrictions(fixed_tuples=self.set_tuples)

        possible_values = set(range(1, self.sudoku_size + 1))

        for row in range(self.sudoku_size):
            for column in range(self.sudoku_size):
                if (row, column) not in self.set_tuples:
        
                    invalid_values = self.find_invalid_values(row=row, column=column)
                    self.open_tuples[(row, column)] = possible_values - invalid_values
        
        fixed_tuples = {key: value for key, value in self.open_tuples.items() if len(value) == 1}
        self.set_tuples.update(fixed_tuples)

    def plot_sudoku_grid(self) -> None:

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

        plt.show()