# Sudoku

Sudoku is a python project that uses quantum algorithms to solve a game of sudoku.

## Nomenclature
Board := The whole board on which a game of sudoku is played, consists of the grid <br>
Grid := Consists of n x m Subunits, a 2 by 2 Grid for example means that you have 2 x 2 Subunits <br>
Subunit := Consists of n x m fields <br>
Field := atomic unit of a sudoku, each field holds an integer with it's value, -1 means the filed is empty in terms of sudoku <br>
Field Index := every field on the board has an unique identifier starting at 0 in the upper left corner and increases by 1 for every field to the right, when reached the right end, you go on with the next line. The highest index is in the lower right corner.

## Black Box / Oracle
See the black_box_generalized.jpeg file for explaination on the generalization of the oracle needed for the graph coloring problem.

## Status
Rigth now you can set a board of sudoku with the Board class. The class provides all necessary information for the QuantumSolver class to set up a quantum circuit and solve the problem.
At the current stage this prototype uses Grover's algorithm.

## External librarys needed
To use the project you also need to install qiskit. Use the package manager [pip](https://pip.pypa.io/en/stable/) to do this:
'''bash
pip install qiskit
'''
