import os
from python_package.sudoku import Sudoku
from python_package.pattern_generation import pattern_generation
from python_package.exact_cover_encoding import ExactCoverEncoding
from python_package.exact_cover_circ import Exact_Cover_QCirc

def process_file_simple_encoding(file_path,size):
    sudoku = Sudoku(file_path)
    sudoku.general_preprocessing()
    sudoku.general_preprocessing()
    # Define open tuples and (pre)set tuples
    sudoku.convert_to_simple_open_tuples()
    open_tuples = sudoku.simple_open_tuples
    # Initialize the encoding
    encoding = ExactCoverEncoding(open_tuples,size=size)
    encoding.gen_universe()     # Generate the universe set
    universe = encoding.universe
    S = encoding.gen_simple_subsets()
    ExactCover = Exact_Cover_QCirc(universe,S,num_solutions=1)
    q_count, gate_count = ExactCover.find_resources()
    """print("Total qubits count =", q_count)
    print("Total gate count =", gate_count)"""
    return q_count, gate_count
    

def process_file_patt_encoding(file_path,size):
    sudoku = Sudoku(file_path)
    sudoku.general_preprocessing()
    sudoku.general_preprocessing()
    sudoku.general_preprocessing()
    # Define open tuples and (pre)set tuples
    sudoku.convert_to_simple_open_tuples()
    open_tuples = sudoku.simple_open_tuples
    sudoku.convert_to_simple_set_tuples()
    set_tuples = sudoku.simple_set_tuples
    # Initialize the encoding
    encoding = ExactCoverEncoding(open_tuples,size=size)
    encoding.gen_universe()     # Generate the universe set
    universe = encoding.universe
    possible_patterns = pattern_generation(open_tuples,set_tuples,size=size).patterns
    S = encoding.gen_patterns_subsets(possible_patterns,set_tuples)
    ExactCover = Exact_Cover_QCirc(universe,S,num_solutions=1)
    q_count, gate_count = ExactCover.find_resources()
    """print("Patt Total qubits count =", q_count)
    print("Patt Total gate count =", gate_count)"""
    return q_count, gate_count

# print(os.getcwd())
directory_path = 'data'
files = os.listdir(directory_path) # List all files in the directory

results = {
    "4x4_simple": [],
    "4x4_pattern": [],
    "easy_simple": [],
    "easy_pattern": [],
    "medium_simple": [],
    "medium_pattern": [],
    "hard_simple": [],
    "hard_pattern": []
}

for file in files:
    if '2x2' in file:  # Skip files that contain '2x2'
        continue

    file_path = os.path.join(directory_path, file)  # Construct full file path once for each file

    if '4x4' in file:  # Process 4x4 example.
        result = process_file_simple_encoding(file_path,2)
        results["4x4_simple"].append(result)
        result = process_file_patt_encoding(file_path,2)
        results["4x4_pattern"].append(result)
        # print(f'File:{file_path},Results:{results}')
        
    if 'easy' in file:
        result = process_file_simple_encoding(file_path, 3)
        results["easy_simple"].append(result)
        result = process_file_patt_encoding(file_path, 3)
        results["easy_pattern"].append(result)
        # print(f'File:{file_path},Results:{results}')

    if 'medium' in file:
        result = process_file_simple_encoding(file_path, 3)
        results["medium_simple"].append(result)
        result = process_file_patt_encoding(file_path, 3)
        results["medium_pattern"].append(result)
        # print(f'File:{file_path},Results:{results}')

    if 'hard' in file:
        result = process_file_simple_encoding(file_path, 3)
        results["hard_simple"].append(result)
        result = process_file_patt_encoding(file_path, 3)
        results["hard_pattern"].append(result)
        # print(f'File:{file_path},Results:{results}')

averages = {}
for key, value in results.items():
    qubit_sum = sum(item[0] for item in value)
    gate_count_sum = sum(item[1] for item in value)
    qubit_avg = qubit_sum / len(value)
    gate_count_avg = gate_count_sum / len(value)
    averages[key] = {'qubit_avg': qubit_avg, 'gate_count_avg': gate_count_avg}

print(f'RESULTS={results}')
print(averages)