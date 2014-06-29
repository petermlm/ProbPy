"""
Contains
========

* RandVar
* RandVarNameEx
* RandVarDomainEx

* Factor
* FactorRandVarsEx
* FactorValuesEx
"""


import copy


class RandVar:
    """
    Represents a Random Variable in a probability distribution. Each variable
    is identified by a string which is it's name. If two RandVar in a script
    have the same name, the library will assume they are the same variable.

    Each variable also has a domain. The domain is a list of values which the
    variable can take. As of this version the elements on the list should only
    be of the string type. In later versions other types will be allowed. Maybe
    even types that are other objects.

    Examples:
        >>> coin = RandVar("Coin", ["Head", "Tail"])
        >>> ball = RandVar("Ball", ["Red", "Green", "Blue"])
    """

    def __init__(self, name, domain):
        """
        Arguments:
        name   -- String with the name of this variable
        domain -- List with the domain of this variable
        """

        if type(name) != str:
            raise RandVarNameEx(name)

        if type(domain) != list or len(domain) == 0:
            raise RandVarDomainEx(domain)

        for i in domain:
            if type(i) != str:
                raise RandVarDomainEx(domain)

        self.name = name
        self.domain = domain

    def __str__(self):
        list_str = "["

        for i in self.domain[:-1]:
            list_str += i + ", "
        list_str += self.domain[-1] + "]"

        return "(" + self.name + ", " + list_str + ")"


class RandVarNameEx(Exception):
    """ Exception use for a bad Random Variable name """

    def __init__(self, bad_name):
        self.bad_name = bad_name

    def __str__(self):
        return "Bad Random Variable name: " + repr(self.bad_name)


class RandVarDomainEx(Exception):
    """ Exception use for a bad domain for a Variable """

    def __init__(self, bad_domain):
        self.bad_domain = bad_domain

    def __str__(self):
        return "Bad Random Variable domain:" + repr(self.bad_domain)


