from ProbPy import RandVar, Factor, Event

from multiprocessing import Process, Queue


class ParFactor(Factor):
    def factorOp(self, factor, fun):
        """
        Same as factorOp() in Factor class, but implemented using Python's
        multiprocessing library

        :param factor: The other factor used for this operation
        :param fun:    Operation used between each element of the values
        :returns:      Result of operation between self and factor using fun
        """

        res_rand_vars = []

        # If this is just scalar operation
        if type(factor) == int or type(factor) == float:
            return self.scalar(factor, fun)
        elif factor.rand_vars == []:
            return self.scalar(factor.values[0], fun)

        # Res will have every variable in self
        for i in self.rand_vars:
            res_rand_vars.append(i)

        # And the variables in factor that are not in self
        for i in factor.rand_vars:
            var_in_self = True
            for j in self.rand_vars:
                if i.name == j.name:
                    var_in_self = False
                    break

            if var_in_self:
                res_rand_vars.append(i)

        # Calculate mult and div list
        mult, div, dim = self.getAuxLists(factor.rand_vars, res_rand_vars)

        # Calculate resulting size of factor
        res_values_size = self.getValuesListSize(res_rand_vars)

        # Calculate resulting factor
        res_values = self.calcResFactor(mult, div, dim, factor.rand_vars, factor.values, res_values_size, fun)
        return Factor(res_rand_vars, res_values)

    def getAuxLists(self, factor_rand_vars, res_rand_vars):
        mult = []
        div = []
        dim = []
        c_mult = 1

        for i in factor_rand_vars:
            # Mult
            mult.append(c_mult)
            c_mult *= len(i.domain)

            # Div
            c_div = 1

            for j in res_rand_vars:
                if i.name == j.name:
                    break

                c_div *= len(j.domain)

            div.append(c_div)

            # Dim
            dim.append(len(i.domain))

        return mult, div, dim

    def calcResFactor(self, mult, div, dim,
                      factor_rand_vars, factor_values,
                      res_values_size,
                      fun):
        res_values = [0] * res_values_size
        index1 = 0
        len_values = len(self.values)

        for i in range(res_values_size):
            # Get index 1
            index1 = i % len_values

            # Get index 2
            index2 = 0
            for j, _ in enumerate(factor_rand_vars):
                index2 += (int(i / div[j]) % dim[j]) * mult[j]

            # Calculate value
            res_values.append(fun(self.values[index1], factor_values[index2]))

        # Make Factor object and return
        return res_values
