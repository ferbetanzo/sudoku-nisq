import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_sudoku_grid(sudoku_data, size=9, title="Sudoku Grid"):
    """
    Draw a Sudoku grid with colored cells and numbers.

    Args:
        sudoku_data (list): A list of tuples where each tuple contains (row, column, value).
                            Represents the Sudoku grid with filled values.
        size (int, optional): Size of the Sudoku grid. Defaults to 9 (9x9 grid).
        title (str, optional): Title for the plot. Defaults to "Sudoku Grid".

    Returns:
        None

    Raises:
        ValueError: If any tuple in sudoku_data has coordinates (row, column) that exceed size.

    Draws a Sudoku grid with specified numbers and colors each cell based on the Sudoku value.
    Empty cells are white, and filled cells are colored based on a predefined color map.
    """
    
    # Check if any tuple in sudoku_data has invalid coordinates
    for item in sudoku_data:
        row, col, _ = item
        if row >= size or col >= size:
            raise ValueError(f"Invalid coordinates ({row}, {col}) for grid size {size}.")
    
    # Define the color map for each number
    number_colors = {
        1: '#FF6666', 2: '#66B2FF', 3: '#66FF66', 4: '#FFFF66',
        5: '#FF99FF', 6: '#B3B3B3', 7: '#FFD966', 8: '#66FFFF', 9: '#66FFCC'
    }
    
    # Adjust dimensions based on size
    figsize = (size, size)
    grid_range = range(size + 1)
    text_fontsize = 18 if size == 9 else 12
    
    # Create the base Sudoku grid
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set background color
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#F0F0F0')
    
    # Draw the grid
    for i in grid_range:
        line_width = 3 if i % int(size ** 0.5) == 0 else 1
        ax.plot([i, i], [0, size], color='black', linewidth=line_width)
        ax.plot([0, size], [i, i], color='black', linewidth=line_width)
    
    # Fill the grid with the provided numbers and colors
    for i in range(size):
        for j in range(size):
            cell_value = 0  # Default value for empty cells
            for item in sudoku_data:
                if item[0] == i and item[1] == j:
                    cell_value = item[2]
                    break
            # Set the color based on the value
            if cell_value == 0:
                cell_color = 'white'  # White for empty cells
            else:
                cell_color = number_colors.get(cell_value, 'white')  # Default to white if not in color map
            rect = patches.Rectangle((j, size - 1 - i), 1, 1, linewidth=0, edgecolor='none', facecolor=cell_color)
            ax.add_patch(rect)
            if cell_value != 0:
                ax.text(j + 0.5, size - 1 - i + 0.5, str(cell_value), ha='center', va='center', fontsize=text_fontsize, fontweight='bold', color='black')
    
    # Draw the outer border
    outer_border = patches.Rectangle((0, 0), size, size, linewidth=3.5, edgecolor='black', facecolor='none')
    ax.add_patch(outer_border)
    
    # Set title
    plt.title(title, fontsize=24, fontweight='bold', color='darkblue')
    
    # Remove axes and show the plot
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


''' Usage examples

# Draw a 4x4 Sudoku grid
sudoku_data_4x4 = [
    (0, 0, 2), (0, 1, 0), (0, 2, 3), (0, 3, 0),
    (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0),
    (2, 0, 0), (2, 1, 3), (2, 2, 0), (2, 3, 0),
    (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)
]
draw_sudoku_grid(sudoku_data_4x4, size=4, title="4x4 Sudoku Grid")

# Draw a default 9x9 Sudoku grid
sudoku_data_9x9 = [
    (0, 0, 5), (0, 1, 3), (0, 4, 7),
    (1, 0, 6), (1, 3, 1), (1, 4, 9), (1, 5, 5),
    (2, 1, 9), (2, 2, 8), (2, 7, 6),
    (3, 0, 8), (3, 4, 6), (3, 8, 3),
    (4, 0, 4), (4, 3, 8), (4, 5, 3), (4, 8, 1),
    (5, 0, 7), (5, 4, 2), (5, 8, 6),
    (6, 1, 6), (6, 6, 2), (6, 7, 8),
    (7, 3, 4), (7, 4, 1), (7, 5, 9), (7, 8, 5),
    (8, 4, 8), (8, 7, 7), (8, 8, 9)
]
draw_sudoku_grid(sudoku_data_9x9, title="9x9 Sudoku Grid")
'''

