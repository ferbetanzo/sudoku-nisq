# import Sudoku

# board = Sudoku.Board(
#     unit_height=2, unit_width=2,
#     grid_height=1, grid_width=2,
#     init_value=-1
#     )

# board.update_board([1, 1, 1, 1, 1, 1, 1],
#                    [(0, 0), (0, 1), (0, 2), (0, 3),
#                     (1, 0), (1, 1), (1, 3)])

# board.print_board()

# print(board.get_open_indexed_tuples())

from Grover import Grover as gr

tuples = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
field_values = {0:0, 1:1}
grover = gr(tuples=tuples, field_values=field_values, 
                subunit_height=2, subunit_width=2)

grover.print_circuit()
result = grover.run_circuit()
print(result)