class Factor:
    """
    Represents a Factor. A Factor has one or more random variables associated
    with an array of values. The array of values is a vectorization of the
    multi dimensional matrix that represents the factor.

    Examples:
        >>> # Assuming X and Y are variables
        >>> XY_factor = Factor([X, Y], [0.2, 0.3, 0.1, 0.4])
    """

    def __init__(self, rand_vars, values):
        """
        Arguments:
        rand_vars -- List of Random Variables of this factor, or single
                     variable
        values    -- Values of the factor
        """

        # Assure the rand_vars argument is always a list
        if type(rand_vars) != list:
            rand_vars = [rand_vars]

        for i in rand_vars:
            if type(i) != RandVar:
                raise FactorRandVarsEx(rand_vars)

        if type(values) == list:
            for i in values:
                if type(i) != int and type(i) != float:
                    raise FactorValuesEx(rand_vars)
        elif type(values) != int and type(values) != float:
            raise FactorValuesEx(rand_vars)

        self.rand_vars = rand_vars
        self.values = values

    def mult(self, factor):
        """ Multiplication operation for factorOp """

        fun = lambda x, y: x*y
        return self.factorOp(factor, fun)

    def div(self, factor):
        """ Division operation for factorOp """

        fun = lambda x, y: x/y
        return self.factorOp(factor, fun)

    def add(self, factor):
        """ Addition operation for factorOp """

        fun = lambda x, y: x+y
        return self.factorOp(factor, fun)

    def sub(self, factor):
        """ Subtraction operation for factorOp """

        fun = lambda x, y: x-y
        return self.factorOp(factor, fun)

    def factorOp(self, factor, fun):
        """
        Function used by others to implement a factor operation between self
        and another factor.

        Arguments:
        factor -- The other factor used for this operation
        fun    -- Operation used between each element of the values
        """

        res_rand_vars = []
        res_values = []

        # If this is just scalar operation
        if type(factor) == int or type(factor) == float:
            return self.scalar(self, factor, fun)
        elif self.rand_vars == []:
            return self.scalar(factor, self.values[0], fun)
        elif factor.rand_vars == []:
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

    def scalar(self, factor, scalar_value, fun):
        """
        Scalar operation between factor and a scalar_value. The scalar is used
        in an operation, defined by fun, with the values of factor.

        Arguments:
        factor       -- The factor which values are going to be used as
                        operands with scalar
        scalar_value -- An int or float value to serve as an operand
        fun          -- Function used in the operation, may be a lambda
        """

        map_res = []
        for i in factor.values:
            map_res.append(fun(i, scalar_value))

        return Factor(factor.rand_vars, list(map_res))

    def marginal(self, arg_rand_vars):
        """
        Calculates the marginal of a factor for a list of random variables.
        For example, if XY_factor is the distribution P(X, Y). Calculating the
        marginal of X will give P(X).
        """

        res_rand_vars = []

        # If the argument is a single variable
        if type(arg_rand_vars) != list:
            rand_vars = [arg_rand_vars]
        else:
            rand_vars = arg_rand_vars

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
                    index += (int(i/div) % len(res_rand_vars[k].domain)) * mult
                    mult *= len(res_rand_vars[k].domain)
                    k += 1

                div *= len(j.domain)

            res_values[index] += self.values[i]

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def normalize(self, arg_rand_vars):
        """
        Normalizes the factor for random variables in the distribution. If the
        factor of variable X has values [1, 3], the normalization will yield
        the [1/4, 3/4], distribution. If a factor represents the distribution
        P(X, Y), normalizing for X will yield P(X | Y).
        """

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

    def instVar(self, rand_vars, insts):
        """
        Instantiates a random variables of a factor. Instantiating variable X
        with value vx and Y with vy would yield f(X=vx, Y=vy, Z) = f(Z).

        Arguments:
        rand_vars -- List of variables to instantiate
        insts     -- Value for each variable

        Note, the sizes of the lists must be the same. Variable rand_vars[k]
        will be instantiated with value insts[k].
        """

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
        """
        Same has instVar, but this method instantiates a single variable and
        it is the one used in the implementation of instVar.

        Arguments:
        rand_var -- Variable to instantiate
        inst     -- Value for variable
        """

        res_rand_vars = []
        var_index = -1

        # Get resulting variables and var_index
        for i in range(len(self.rand_vars)):
            # Store current index of variable to instantiate and add rest of
            # variables
            if self.rand_vars[i].name == rand_var.name:
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
            if i.name == rand_var.name:
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
            if int(i/div) % len(self.rand_vars[var_index].domain) == \
                    inst_index:
                res_values.append(self.values[i])

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def expectedValue(self, fun):
        """
        Calculates the expected value for the variables in rand_vars. The
        method should be used if the factor represents a probability
        distribution. Suppose the factor f(X) would represent the distribution
        P(X), this method would calculate the expected value of X, E[X].

        If the factor f(X, Y) represents the distribution P(X | Y), the
        expected value calculated is E[X]

        Arguments:
        fun -- A function for the variable

        Examples:
            >>> X_factor = RandVar(X, ["T", "F"])
            >>> X_factor.Factor(X, [0.8, 0.2])
            >>> X_ev.Factor(X, [10, 20])
            >>> X_factor.expectedValue(X, X_ev)
            12.0
        """

        # Instantiate every conditional variable with it's first value, because
        # E[X] == E[X | Y=y], for any y
        fac = copy.deepcopy(self)
        fact_vars = fac.rand_vars

        for i in fact_vars:
            if not fun.varInFactor(i):
                fac = fac.instVar(i, i.domain[0])

        # Make the multiplication
        mult = fac.mult(fun)

        # Sum all
        res = 0
        for i in mult.values:
            res += i

        return res

    def varInFactor(self, rand_var):
        for i in self.rand_vars:
            if i.name == rand_var.name:
                return True
        return False

    def getValuesListSize(self, rand_vars):
        values_size = 1
        for i in rand_vars:
            values_size *= len(i.domain)
        return values_size

    def __str__(self):
        if len(self.rand_vars) == 0:
            return "[]"

        s = "["

        # Place random variables
        for i in range(len(self.rand_vars) - 1):
            s += self.rand_vars[i].name + ", "
        s += self.rand_vars[-1].name + "]"

        return s


class FactorRandVarsEx(Exception):
    """
    Exception use if the list of random variables is not a list or contains
    something other then random variables.
    """

    def __init__(self, bad_rand_vars):
        self.bad_rand_vars = bad_rand_vars

    def __str__(self):
        return "Bad Random Variables:" + repr(self.bad_rand_vars)


class FactorValuesEx(Exception):
    """
    If the list of values is not a list or contains something other then ints
    or floats.
    """

    def __init__(self, bad_values):
        self.bad_values = bad_values

    def __str__(self):
        return "Bad values for factor:" + repr(self.bad_values)