def generate_sudoku_bitstrings(preset_values, grid_size=9):
    """
    Generates bitstring representations of preset values in a Sudoku grid.

    Args:
        preset_values (list): A list of tuples where each tuple contains (row, column, value).
                              Represents preset values in the Sudoku grid.
        grid_size (int, optional): Size of the Sudoku grid. Defaults to 9.

    Returns:
        dict: A dictionary where keys are numbers 1 to grid_size and values are bitstrings 
              representing their positions. Each bitstring is a string of '0's and '1's 
              of length grid_size^2.

    Raises:
        ValueError: If any tuple in preset_values has coordinates (row, column) that exceed grid_size,
                    or if any value is greater than grid_size.

    Note:
        Generates bitstring representations for each number (1 to grid_size) based on its positions 
        in the Sudoku grid. Each position is marked with '1' in the bitstring, with '0' for empty positions.

    Usage:
        # Example for a 9x9 Sudoku grid
        preset_values_9x9 = [
            (0, 0, 5), (0, 1, 3), (0, 4, 7),
            (1, 0, 6), (1, 3, 1), (1, 4, 9), (1, 5, 5),
            (2, 1, 9), (2, 2, 8), (2, 7, 6),
            (3, 0, 8), (3, 4, 6), (3, 8, 3),
            (4, 0, 4), (4, 3, 8), (4, 5, 3), (4, 8, 1),
            (5, 0, 7), (5, 4, 2), (5, 8, 6),
            (6, 1, 6), (6, 6, 2), (6, 7, 8),
            (7, 3, 4), (7, 4, 1), (7, 5, 9), (7, 8, 5),
            (8, 4, 8), (8, 7, 7), (8, 8, 9)
        ]
        bitstrings_9x9 = generate_sudoku_bitstrings(preset_values_9x9)

        # Example for a 4x4 Sudoku grid
        preset_values_4x4 = [
            (0, 0, 2), (0, 2, 3),
            (2, 1, 3)
        ]
        bitstrings_4x4 = generate_sudoku_bitstrings(preset_values_4x4, grid_size=4)
    """
    
    # Check if any tuple in preset_values has invalid coordinates or values for the given grid_size
    for row, col, value in preset_values:
        if row >= grid_size or col >= grid_size or value > grid_size:
            raise ValueError(f"Invalid input: ({row}, {col}, {value}) for grid size {grid_size}.")
    
    # Initialize a dictionary to store bitstrings for numbers 1 to grid_size
    bitstrings_dict = {num: ['0'] * (grid_size ** 2) for num in range(1, grid_size + 1)}
    
    # Populate bitstrings based on preset_values
    for row, col, value in preset_values:
        index = row * grid_size + col
        bitstrings_dict[value][index] = '1'
    
    # Convert list of '0's and '1's to a single bitstring for each number
    return {num: ''.join(bitstring) for num, bitstring in bitstrings_dict.items()}



def decode_sudoku_bitstrings(bitstrings_dict, grid_size=9):
    """
    Decodes bitstring representations back into a list of tuples representing preset values in a Sudoku grid.

    Args:
        bitstrings_dict (dict): A dictionary where keys are numbers 1 to 9 and values are bitstrings.
                                Each bitstring represents the positions of the number in the Sudoku grid.
        grid_size (int, optional): Size of the Sudoku grid. Defaults to 9.

    Returns:
        list: A list of tuples where each tuple contains (row, column, value).
              Represents preset values in the Sudoku grid based on the bitstring representations.

    Raises:
        ValueError: If the length of any bitstring in bitstrings_dict does not match grid_size squared.

    Decodes bitstring representations for numbers 1 to 9 back into tuples (row, column, value).
    """
    
    # Check if all bitstrings have the correct length
    for num, bitstring in bitstrings_dict.items():
        if len(bitstring) != grid_size ** 2:
            raise ValueError(f"Bitstring length mismatch for number {num}. Expected {grid_size**2}, got {len(bitstring)}.")
    
    preset_values = []
    
    # Iterate through each number (1 to 9) in the bitstrings_dict
    for num, bitstring in bitstrings_dict.items():
        # Iterate through each position in the bitstring
        for index, bit in enumerate(bitstring):
            if bit == '1':
                # Calculate row and column from index
                row = index // grid_size
                col = index % grid_size
                # Add tuple (row, column, number) to preset_values
                preset_values.append((row, col, num))
    
    return preset_values

