from dist import *

import copy

class BayesianNetwork:
    def __init__(self, network):
        self.network = network

    def elemination_ask(self, query_var, observed):
        factors = []
        for i in self.network:
            factors.append(self.makeFactor(i[1], observed))
            for k in factors:
            if self.hidden(i[0], query_var.name, observed):
                factors = self.sumOut(i[0], factors)
                for k in factors:

        prod = factors[0]
        for i in factors[1:]:
            prod = prod.mult(i)

        res = prod.normalize([query_var])

        return 0

    def makeFactor(self, arg_var, observed):
        var = copy.deepcopy(arg_var)

        for i in observed:
            res = var.instVar(i[0], i[1])
            if res != None:
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

