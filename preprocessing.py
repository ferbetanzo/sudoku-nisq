size=3

## Find pre-filled cells
def pre_tuples(sudoku):
   preset_tuples = []
   for i in range(size*size):  # Loop over each row
       for j in range(size*size):  # Loop over each column in the row
           element = sudoku[i][j]
           if element is not None: # Check if the cell is pre-filled
               preset_tuples.append((i,j,element)) # Store pre-filled cell as tuple
   return preset_tuples

## Find open cells and store them in tuples
def find_open_tuples(sudoku):
   open_tuple = []
   for i in range(size*size):  # Loop over each row
       for j in range(size*size):  # Loop over each column in the row
           element = sudoku[i][j]
           if element is None: # Check if the cell is empty
               digits = list(range(1, size*size +1)) # Possible digits for the cell
               # Discard digits based on the column constraint
               for p in range(size*size):
                   if sudoku[p][j] is not None and sudoku[p][j] in digits:
                       digits.remove(sudoku[p][j])
               # Discard digits based on the row constraint
               for q in range(size*size):
                   if sudoku[i][q] is not None and sudoku[i][q] in digits:
                       digits.remove(sudoku[i][q])
               # Discard digits based on the subfield
               subgrid_row_start = size * (i // size)
               subgrid_col_start = size * (j // size)
               for x in range(subgrid_row_start, subgrid_row_start + size):
                   for y in range(subgrid_col_start, subgrid_col_start + size):
                       if sudoku[x][y] is not None and sudoku[x][y] in digits:
                           digits.remove(sudoku[x][y])

               # Store a tuple for each remaining possibility for the given cell
               for digit in digits:
                   open_tuple.append((i, j, digit))
   return open_tuple

## Find tuples that have unique assignments
def fix_tuples(open_tuples):
    # Create dictionary to count occurrences of each cell position with potential digits
    count_dict = {}
    # Count each cell's possible digits
    for tup in open_tuples:
        key = (tup[0], tup[1])  # Use cell position as key
        if key in count_dict:
            count_dict[key].append(tup)
        else:
            count_dict[key] = [tup]
    # Collect only those cell positions with a single possible digit
    fixed_tuples = []
    for key, value in count_dict.items():
        if len(value) == 1:
            fixed_tuples.extend(value)
    return fixed_tuples

## Use the previous functions to find and fill all trivially solvable cells
def preprocess(puzzle):
    # Process to reduce possible digits for each cell
    open_tuples = find_open_tuples(puzzle.board)
    fixed_tuples = fix_tuples(open_tuples)
    # Keep processing while there are cells with a single possible digit
    while len(fixed_tuples) != 0:
        for tuple in fixed_tuples:
            i, j, digit = tuple  # Extract row, column, and digit
            puzzle.board[i][j] = digit  # Set digit on the board
        # Recalculate possible digits after setting known digits
        open_tuples = find_open_tuples(puzzle.board)
        fixed_tuples = fix_tuples(open_tuples)
        #puzzle.show()  # Display the board state
    return puzzle