''' Usage Examples

# Example bitstring dictionary for a 4x4 Sudoku grid
bitstrings_dict_4x4 = {
    1: '00010000',
    2: '00000010',
    3: '00001000',
    4: '00000100'
}

# Generate preset values from the bitstring dictionary
preset_values_4x4 = decode_sudoku_bitstrings(bitstrings_dict_4x4, grid_size=4)

'''


def draw_4x4_sudoku_grid_bs(sudoku_data):
    # Define the color map for each number
    color_map = {
        1: '#FF6666', 2: '#66B2FF', 3: '#66FF66', 4: '#FFFF66'
    }
    
    # Create the base 4x4 grid
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Set background color
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#F0F0F0')
    
    # Draw the grid
    for i in range(5):
        line_width = 3 if i % 2 == 0 else 1
        ax.plot([i, i], [0, 4], color='black', linewidth=line_width)
        ax.plot([0, 4], [i, i], color='black', linewidth=line_width)
    
    # Initialize a 4x4 grid with zeroes
    grid = [[0 for _ in range(4)] for _ in range(4)]
    
    # Fill the grid based on the bitstrings
    for number, bitstring in sudoku_data.items():
        for index, bit in enumerate(bitstring):
            if bit == '1':
                row = index // 4
                col = index % 4
                grid[row][col] = number
    
    # Draw the numbers and colors in the grid
    for i in range(4):
        for j in range(4):
            cell_value = grid[i][j]
            # Set the color based on the value
            if cell_value == 0:
                cell_color = 'white'  # White for empty cells
            else:
                cell_color = color_map[cell_value]
            rect = patches.Rectangle((j, 3 - i), 1, 1, linewidth=0, edgecolor='none', facecolor=cell_color)
            ax.add_patch(rect)
            if cell_value != 0:
                ax.text(j + 0.5, 3 - i + 0.5, str(cell_value), ha='center', va='center', fontsize=18, fontweight='bold', color='black')
    
    # Draw the outer border
    outer_border = patches.Rectangle((0, 0), 4, 4, linewidth=3.5, edgecolor='black', facecolor='none')
    ax.add_patch(outer_border)
    
    # Set title
    plt.title('4x4 Sudoku', fontsize=24, fontweight='bold', color='darkblue')
    
    # Remove axes and show the plot
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()



def draw_9x9_sudoku_grid_bs(sudoku_data):
    # Define the color map for each number
    color_map = {
        1: '#FF6666', 2: '#66B2FF', 3: '#66FF66', 4: '#FFFF66',
        5: '#FF66FF', 6: '#66FFFF', 7: '#FF9966', 8: '#9966FF',
        9: '#66FF99'
    }
    
    # Create the base 9x9 grid
    fig, ax = plt.subplots(figsize=(9, 9))
    
    # Set background color
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#F0F0F0')
    
    # Draw the grid
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        ax.plot([i, i], [0, 9], color='black', linewidth=line_width)
        ax.plot([0, 9], [i, i], color='black', linewidth=line_width)
    
    # Initialize a 9x9 grid with zeroes
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the grid based on the bitstrings
    for number, bitstring in sudoku_data.items():
        for index, bit in enumerate(bitstring):
            if bit == '1':
                row = index // 9
                col = index % 9
                grid[row][col] = number
    
    # Draw the numbers and colors in the grid
    for i in range(9):
        for j in range(9):
            cell_value = grid[i][j]
            # Set the color based on the value
            if cell_value == 0:
                cell_color = 'white'  # White for empty cells
            else:
                cell_color = color_map[cell_value]
            rect = patches.Rectangle((j, 8 - i), 1, 1, linewidth=0, edgecolor='none', facecolor=cell_color)
            ax.add_patch(rect)
            if cell_value != 0:
                ax.text(j + 0.5, 8 - i + 0.5, str(cell_value), ha='center', va='center', fontsize=18, fontweight='bold', color='black')
    
    # Draw the outer border
    outer_border = patches.Rectangle((0, 0), 9, 9, linewidth=3.5, edgecolor='black', facecolor='none')
    ax.add_patch(outer_border)
    
    # Set title
    plt.title('9x9 Sudoku', fontsize=24, fontweight='bold', color='darkblue')
    
    # Remove axes and show the plot
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
