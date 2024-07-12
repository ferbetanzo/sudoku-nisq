

class Preprocessing:
    def __init__(self) -> None:
        self.rows_constraints: dict[tuple: set] = {}
        self.columns_constraints: dict[tuple: set] = {}
        self.subunit_constraints: dict[tuple: set] = {}
        self.open_tuples: dict[tuple: set] = {}
        
    
    def update_constraints(self) -> None:
        """Update the row, column and subunit constraints for each cell given the 
        set values"""

        fixed_tuples = {key: value for key, value in self.open_tuples.items() if len(value) == 1}
        self.set_tuples.update(fixed_tuples)
    
        for row in range(self.sudoku_size):
            for column in range(self.sudoku_size):        
                if (row, column) in self.set_tuples:
                    subunit = (int(row//self.sudoku_size**0.5), int(column//self.sudoku_size**0.5))

                    if row in self.rows_constraints:
                        self.rows_constraints[row].update(self.set_tuples[(row, column)])
                    else:
                        self.rows_constraints[row] = self.set_tuples[(row, column)].copy()
                        
                    if column in self.columns_constraints:
                        self.columns_constraints[column].update(self.set_tuples[(row, column)])
                    else:
                        self.columns_constraints[column] = self.set_tuples[(row, column)].copy()

                    if subunit in self.subunit_constraints:
                        self.subunit_constraints[subunit].update(self.set_tuples[(row, column)])
                    else: 
                        self.subunit_constraints[subunit] = self.set_tuples[(row, column)].copy()


    def find_invalid_values(self, row: int, column: int) -> set:
        """Create a set containing the invalid values for the cell in the specified row
         and column given the row, column and subunit constraints"""

        subunit = (int(row//self.sudoku_size**0.5), int(column//self.sudoku_size**0.5))
        invalid_values = set()
        if row in self.rows_constraints:
            invalid_values = invalid_values | self.rows_constraints[row]
        if column in self.columns_constraints:
            invalid_values = invalid_values | self.columns_constraints[column]
        if subunit in self.subunit_constraints:
            invalid_values = invalid_values | self.subunit_constraints[subunit]

        return invalid_values
    
    def digit_exclusion(self) -> None:
        """Exclude the invalid values from the possible values based on the current constraints"""

        self.open_tuples = {}
        possible_values = set(range(1, self.sudoku_size + 1))

        for row in range(self.sudoku_size):
            for column in range(self.sudoku_size):
                if (row, column) not in self.set_tuples:
        
                    invalid_values = self.find_invalid_values(row=row, column=column)
                    self.open_tuples[(row, column)] = possible_values - invalid_values
                

        
    
    def general_preprocessing(self) -> None:
        """Performs an iteration of the general preprocessing algorithm, finds new set values
        if exist and updates the constraints"""
    
        # Step 1: Digit exclusion
        self.digit_exclusion()

        # Step 2: constraints update
        self.update_constraints()
        

    