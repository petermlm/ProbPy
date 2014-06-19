import copy

class RandVar:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Factor:
    def __init__(self, rand_vars, values):
        self.rand_vars = rand_vars
        self.values = values

    def __repr__(self):
        if len(self.rand_vars) == 0:
            return "[]"

        s = "["

        # Place random variables
        for i in range(len(self.rand_vars) - 1):
            s += self.rand_vars[i].name + ", "
        s += self.rand_vars[-1].name + "]"

        return s

    def varInFactor(self, rand_var):
        for i in self.rand_vars:
            if i.name == rand_vars.name:
                return True
        return False

    def mult(self, factor):
        f = lambda x, y: x*y
        return self.factorOp(factor, f)

    def div(self, factor):
        f = lambda x, y: x/y
        return self.factorOp(factor, f)

    def factorOp(self, factor, fun):
        res_rand_vars = []
        res_values = []

        # If this is just scalar operation
        if self.rand_vars == []:
            return self.scalar(factor, self.values[0], fun)
        elif factor.rand_vars ==  []:
            return self.scalar(self, factor.values[0], fun)

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

        # Calculate mult list
        mult = []
        c_mult = 1

        for i in factor.rand_vars:
            mult.append(c_mult)
            c_mult *= len(i.domain)

        # Calculate div list
        div = []

        for i in factor.rand_vars:
            c_div = 1

            for j in res_rand_vars:
                if i.name == j.name:
                    break

                c_div *= len(j.domain)

            div.append(c_div)

        # Calculate resulting size of factor
        res_values_size = 1
        for i in res_rand_vars:
            res_values_size *= len(i.domain)

        # Calculate resulting factor
        index1 = 0
        for i in range(res_values_size):
            # Get index 2
            index2 = 0
            for j in range(len(factor.rand_vars)):
                dim = len(factor.rand_vars[j].domain)
                index2 += (int(i / div[j]) % dim) * mult[j]

            # Calculate value
            res_values.append(fun(self.values[index1], factor.values[index2]))

            # Increment index 1
            index1 = (index1 + 1) % len(self.values)

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def marginal(self, rand_vars):
        res_rand_vars = []

        # Get resulting variables
        for i in self.rand_vars:
            var_in_self = False

            for j in rand_vars:
                if i.name == j.name:
                    var_in_self = True
                    break

            if var_in_self:
                res_rand_vars.append(i)

        # Calculate resulting size of factor
        res_values_size = self.getValuesListSize(res_rand_vars)

        # Initialized Resulting factor
        res_values = [0] * res_values_size

        # Calculate marginal
        for i in range(len(self.values)):
            index = 0
            div = 1
            mult = 1
            k = 0

            for j in self.rand_vars:
                if k < len(res_rand_vars) and j.name == res_rand_vars[k].name:
                    index += (int(i / div) % len(res_rand_vars[k].domain)) * mult
                    mult *= len(res_rand_vars[k].domain)
                    k += 1

                div *= len(j.domain)

            res_values[index] += self.values[i]

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def instVar(self, rand_vars, insts):
        # If this is a single instantiation
        if type(rand_vars) != list and type(insts) != list:
            return self.instVarSingle(rand_vars, insts)

        # If this is a multiple instantiation
        elif type(rand_vars) == list and type(insts) == list:
            # If the size of this lists is not the same return
            if len(rand_vars) != len(insts):
                return None

            # Instantiate one variable at a time
            res = copy.copy(self)
            for i in range(len(rand_vars)):
                res = res.instVarSingle(rand_vars[i], insts[i])

            return res

    def instVarSingle(self, rand_var, inst):
        res_rand_vars = []
        var_index = -1

        # Get resulting variables and var_index
        for i in range(len(self.rand_vars)):
            # Store current index of variable to instantiate and add rest of variables
            if self.rand_vars[i].name == rand_var:
                var_index = i
                res_rand_vars += self.rand_vars[i+1:]
                break

            # Add current variable to list
            res_rand_vars.append(self.rand_vars[i])

        # If inst variable not in this factor, return it unchanged
        if var_index == -1:
            return self

        # Get div factor
        div = 1
        for i in self.rand_vars:
            if i.name == rand_var:
                break
            div *= len(i.domain)

        # Get inst index
        inst_index = -1
        for i in range(len(self.rand_vars[var_index].domain)):
            if self.rand_vars[var_index].domain[i] == inst:
                inst_index = i
                break

        # If the value for instance couldn't be found, return None
        if inst_index == -1:
            return None

        # Calculate resulting factor
        res_values = []
        for i in range(len(self.values)):
            if int(i/div) % len(self.rand_vars[var_index].domain) == inst_index:
                res_values.append(self.values[i])

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def normalize(self, arg_rand_vars):
        marg_vars = []

        # If the argument is a single variable
        if type(arg_rand_vars) != list:
            rand_vars = [arg_rand_vars]
        else:
            rand_vars = arg_rand_vars

        # Get resulting variables for marginal
        for i in self.rand_vars:
            var_in_self = True

            for j in rand_vars:
                if i.name == j.name:
                    var_in_self = False
                    break

            if var_in_self:
                marg_vars.append(i)

        # Get marginal
        marg = self.marginal(marg_vars)

        # Make division
        return self.div(marg)

    def getValuesListSize(self, rand_vars):
        values_size = 1
        for i in rand_vars:
            values_size *= len(i.domain)
        return values_size

    def scalar(self, factor, scalar_value, fun):
        return Factor(factor.rand_vars, list(map(fun, factor.values, [scalar_value]*len(factor.values))))

