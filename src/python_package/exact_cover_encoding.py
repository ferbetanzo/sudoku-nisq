from collections import defaultdict

class ExactCoverEncoding:
    def __init__(self, open_tuples, size):
        self.open_tuples = open_tuples
        self.size = size

        if self.size >= 2:
            self.universe = []
            self.gen_universe()
        else: self.universe2x2 = []

    def cell_const(self):
        unique_pairs = set((x, y) for x, y, _ in self.open_tuples)
        return list(unique_pairs)

    def row_const(self):
        row_constraints = {('row', row, digit) for row, _, digit in self.open_tuples}
        return list(row_constraints)

    def col_const(self):
        col_constraints = {('col', column, digit) for _, column, digit in self.open_tuples}
        return list(col_constraints)

    def subgrid_const(self):
        subgrid_constraints = set()
        for tup in self.open_tuples:
            i, j, value = tup
            subgrid_row_start = (i // self.size) * self.size
            subgrid_col_start = (j // self.size) * self.size
            subgrid_constraint = ('subgrid', subgrid_row_start, subgrid_col_start, value)
            subgrid_constraints.add(subgrid_constraint)
        return list(subgrid_constraints)

    def gen_universe(self):
        self.universe.extend(self.cell_const())
        self.universe.extend(self.row_const())
        self.universe.extend(self.col_const())
        self.universe.extend(self.subgrid_const())

    def gen_simple_subsets(self):
        subsets = defaultdict(list)
        i = 0
        for tuple in self.open_tuples:
            x, y, z = tuple
            cell = (x, y)
            row = ('row', x, z)
            col = ('col', y, z)
            subgrid = ('subgrid', (x // self.size) * self.size, (y // self.size) * self.size, z)
            key = f'S_{i}'
            subsets[key].append(cell)
            subsets[key].append(row)
            subsets[key].append(col)
            subsets[key].append(subgrid)
            i += 1
        return dict(subsets)

    def gen_patterns_subsets(self, possible_patterns, fixed_tuples):
        omitted_tuples = defaultdict(list)
        for tup in fixed_tuples:
            x, y, z = tup
            omitted_tuples[z].append((x, y))
        subsets = defaultdict(list)
        i = 0
        for digit, patterns_list in possible_patterns.items():
            for pattern in patterns_list:
                key = f'S_{i}'
                for col in range(len(pattern)):
                    k, l = pattern[col], col
                    cell = (k, l)
                    if cell not in omitted_tuples[digit]:
                        subsets[key].append(cell)
                        row = ('row', k, digit)
                        subsets[key].append(row)
                        col_item = ('col', l, digit)
                        subsets[key].append(col_item)
                        subgrid = ('subgrid', (k // self.size) * self.size, (l // self.size) * self.size, digit)
                        subsets[key].append(subgrid)
                i += 1
        return dict(subsets)

    def gen_universe2x2(self):
        self.universe2x2.extend(self.cell_const())
        self.universe2x2.extend(self.row_const())
        self.universe2x2.extend(self.col_const())

    def gen_simple_subsets2x2(self):
        subsets = defaultdict(list)
        i = 0
        for tuple in self.open_tuples:
            x, y, z = tuple
            cell = (x, y)
            row = ('row', x, z)
            col = ('col', y, z)
            key = f'S_{i}'
            subsets[key].append(cell)
            subsets[key].append(row)
            subsets[key].append(col)
            i += 1
        return dict(subsets)

    def gen_patterns_subsets2x2(self, possible_patterns, fixed_tuples):
        omitted_tuples = defaultdict(list)
        for tup in fixed_tuples:
            x, y, z = tup
            omitted_tuples[z].append((x, y))
        subsets = defaultdict(list)
        i = 0
        for digit, patterns_list in possible_patterns.items():
            for pattern in patterns_list:
                key = f'S_{i}'
                for col in range(len(pattern)):
                    k, l = pattern[col], col
                    cell = (k, l)
                    if cell not in omitted_tuples[digit]:
                        subsets[key].append(cell)
                        row = ('row', k, digit)
                        subsets[key].append(row)
                        col_item = ('col', l, digit)
                        subsets[key].append(col_item)
                i += 1
        return dict(subsets)