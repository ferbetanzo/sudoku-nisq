import numpy as np
from typing import List
from qiskit import QuantumCircuit


def prepare_w_state(quantum_circuit: QuantumCircuit, qubit_indices: list[int]) -> None:
    """
    Prepare a W-state on the specified qubits in the quantum circuit.

    This function implements the W-state preparation algorithm as described in
    'Efficient quantum circuits for arbitrary W states' by Yong-Cheng Hou et al.

    Args:
        quantum_circuit (QuantumCircuit): The quantum circuit to modify.
        qubit_indices (list[int]): List of qubit indices to prepare the W-state on.

    Returns:
        None: The function modifies the input quantum circuit in-place.

    Raises:
        ValueError: If the input list of qubit indices is empty.

    Example:
        >>> qc = QuantumCircuit(3)
        >>> prepare_w_state(qc, [0, 1, 2])
    """
    if not qubit_indices:
        raise ValueError("The list of qubit indices cannot be empty.")

    num_qubits = len(qubit_indices)
    theta_angles = [np.arccos(np.sqrt(1 / (num_qubits + 2 - i))) for i in range(2, num_qubits + 1)]

    # Apply X gate to the first qubit
    quantum_circuit.x(qubit_indices[0])

    # Apply the sequence of controlled rotations
    for i in range(num_qubits - 1):
        control_qubit = qubit_indices[i]
        target_qubit = qubit_indices[i + 1]
        angle = theta_angles[i]

        quantum_circuit.cx(control_qubit, target_qubit)
        quantum_circuit.ry(-angle, target_qubit)
        quantum_circuit.cx(control_qubit, target_qubit)
        quantum_circuit.ry(angle, target_qubit)
        quantum_circuit.cx(target_qubit, control_qubit)



def prepare_controlled_w_state(quantum_circuit: QuantumCircuit, 
                               target_qubits: list[int], 
                               control_qubits: list[int]) -> None:
    """
    Prepare a controlled W-state on the specified target qubits in the quantum circuit.

    This function implements a controlled version of the W-state preparation algorithm.
    The W-state is prepared on the target qubits only if all control qubits are in the |1⟩ state.

    Args:
        quantum_circuit (QuantumCircuit): The quantum circuit to modify.
        target_qubits (list[int]): List of qubit indices to prepare the W-state on.
        control_qubits (list[int]): List of control qubit indices.

    Returns:
        None: The function modifies the input quantum circuit in-place.

    Raises:
        ValueError: If the input list of target qubits is empty.

    Example:
        >>> qc = QuantumCircuit(5)
        >>> prepare_controlled_w_state(qc, target_qubits=[2, 3, 4], control_qubits=[0, 1])
    """
    if not target_qubits:
        raise ValueError("The list of target qubits cannot be empty.")

    num_target_qubits = len(target_qubits)
    theta_angles = [np.arccos(np.sqrt(1 / (num_target_qubits + 2 - i))) 
                    for i in range(2, num_target_qubits + 1)]

    # Apply multi-controlled X gate to the first target qubit
    quantum_circuit.mcx(control_qubits, target_qubits[0])

    # Apply the sequence of controlled rotations
    for i in range(num_target_qubits - 1):
        current_target = target_qubits[i]
        next_target = target_qubits[i + 1]
        angle = theta_angles[i]

        # Multi-controlled X gate
        quantum_circuit.mcx([current_target] + control_qubits, next_target)

        # Controlled rotation
        quantum_circuit.ry(-angle, next_target)

        # Multi-controlled X gate
        quantum_circuit.mcx([current_target] + control_qubits, next_target)

        # Rotation
        quantum_circuit.ry(angle, next_target)

        # Final multi-controlled X gate
        quantum_circuit.mcx([next_target] + control_qubits, current_target)



def traverse_quantum_blocks(block_size: int, 
                            qubit_blocks: List[List[int]], 
                            control_qubits: List[int], 
                            target_qubits: List[int], 
                            quantum_circuit: QuantumCircuit) -> None:
    """
    Traverse quantum blocks and apply controlled operations based on block structure.

    This function recursively traverses the quantum circuit, applying controlled W-state
    preparations and multi-controlled X gates based on the given block structure and qubit
    configurations.

    Args:
        block_size (int): Number of qubits in each block.
        qubit_blocks (List[List[int]]): List of qubit blocks, where each block is a list of qubit indices.
        control_qubits (List[int]): List of control qubit indices.
        target_qubits (List[int]): List of target qubit indices for the current operation.
        quantum_circuit (QuantumCircuit): The quantum circuit to modify.

    Returns:
        None: The function modifies the input quantum circuit in-place.

    Note:
        This function assumes the existence of a `create_cwstate` function.

    Example:
        >>> from qiskit import QuantumCircuit
        >>> 
        >>> quantum_circuit = QuantumCircuit(8)
        >>> block_size = 4
        >>> qubit_blocks = [[0, 1, 2, 3], [4, 5, 6, 7]]
        >>> initial_controls = []
        >>> initial_targets = [0, 1, 2, 3]
        >>> 
        >>> traverse_quantum_blocks(block_size, qubit_blocks, initial_controls, initial_targets, quantum_circuit)
    """
    if len(control_qubits) < (block_size - 1):
        original_targets = target_qubits.copy()
        
        # Remove blocks containing control qubits
        for control_qubit in control_qubits:
            for block in qubit_blocks:
                if control_qubit in block:
                    qubit_blocks.remove(block)
                    break
        
        # Identify qubits to remove from target_qubits
        qubits_to_remove = []
        for qubit in target_qubits:
            if not any(qubit in block for block in qubit_blocks):
                qubits_to_remove.append(qubit)
        
        # Remove identified qubits from target_qubits
        for qubit in qubits_to_remove:
            target_qubits.remove(qubit)
        
        print(target_qubits, control_qubits)
        prepare_controlled_w_state(quantum_circuit, target_qubits, control_qubits)
        
        for qubit in original_targets:
            if any(qubit in block for block in qubit_blocks):
                new_targets = original_targets.copy()
                new_targets.remove(qubit)
                new_targets = [q + block_size for q in new_targets]
                new_blocks = qubit_blocks.copy()
                traverse_quantum_blocks(block_size, new_blocks, control_qubits + [qubit], new_targets, quantum_circuit)
    
    elif len(control_qubits) == block_size - 1:
        quantum_circuit.mcx(control_qubits, target_qubits[0])
