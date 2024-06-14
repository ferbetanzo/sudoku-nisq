"""This module defines the class Grover."""

import numpy as np
from itertools import chain, combinations

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, IBMQ, execute

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
        self.normalized_tuples = self.__get_normalized_tuples()
        self.normalized_field_values = self.__get_normalized_field_values(field_values)
        self.subunit_height = subunit_height
        self.subunit_width = subunit_width
        self.circuit = self.__set_circuit()
    
    def __get_normalized_tuples(self) -> list:
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
    
    def __get_normalized_field_values(self, field_values: dict) -> dict:
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
        field_index_set = set([t for tup in self.tuples for t in tup])
        normalized_dict = {original:index for index, original in enumerate(field_index_set)}

        normalized_field_values = {normalized_dict.get(k) : v for k, v in field_values.items()}

        return normalized_field_values

    def __build_diffuser(self, number_of_qubits: int):
        """
        Builds the diffuser part of the circuit.

        Parameters
        ----------
        number_of_qubits : int
            The number of qubits the diffusor should operate on.
        
        Returns
        -------
        gate
        """
        # the diffuser should work on any number of qubits
        # first you apply h and x to all qubits, then you apply a mcz to the last quibt
        # controlleb by all the others
        # afterwars x and h are applied again and the diffuser is returned as a gate

        qc = QuantumCircuit(number_of_qubits)

        qc.h(list(range(number_of_qubits)))
        qc.x(list(range(number_of_qubits)))

        qc.h(number_of_qubits-1)
        qc.mct(list(range(number_of_qubits-1)), number_of_qubits-1)
        qc.h(number_of_qubits-1)

        qc.x(list(range(number_of_qubits)))
        qc.h(list(range(number_of_qubits)))
        
        re_gate = qc.to_gate()
        re_gate.name = "Diffuser"

        return re_gate
    
    def __get_all_sublists(self, n: int, exclude: int) -> list:
        """
        A helper function for __flipper to find all sublists of a list without one specific index.
        """
        starting_list = [x for x in range(n) if x != exclude]
        max_n = n if exclude != -1 else n+1
        re_list = list(chain.from_iterable(combinations(starting_list, b) for b in range(1, max_n)))
        return re_list

    def __flipper(self, qc: QuantumCircuit, x: int, y: int, cmp: QuantumRegister, tup_index: int, color_size: int):
        """
        Sets one output Qubit to state 1 (equal) or 0 (not equal) for two Qubits x and y.
        Manipulates the state of cmp in the QuantumCircuit qc.

        Parameters
        ----------
        qc : QuantumCircuit
            The quantum circuit to operate on
        x : int
            The normalized_field_index of the first qubit to be compared
        y : int
            The normalized_field_index of the second qubit to be compared
        cmp : QuantumRegister
            The QuantumRegister to represent the result of the comparison
        tup_index : int
            The index of the tuple in the tuple list, needed for choosing the right compare qubits
        color_size : int
            The number of bits used to encode the colors in this problem
        """
        # TODO: reduce number of compare bits by just increasing gates
        # first all single bit pairs of two fileds are compared to one compare bit each
        # then all compare bits are compared in a single mct to a final compare bit

        for i in range(color_size):
            sublists_part_3 = self.__get_all_sublists(color_size, i)
            x_i = x*color_size+i
            y_i = y*color_size+i
            # Part 1 see explaination black_box_generalization.jpeg
            qc.cx([x_i, y_i], cmp[tup_index])

            # Part 3
            for e in sublists_part_3:
                list_e = list(e)
                # if the lenth of this list is 1 you just campare two bits and dont have to do it twice
                # otherwise you get the same ones twice
                if len(list_e) == 1:
                    qc.ccx(x_i, y_i+list_e[0], cmp[tup_index])
                else:
                    pass
            
        # Part 2
        sublists_part_2 = self.__get_all_sublists(color_size, -1)
        for e in sublists_part_2:
            list_e = list(e)
            # if more than on eelement is in list_e you apply a mct to them within one color register
            # this can be generalized and combined with Part 1 later in the optimization
            if len(list_e) > 1:
                print("ok")
                control_list_x = [x*color_size+x_i for x_i in list_e]
                control_list_y = [y*color_size+y_i for y_i in list_e]
                qc.ccx(control_list_x[:1], control_list_x[1:], cmp[tup_index])
                qc.ccx(control_list_y[:1], control_list_y[1:], cmp[tup_index])
    
    def __graph_coloring_oracle(self, qc: QuantumCircuit, compare_qubits: QuantumRegister, 
                                out_qubit: QuantumRegister, color_size: int):
        """
        Builds the graph coloring oracle needed for Grover.
        Does not return a value but directly manipulates the QuantumCircuit that was given
        as a parameter.

        Parameters
        ----------
        in_qubits : QuantumRegister
            the input qubits representing the n-bit encoded fields
        compare_qubits : QuantumRegister
            the qubits used to show the result of the comaprison of two input qubit groups
        out_qubit : QuantumRegister
            the qubit with the negative amplitude used in grover
        color_size : int
            the number of bits used to encode the colors in the problem
        """
        # we apply the gates between the single qubits of the field pair to see if they are equal
        # then on all final compare output bits a mct is perfromed that if all values are 1
        # the last len(self.normalized_tuples) bits are the final comapre output bits
        # a mct on the final output bits flips the output qubit and the phase flips to negative values
        for index, tup in enumerate(self.normalized_tuples):
            self.__flipper(qc, tup[0], tup[1], compare_qubits, index, color_size)
        # for every tupel there is one final compare bit
        # the final compare bits sre at the end of the caompare_qubits
        qc.mct(compare_qubits[-len(self.normalized_tuples):], out_qubit)
        for index, tup in enumerate(self.normalized_tuples):
            self.__flipper(qc, tup[0], tup[1], compare_qubits, index, color_size)


    def __get_color_size(self) -> int:
        """
        A helpfer function for __set_circuit to calculate the nuber of bits needed to encode the colors.
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

    def __get_qubit_inits(self, number_of_qubits: int, color_size: int) -> dict:
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
                    binary_value = self.__padded_binary(field_value, color_size)
                    if binary_value[j] == '0':
                        re_dict[i*color_size+j] = [1, 0]
                    else:
                        re_dict[i*color_size+j] = [0, 1]
        
        return re_dict

    def __padded_binary(self, dec: int, color_size: int) -> str:
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

    def __set_circuit(self):
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
        unique_bits = len(set([t for tup in self.tuples for t in tup]))
        color_size = self.__get_color_size()

        input_bits_needed = unique_bits*color_size
        compare_bits_needed = len(self.tuples)
        classical_bits_needed = input_bits_needed

        unknown_qubits_needed = (unique_bits - len(self.normalized_field_values.keys())) * color_size
        iterations_needed = self.__get_iterations_needed(unknown_qubits_needed)

        qubit_inits = self.__get_qubit_inits(input_bits_needed, color_size)
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
            self.__graph_coloring_oracle(qc, compare_qubits, out_qubit, color_size)
            qc.barrier()
            qc.append(self.__build_diffuser(unknown_qubits_needed), unknown_qubits_positions)
            qc.barrier()
        
        qc.measure(in_qubits, classical_bits)

        return qc

    def print_circuit(self) -> dict:
        """
        Prints the circuit to the standard output.
        """
        print(self.circuit)

    def run_circuit(self):
        """
        Runs the circuit on the quasm simulator and returns the counts of the results.

        Returns
        -------
        {str : int}
            The result of the measured qubits as a string and the number of occurences
        """
        provider = IBMQ.load_account()
        backend = provider.get_backend('ibmq_qasm_simulator')
        job = execute(self.circuit, backend, shots = 1024)
        result = job.result()
        return result.get_counts()