import pandas as pd
import itertools
import re

class Expression:
    def __init__(self, expr):
        self.expr = expr
        self.products, self.literals = self.parse_expression(expr)
        self.base_literals = sorted(set([literal.replace("'", "") for literal in self.literals]))
        self.depth = len(self.base_literals)
        self.truth_table = self.generate_truth_table()

    def parse_expression(self, expr):
        products = re.split("\+", expr.replace(' ', ''))
        literals = set([val for sublist in [re.split("\*", product) for product in products] for val in sublist])
        return products, literals

    def generate_truth_table(self):
        self.truths = dict()

        variable_indices = list(zip(self.base_literals, range(self.depth)))
        tt = list(itertools.product([True, False], repeat=self.depth))

        for var in variable_indices:
            self.truths[var[0]] = [row[var[1]] for row in tt]

        base_df = pd.DataFrame(self.truths, dtype="bool")

        for lit in self.literals:
            if lit[-1] == "'":
                base_df[lit] = ~base_df[lit[0]]

        for prod in self.products:
            terms = re.split("\*", prod)
            base_df[prod] = base_df[terms].product(axis=1).astype(bool)
        
        base_df[self.expr] = base_df[self.products].sum(axis=1).astype(bool)

        return base_df

    def add_term(self, expr):
        products, literals = self.parse_expression(expr)
        base_literals = set([literal.replace("'", "") for literal in literals])

        if not base_literals.issubset(set(self.base_literals)):
            raise KeyError("Please only add terms containing variable found in the initial expression.")

        self.literals.update(literals)
        self.products += products
        
        for lit in literals:
            if lit[-1] == "'":
                self.truth_table[lit] = ~self.truth_table[lit[0]]
            
        for prod in products:
            terms = re.split("\*", prod)
            self.truth_table[prod] = self.truth_table[terms].product(axis=1).astype(bool)

        self.truth_table[expr] = self.truth_table[products].sum(axis=1).astype(bool)

    def display(self):
        print(self.truth_table)