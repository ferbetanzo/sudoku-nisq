import math
from pytket import Circuit, Qubit, OpType
from copy import deepcopy

class Exact_Cover_QCirc:
    def __init__(self, universe, subsets, num_solutions=1):
        self.universe = universe
        self.subsets = subsets
        self.num_solutions = num_solutions
        self.u_size = len(universe)        # Total elements to cover
        self.s_size = len(subsets)         # Number of subsets
        self.b = math.ceil(math.log2(self.s_size))  # Qubits for counting
        
        # Initialize circuits
        self.main_circuit = Circuit()
        self.oracle = Circuit()
        self.diffuser = Circuit()
        self.count_circuit = Circuit()
        self.count_circuit_dag = Circuit()
        self.aux_circ = Circuit()

        # Generate a register for the subsets
        self.s_qubits = [Qubit("S",i) for i in range(self.s_size)]

        # Add subset qubits to the main circuit
        for q in self.s_qubits:
            self.main_circuit.add_qubit(q)

        # Apply Hadamard to each qubit in the main circuit
        for q in self.s_qubits:
            self.main_circuit.H(q)

        # Add the subset register to the counting, diffuser and auxiliary circuits
        for q in self.s_qubits:
            self.count_circuit.add_qubit(q)
            self.diffuser.add_qubit(q)
            self.aux_circ.add_qubit(q)
        
        '''
        For each element u_i in U, we add qubits U_i[0], ... , U_i[b] for implementing
        the counter of the element u_i to store the number of subsets covering it
        '''
        self.u_qubits = []
        for i in range(self.u_size):
            label = f"U_{i}"
            u_label_qubits = [Qubit(label,j) for j in range(self.b)]
            self.u_qubits.extend(u_label_qubits)

        # Add the U_{i} registers to the main, counting, oracle and auxiliary circuits
        for q in self.u_qubits:
            self.main_circuit.add_qubit(q)
            self.count_circuit.add_qubit(q)
            self.oracle.add_qubit(q)
            self.aux_circ.add_qubit(q)

        # Add the ancilla
        self.anc = Qubit("anc")
        self.main_circuit.add_qubit(self.anc)
        self.oracle.add_qubit(self.anc)
        self.aux_circ.add_qubit(self.anc)
        self.main_circuit.add_gate(OpType.X, [self.anc])
        self.main_circuit.add_gate(OpType.H, [self.anc])

    def build_counter(self):
        ## Generate lists for creating the Toffoli's for the counters
        # The following section takes a subset and creates a list of the qubits that will be
        # controls and targets for the toffoli gate for generating the counters
        all_lists = []  # This will store all generated lists
        j = 0  # Index for the S qubit corresponding to the S_j subset
        for subset in self.subsets:
            q_list = []
            for elementU in self.subsets[subset]:
                S_list = []  # Generate a list to contain all lists of qubits to add a Toffoli
                S_list.append(Qubit("S", j))
                # Access register corresponding to the element u_i in subset S_subset
                i = self.universe.index(elementU)
                label = f"U_{i}"
                register = [q for q in self.count_circuit.qubits if q.reg_name.startswith(label)]
                for q in register:
                    S_list.append(q)
                    q_list.append(deepcopy(S_list))
            all_lists.append(q_list)
            j += 1

        reversed_lists = []
        for element in all_lists:
            reversed_element = element[::-1]
            reversed_lists.append(reversed_element)
            
        for element in reversed_lists:
            for q_list in element:
                self.count_circuit.add_gate(OpType.CnX, q_list)

        # Invert the counter
        self.count_circuit_dag = self.count_circuit.dagger()

    def build_oracle(self):
        for q in self.u_qubits:
            if q.index[0] != 0:
                    self.oracle.X(q)

        oracle_qubits_list = []
        for q in self.u_qubits:
            oracle_qubits_list.append(q)
        oracle_qubits_list.append(self.anc)
        self.oracle.add_gate(OpType.CnX, oracle_qubits_list)
        
        for q in self.u_qubits:
            if q.index[0] != 0:
                    self.oracle.X(q)

    def build_diffuser(self):
        diffuser_qubits_list = []
        for q in self.s_qubits:
            self.diffuser.H(q)
            self.diffuser.X(q)
            diffuser_qubits_list.append(q)
        
        self.diffuser.add_gate(OpType.CnZ, diffuser_qubits_list)
        
        for q in self.s_qubits:
            self.diffuser.X(q)
            self.diffuser.H(q)

    def assemble_aux_circ(self):
        self.build_counter()
        self.build_oracle()
        self.aux_circ.append(self.count_circuit)
        self.aux_circ.append(self.oracle)
        self.aux_circ.append(self.count_circuit_dag)

    def assemble_full_circuit_w_meas(self, num_iterations = None):
        
        self.assemble_aux_circ()
        self.build_diffuser()
        
        if num_iterations is None:
            a = math.sqrt((2 ** self.s_size) / self.num_solutions)
            num_iterations = math.floor((math.pi / 4) * a)
            
        # Append sub-circuits to the main circuit
        for i in range(num_iterations):
            self.main_circuit.append(self.aux_circ)
            self.main_circuit.append(self.diffuser)

        c_bits = self.main_circuit.add_c_register("c", self.s_size)
        for q in self.s_qubits:
            self.main_circuit.Measure(q, c_bits[q.index[0]])

    def find_resources(self, num_iterations = None):
        if num_iterations is None:
            a = math.sqrt((2 ** self.s_size) / self.num_solutions)
            num_iterations = math.floor((math.pi / 4) * a)
        num_qubits = self.s_size + self.u_size * self.b + 1
        superpos_gates = self.s_size
        prepare_anc_gates = 2
        counter_gates = 0
        for s in self.subsets:
            counter_gates += len(self.subsets[s]) * self.b
        oracle_gates = 1 + 2*((self.u_size - 1)*self.b)
        diffuser_gates = 1 + 4*self.s_size
        MCX_gates = num_iterations*(oracle_gates+2*counter_gates)
        total_gates = superpos_gates + prepare_anc_gates + MCX_gates + num_iterations*diffuser_gates
        
        return num_qubits, total_gates, MCX_gates

    def get_circuit(self):
        # Returns the fully assembled circuit
        return self.main_circuit


'''
# Example usage
U = [1, 2, 3]
S = {'S_0': [U[2]], 'S_1': [U[0], U[2]], 'S_2': [U[0]], 'S_3': [U[1]], 'S_4': [U[0], U[1]]}
'''