import copy
from functools import lru_cache

import networkx as nx
from docplex.mp.model import Model

from .graph_problem import GraphProblem
from qiskit_optimization.problems.quadratic_program import QuadraticProgram


class Maxcut(GraphProblem):

    def __init__(self, g=None):
        self._g = copy.deepcopy(g)

    @lru_cache()
    def to_quadratic_problem(self):
        mdl = Model()

        x = {i: mdl.binary_var(name='x_{0}'.format(i)) for i in range(self._g.number_of_nodes())}

        for u, v in self._g.edges:
            self._g.edges[u, v].setdefault('weight', 1)

        objective = mdl.sum(self._g.edges[i, j]['weight'] * x[i]
                            * (1 - x[j]) for i, j in self._g.edges)

        mdl.maximize(objective)

        # print(mdl.export_as_lp_string())

        qp = QuadraticProgram()
        qp.from_docplex(mdl)
        # print(qp.export_as_lp_string())

        return qp

    # def is_feasible(self, x):
    #     return self.qp.is_feasible(x)

    # def objective_value(self, x):
    #     var_values = {}
    #     for i, var in enumerate(self.qp.variables):
    #         var_values[var.name] = x[i]
    #     return self.qp.substitute_variables(var_values).objective.constant

    def plot_graph(self, x, pos=None):
        colors = ['r' if value == 0 else 'b' for value in x]
        nx.draw(self._g, node_color=colors, pos=pos)

    def g(self):
        return copy.deepcopy(self._g)
