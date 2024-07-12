import numpy as np
from itertools import combinations

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

class Grover:
    """
    A class that allows you to set up a Grover quantum circuit and run it.

    Attributes
    ----------
    tuples : [(int, int)]
        list of all field pairs that need to be considered in the algorithm
    normalized_tuples : [(int, int)]
        tuples normalized to 0..n field_index
    normalized_field_values : {int : int}
        the value for each field by normalized index which has a set value
    circuit : quantumCircuit
        the quantum circuit based on the tuples
    Methods
    -------
    print_circuit():
        prints the circuit that was generated for the problem
    run_circuit() -> dict:
        runs the quantum circuit and returns the number of appearence for each result
    """

    def __init__(self, tuples: list, field_values: dict, subunit_height: int, subunit_width: int):
        """
        Constructs the necessary attributes for the Grover class.

        Parameters
        ----------
        tuples : [(int, int)]
            a list of all field pairs that need to be considered
        field_values : {field_index : value}
            dictionary of all fields with a set value that are in the tuples
        subunit_height : int
            height a subunit has
        subunit_width : int
            width a subunit has
        """
        self.tuples = tuples
        self.normalized_tuples = self.get_normalized_tuples()
        self.normalized_field_values = self.get_normalized_field_values(field_values)
        self.subunit_height = subunit_height
        self.subunit_width = subunit_width
        self.circuit = self.set_circuit()

        ####################################################################################
        ####################################################################################
        ####                                                                            ####
        ####                                MODIFIED METHOD                             ####
        ####                                                                            ####
        ####################################################################################
        ####################################################################################

    # Auxiliar method added
    def generate_valid_combinations(self, elements, combination_size, forbidden_difference):
        """
        Generates valid combinations of a set of elements that meet the condition
        that the difference between any pair of elements is not equal to forbidden_difference.
        
        :param elements: Set of elements to generate combinations from.
        :param combination_size: Size of each combination.
        :param forbidden_difference: Forbidden difference between elements in a combination.
        :return: List of valid combinations.
        """
        
        # Function to check the condition of difference
        def difference_is_not_forbidden(combination):
            for a, b in combinations(combination, 2):
                if abs(a - b) == forbidden_difference:
                    return False
            return True
        
        # Generate all possible combinations of the specified size
        valid_combinations = [
            combination for combination in combinations(elements, combination_size) 
            if difference_is_not_forbidden(combination)
        ]
        
        return valid_combinations

    # Modification of the original flipper method
    def modified_flipper(self, quantum_circuit, x, y, compare_register, tuple_index, color_size):
        x_qubits = list(range(x*color_size, (x+1)*color_size))
        y_qubits = list(range(y*color_size, (y+1)*color_size))
        xy_distance = abs(y - x)
        qubit_indices = x_qubits + y_qubits

        # Apply XOR gates qubitwise between the x_qubits and y_qubits
        for i in range(color_size):
            quantum_circuit.cx(x_qubits[i], compare_register[tuple_index])
            quantum_circuit.cx(y_qubits[i], compare_register[tuple_index])


        for i in range(2, color_size+1):
            combinations = self.generate_valid_combinations(qubit_indices, i, color_size*xy_distance)
            for comb in combinations:
                quantum_circuit.mcx(list(comb), compare_register[tuple_index])

    # Modification of the original graph_coloring_oracle
    def modified_graph_coloring_oracle(self, qc: QuantumCircuit, compare_qubits: QuantumRegister, 
                                out_qubit: QuantumRegister, color_size: int, tuples):
    
        for index, tup in enumerate(tuples):#self.normalized_tuples):
            self.modified_flipper(qc, tup[0], tup[1], compare_qubits, index, color_size)
            qc.barrier()

        qc.mcx(compare_qubits[-len(tuples):], out_qubit)
        qc.barrier()
    

        for index, tup in enumerate(tuples):#self.normalized_tuples):
            self.modified_flipper(qc, tup[0], tup[1], compare_qubits, index, color_size)
            qc.barrier()
  

    # Modification of the original build_diffuser method
    def modified_difusser(self, quantum_circuits, quantum_register, out_qubit): 

        quantum_circuits.h(quantum_register)
        quantum_circuits.x(quantum_register)
        quantum_circuits.mcx(quantum_register, out_qubit)
        quantum_circuits.x(quantum_register)
        quantum_circuits.h(quantum_register)



        ####################################################################################
        ####################################################################################
  

    
    def get_normalized_tuples(self) -> list:
        """
        Tuples are given in a non normalized way as there are not all field indexes in the tuples.
        This means tuples could contain only n unique filed indexes but the field index could be
        higher than n. This function normalizes the tuples starting from 0 going up to n so the qubit
        init values can be applied later without problems.
        
        Returns
        -------
        [(int, int)]
            The tupels normalized so the minimum value is 0 and the max is n
        """
        # first a set of all field indexes that appear in the tuples is generated
        # the set gets ordered and every field index gets mapped to an int 0..n
        # the new tuple list is generated and returned
        # info: sets are by default allready ordered ascending
        field_index_set = set([t for tup in self.tuples for t in tup])
        normalized_dict = {original:index for index, original in enumerate(field_index_set)}

        normalized_tuples = [(normalized_dict.get(a), normalized_dict.get(b)) for (a, b) in self.tuples]

        return normalized_tuples
    
    def get_normalized_field_values(self, field_values: dict) -> dict:
        """
        For every field index its value is given if already set. This functions returns a normalized version of
        the dict where the field indexes get normalized to 0..n.
        
        Parameters
        ----------
        field_values : {int : int}
            The not normalized field index (key) and the corresponding value in dec representation

        Returns
        -------
        {int, int}
            The field indexes normalized so the minimum value is 0 and the max is n and their values
        """
        # first a set of all field indexes that appear in the tuples is generated
        # the set gets ordered and every field index gets mapped to an int 0..n
        # the new tuple list is generated and returned
        # info: sets are by default allready ordered ascending
        field_index_set = set([t for tup in self.tuples for t in tup]) # unique cells to compare
        normalized_dict = {original:index for index, original in enumerate(field_index_set)} # Reassign index

        normalized_field_values = {normalized_dict.get(k) : v for k, v in field_values.items() if k in normalized_dict} 
        # Add a conditional for dict creation

        return normalized_field_values
    

    def get_color_size(self) -> int:
        """
        A helpfer function for set_circuit to calculate the nuber of bits needed to encode the colors.
        Returns the number of bits needed.

        Returns
        -------
        int
        """
        # the number of colors needed to fill a subunit is calculated and transformed to binary
        # note that bin(dec) returns '0b....' so you have to reduce the len by 2 to get the bits needed
        subunit_size = self.subunit_height*self.subunit_width-1
        bits_needed = len(bin(subunit_size))-2
        
        return bits_needed
    

    def get_qubit_inits(self, number_of_qubits: int, color_size: int) -> dict:
        """
        Returns a dict aof all qubits with known positions.
        The key is the index in the QuantumRegister.
        The value ist eighter [1, 0], [0, 1] or [np.sqrt(2), np.sqrt(2)]
        
        Parameters
        ----------
        number_of_qubits : int
            The number of qubits in the input register.
        color_size : int
            The number of bits used to encode a color.

        Returns
        -------
        {int : list}
        """
        # go through all input qubits in steps of size color_size
        # check for the index i - this is the normalized number of the field represented by
        # the qubits - what its original field_index is
        # then get the value for this field from the field_values and set the init value
        # if there is no value in the dict the bits are set to superposition
        # otherwise the binary is generated and very bit gets set
        re_dict = {}

        for i in range(int(number_of_qubits/color_size)):
            field_value = self.normalized_field_values.get(i)
            for j in range(color_size):
                if field_value == None:
                    re_dict[i*color_size+j] = [1, 1]/np.sqrt(2)
                else:
                    binary_value = self.padded_binary(field_value, color_size)
                    if binary_value[j] == '0':
                        re_dict[i*color_size+j] = [1, 0]
                    else:
                        re_dict[i*color_size+j] = [0, 1]
        
        return re_dict
    

    def padded_binary(self, dec: int, color_size: int) -> str:
        """
        Helper function for get_qubit_inits that genreates a binary for a decimal number and
        pads it with leading 0 if it is not length of color_size.
        
        Parameters
        ----------
        dec : int
            The decimal representation of the number
        color_size : int
            The length the padded binnary has to have

        Returns
        -------
        str
            The padded binary string
        """
        binary = str(bin(dec))[2:]
        padding = '0' * (color_size - len(binary))
        padded_binary = padding + binary

        return padded_binary
    

    def __get_iterations_needed(self, number_of_qubits: int) -> int:
        """
        Returns the number of iterations needed to get the optimal solution.
        
        Parameters
        ----------
        number_of_qubits : int
            The number of qubits the diffuser is applied to

        Returns
        -------
        int
        """
        return int((np.pi/4)*np.sqrt(number_of_qubits))

    def set_circuit(self):
        """
        Builds the quantum circuit and returns it.
        The colors are encoded in the minimum number of bits needed to fill a subunit with unique colors.

        Returns
        -------
        QuantumCircuit
        """
        # from the tuples list the number of qubits is calculated by getting
        # the number of unique indexes that appear in the pairs
        # we use one compare qubit for each qubit of a field so to caompare two
        # fields with n-bit encoding we need n caompare qubits plus 1 extra compare
        # qubit to show if all single compared qubits were the same for two fields
        # with these numbers the circuit gets constructed
        unique_bits = len(set([t for tup in self.tuples for t in tup])) #unique cells to compare
        color_size = self.get_color_size() # Number of qubits to represent each possible value in a cell

        input_bits_needed = unique_bits*color_size # qubits needed to represent the cells to compare
        compare_bits_needed = len(self.tuples) # Number of auxiliar compare qubits
        classical_bits_needed = input_bits_needed # Number of readout bits

        unknown_qubits_needed = (unique_bits - len(self.normalized_field_values.keys())) * color_size # Number of qubits to represent the empty cells
        iterations_needed = self.__get_iterations_needed(unknown_qubits_needed) # iterations needed

        qubit_inits = self.get_qubit_inits(input_bits_needed, color_size) # Initialize the qubits eith the values in the cells
        unknown_qubits_positions = [pos for pos, val in qubit_inits.items() if val[0] not in [0, 1]]

        in_qubits = QuantumRegister(input_bits_needed, name='in')
        compare_qubits = QuantumRegister(compare_bits_needed, name='cmp')
        out_qubit = QuantumRegister(1, name='out')
        classical_bits = ClassicalRegister(classical_bits_needed, name='classic')

        qc = QuantumCircuit(in_qubits, compare_qubits, out_qubit, classical_bits)

        # the qubits are initialized 
        # afterwards the iterations are calculated and the circuit gets constructed
        qc.initialize([0, 1], out_qubit)
        qc.h(out_qubit)
        
        for position, init in qubit_inits.items():
            qc.initialize(init, in_qubits[position])

        qc.barrier()

        for _ in range(iterations_needed):
            self.modified_graph_coloring_oracle(qc, compare_qubits, out_qubit, color_size, self.normalized_tuples)
            qc.barrier()
            self.modified_difusser(qc, in_qubits, out_qubit)
            qc.barrier()
        
        qc.measure(in_qubits, classical_bits)

        return qc

    def print_circuit(self) -> dict:
        """
        Prints the circuit to the standard output.
        """
        print(self.circuit)