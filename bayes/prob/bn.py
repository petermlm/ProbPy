"""
Contain
=======

* BayesianNetwork
"""

from bayes.prob import factor

import copy


class BayesianNetwork:
    """
    Class that implements a Bayesian Network. It encapsulates some algorithms
    for Bayesian inference and abstract their usage
    """

    def __init__(self, network):
        """
        Constructor for class BayesianNetwork

        Argument:
        network -- List of tuples, where each tuple has a RandVar in the first
                   element and a factor in the second.
        """

        self.network = network

    def elimination_ask(self, query_var, observed):
        """
        Executes the Elimination Ask algorithm, receiving a query variable (q)
        and observations (E), returning a factor which correspondes to the
        distribution P(q | E)

        Arguments:
        query_var -- Random variable of type RandVar
        observed  -- List of observations. Each element of the list should be
                     a tuple, which first element is a RandVar and second
                     element is the observed value for that variable

        Example:
            >>> # Assuming X, Y and Z as vars and vz, vy as values of X and Y
            >>> observed = [(X, vx), (Y, vy)]
            >>> res = BN.elimination_ask(Z, observed)
            >>> res # P(Z | X=vx, Y=vy)
        """

        factors = []
        for i in self.network:
            factors.append(self.makeFactor(i[1], observed))
            if self.hidden(i[0], query_var.name, observed):
                factors = self.sumOut(i[0], factors)

        prod = factors[0]
        for i in factors[1:]:
            prod = prod.mult(i)

        res = prod.normalize([query_var])
        return res

    def makeFactor(self, arg_var, observed):
        var = copy.deepcopy(arg_var)

        for i in observed:
            res = var.instVar(i[0], i[1])
            if res is not None:
                var = res

        return var

    def hidden(self, var, query_var, observed):
        if var.name == query_var:
            return False

        for i in observed:
            if var.name == i[0]:
                return False

        return True

    def sumOut(self, var, arg_factors):
        # Multiply all until now
        prod = arg_factors[0]
        for i in arg_factors[1:]:
            prod = prod.mult(i)

        # Sum variable out
        marg_vars = []
        for i in prod.rand_vars:
            if i.name != var.name:
                marg_vars.append(i)

        return [prod.marginal(marg_vars)]
