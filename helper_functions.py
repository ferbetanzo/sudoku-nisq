def filter_and_reverse_bitstrings(counts: dict, prefix: str = '11') -> list:
    """
    Filter bitstrings from quantum measurement counts and reverse the remaining part.

    This function takes a dictionary of measurement counts, filters the bitstrings
    based on a specified prefix, removes the prefix, and reverses the remaining part.

    Args:
        counts (dict): A dictionary where keys are bitstrings and values are counts.
        prefix (str, optional): The prefix to filter by. Defaults to '11'.

    Returns:
        list: A list of filtered and reversed bitstrings.

    Example:
        >>> counts = {'1100': 10, '1101': 20, '1000': 5, '1110': 15}
        >>> filter_and_reverse_bitstrings(counts)
        ['00', '01', '10']
        >>> filter_and_reverse_bitstrings(counts, prefix='10')
        ['00']
    """
    return [k[len(prefix):][::-1] for k in counts.keys() if k.startswith(prefix)]


def count_gates_between_first_two_barriers(quantum_circuit):
    """
    Count the number of gates between the first two barriers in a quantum circuit.

    Args:
        quantum_circuit (QuantumCircuit): The quantum circuit to analyze.

    Returns:
        int: The number of gates between the first two barriers.

    Raises:
        ValueError: If fewer than two barriers are found in the circuit.

    Usage Examples:
        >>> from qiskit import QuantumCircuit
        >>> qc = QuantumCircuit(3)
        >>> qc.h(0)
        >>> qc.barrier()
        >>> qc.cx(0, 1)
        >>> qc.cx(1, 2)
        >>> qc.barrier()
        >>> qc.measure_all()
        >>> count_gates_between_first_two_barriers(qc)
        2

        >>> qc2 = QuantumCircuit(2)
        >>> qc2.h(0)
        >>> qc2.barrier()
        >>> qc2.barrier()
        >>> count_gates_between_first_two_barriers(qc2)
        0

        >>> qc3 = QuantumCircuit(1)
        >>> qc3.h(0)
        >>> try:
        >>>     count_gates_between_first_two_barriers(qc3)
        >>> except ValueError as e:
        >>>     print(e)
        Fewer than two barriers found in the circuit
    """
    gate_count = 0
    barrier_count = 0

    for instruction in quantum_circuit.data:
        if instruction.operation.name == 'barrier':
            barrier_count += 1
            if barrier_count == 2:
                return gate_count
        elif barrier_count == 1:
            gate_count += 1

    raise ValueError("Fewer than two barriers found in the circuit")



def find_control_indices_for_sudoku(preset_dict, target_digit):
    """
    Identify qubit indices for a given target digit in a quantum Sudoku solving context.

    Args:
        preset_dict (dict): A dictionary where keys are qubit labels (e.g., cell positions) and values are bitstrings 
                             representing the presence (1) or absence (0) of digits in those cells.
        target_digit (int): The digit whose positions are to be identified in the Sudoku grid.

    Returns:
        tuple: A tuple containing two lists:
            - A list of indices where the target digit is found (already known or given positions).
            - A list of indices where other digits are present (excluding the target digit).

    Usage Examples:
        >>> sudoku_qubits = {
        ...     1: '1000000000000000',
        ...     2: '0100000000010000',
        ...     3: '0000100000000001',
        ...     4: '0010000100000000'
        ... }
        >>> find_qubit_indices_for_sudoku(sudoku_qubits, 2)
        ([1, 11], [0, 4, 15, 2, 7])

    Notes:
        - This function assumes the `qubit_states` dictionary has integer keys representing Sudoku cell positions and 
          bitstrings as values indicating the presence or absence of digits.
    """
    target_indices = [i for i, bit in enumerate(preset_dict[target_digit]) if bit == '1']
    non_target_indices = [i for key, bitstring in preset_dict.items() if key != target_digit for i, bit in enumerate(bitstring) if bit == '1']

    return target_indices, non_target_indices



def apply_multi_qubit_or(quantum_circuit, control_qubits, target_qubit):
    """
    Apply a multi-qubit OR operation on a set of control qubits and store the result in the target qubit.

    The OR operation is achieved using multi-controlled NOT gates (mcx) and single-qubit X gates.

    Args:
        quantum_circuit (QuantumCircuit): The quantum circuit to which the operations are applied.
        control_qubits (list[int]): List of qubit indices that serve as control qubits for the OR operation.
        target_qubit (int): The qubit index where the result of the OR operation is stored.

    Usage Examples:
        >>> from qiskit import QuantumCircuit
        >>> qc = QuantumCircuit(5)
        >>> control_qubits = [0, 1, 2]
        >>> target_qubit = 4
        >>> apply_multi_qubit_or(qc, control_qubits, target_qubit)
        >>> qc.draw('mpl')

        >>> qc2 = QuantumCircuit(6)
        >>> control_qubits2 = [1, 2, 3, 4]
        >>> target_qubit2 = 5
        >>> apply_multi_qubit_or(qc2, control_qubits2, target_qubit2)
        >>> qc2.draw('mpl')
    """
    # Apply X gates to all control qubits
    for qubit in control_qubits:
        quantum_circuit.x(qubit)
    
    # Apply multi-controlled X gate to the target qubit
    quantum_circuit.mcx(control_qubits, target_qubit)
    
    # Apply X gates again to restore control qubits
    for qubit in control_qubits:
        quantum_circuit.x(qubit)
    
    # Apply X to the target qubit to get the OR result
    quantum_circuit.x(target_qubit)



def calculate_negated_or_bitstring(bitstring_dict, excluded_key):
    """
    Calculate the bitwise OR of all bitstrings in the dictionary except the one corresponding to the excluded key,
    and then return the bitwise NOT of the result.

    Args:
        bitstring_dict (dict): A dictionary where keys are labels and values are bitstrings.
        excluded_key (str): The key whose corresponding bitstring should be excluded from the OR operation.

    Returns:
        str: The bitwise NOT of the OR result of all bitstrings except the excluded one.

    Usage Examples:
        >>> bitstrings = {
        ...     'a': '1100',
        ...     'b': '1010',
        ...     'c': '0110'
        ... }
        >>> calculate_negated_or_bitstring(bitstrings, 'b')
        '0001'

        >>> bitstrings2 = {
        ...     'x': '1111',
        ...     'y': '0000',
        ...     'z': '0011'
        ... }
        >>> calculate_negated_or_bitstring(bitstrings2, 'x')
        '1100'
    """
    # Initialize the result with zeros of the same length as the bitstrings
    bit_length = len(next(iter(bitstring_dict.values())))
    or_result = '0' * bit_length
    
    # Perform OR operation on all bitstrings except the excluded one
    for key, bitstring in bitstring_dict.items():
        if key != excluded_key:
            or_result = ''.join(str(int(a) | int(b)) for a, b in zip(or_result, bitstring))
    
    # Perform NOT operation on the result
    negated_result = ''.join('1' if bit == '0' else '0' for bit in or_result)
    
    return negated_result