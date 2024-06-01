import csv

# Fill with zeros the empty cells and with the corresponding value the preset cells
# 9x9 grid
# preset_grid =  [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 9, 0, 0]
# ]

# 4x4 grid
preset_grid = [
    [1, 0, 0, 0],
    [0, 4, 0, 0],
    [0, 2, 0, 0],
    [3, 0, 0, 0]
]
  
# Save the sudoku in a csv format
with open('./data/4x4sudoku.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(preset_grid)