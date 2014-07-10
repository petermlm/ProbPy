"""
File that implements the Factor class
"""


from ProbPy.prob.rand_var import RandVar
import copy
import math


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
        :param rand_vars: List of Random Variables of this factor, or single
                          variable
        :param values:    Values of the factor
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
        """
        Multiplication operation for factorOp

        :param factor: Other factor in operation
        :returns: Result of operation
        """

        fun = lambda x, y: x*y
        return self.factorOp(factor, fun)

    def div(self, factor):
        """
        Division operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        fun = lambda x, y: x/y
        return self.factorOp(factor, fun)

    def add(self, factor):
        """
        Addition operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        fun = lambda x, y: x+y
        return self.factorOp(factor, fun)

    def sub(self, factor):
        """
        Subtraction operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        fun = lambda x, y: x-y
        return self.factorOp(factor, fun)

    def factorOp(self, factor, fun):
        """
        Function used by others to implement a factor operation between self
        and another factor.

        :param factor: The other factor used for this operation
        :param fun:    Operation used between each element of the values
        :returns:      Result of operation between self and factor using fun
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

        # Calculate dim list
        dim = []

        for i in range(len(factor.rand_vars)):
            dim.append(len(factor.rand_vars[i].domain))

        # Calculate resulting size of factor
        res_values_size = self.getValuesListSize(res_rand_vars)

        # Calculate resulting factor
        index1 = 0
        index2_range = range(len(factor.rand_vars))
        len_values = len(self.values)

        for i in range(res_values_size):
            # Get index 2
            index2 = 0
            for j in index2_range:
                index2 += (int(i / div[j]) % dim[j]) * mult[j]

            # Calculate value
            res_values.append(fun(self.values[index1], factor.values[index2]))

            # Increment index 1
            index1 = (index1 + 1) % len_values

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def scalar(self, factor, scalar_value, fun):
        """
        Scalar operation between factor and a scalar_value. The scalar is used
        in an operation, defined by fun, with the values of factor.

        :param factor:       The factor which values are going to be used as
                             operands with scalar
        :param scalar_value: An int or float value to serve as an operand
        :param fun:          Function used in the operation, may be a lambda
        :returns:            Result of mapping scalar_value to factor's values
                             using fun
        """

        map_res = []
        for i in factor.values:
            map_res.append(fun(i, scalar_value))

        return Factor(factor.rand_vars, list(map_res))

    def log(self, base):
        """
        Applies the logarithm function to the whole factor. The actual
        logarithm used in the one in Python's library

        :param base: Base of the logarithm
        :returns:    Apply the logarithm function with base given by parameter
                     to the values of self
        """

        fun = lambda x: math.log(x, base)
        return self.map(fun)

    def pow(self, p):
        """
        Calculates the power of the elements in the factor by p

        :param p: Values of power used
        :returns: Power of the elements in the factor by p
        """

        fun = lambda x: x**p
        return self.map(fun)

    def exp(self, base=None):
        """
        Applies the exp function to the whole factor. The base of exp is given
        by parameter. If omitted, the Exp implemented by Python's library is
        used

        :param base: The base of the exp
        :returns:    Exp function to the factor
        """

        if base is None:
            fun = lambda x: math.exp(x)
        else:
            fun = lambda x: base ** x

        return self.map(fun)

    def map(self, fun):
        """
        Returns the result of applying a function the factor. Used in the
        implementation of the log function, exp and power

        :param fun: Function used in the mapping
        :returns:   Result of applying fun to the factors values
        """

        map_res = []
        for i in self.values:
            map_res.append(fun(i))

        return Factor(self.rand_vars, list(map_res))

    def marginal(self, arg_rand_vars):
        """
        Calculates the marginal of a factor for a list of random variables.
        For example, if XY_factor is the distribution P(X, Y). Calculating the
        marginal of X will give P(X).

        :param arg_rand_vars: List of random variables that will make up the
                              returning factor
        :returns:             Marginal factor

        Examples:
            >>> # Assuming XYZ_factor as factor of P(X, Y, Z)
            >>> XY_factor = XYZ_factor.marginal([X, Y])
            >>> XY_factor # Will yield marginal P(X, Y)
            >>> X_factor = XYZ_factor.marginal(X)
            >>> X_factor # Will yield marginal P(X)
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
        P(X, Y), normalizing for X will yield P(X | Y), which would be similar
        to make the division P(X, Y) / P(Y) with the advantage that the
        distribution P(Y) doesn't need to be known or calculated before

        :param arg_rand_vars: List of random variables to normalize
        :returns:             Normalized factor

        Examples:
            >>> # Assuming XYZ_factor as factor of P(X, Y, Z)
            >>> XY_Z_factor = XYZ_factor.normalize([X, Y])
            >>> XY_Z_factor # Will yield conditional distribution P(X, Y | Z)
            >>> X_YZ_factor = XYZ_factor.normalize(X)
            >>> X_YZ_factor # Will yield conditional distribution P(X | Y, Z)
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

        :param rand_vars: List of variables to instantiate
        :param insts:     Value for each variable
        :returns:         Factor equivalent to self but lacking variables in
                          rand_vars, which were initialized

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

        :param rand_var: Variable to instantiate
        :param inst:     Value for variable
        :returns:        Factor with variable in rand_var instantiated
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
        len_domain = len(self.rand_vars[var_index].domain)
        for i in range(len(self.values)):
            if int(i/div) % len_domain == inst_index:
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

        :param fun: A function for the variable.
        :returns:   Expected value of factor

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
        """
        Returns true if the variable rand_var is in the factor's variables
        """

        for i in self.rand_vars:
            if i.name == rand_var.name:
                return True
        return False

    def getValuesListSize(self, rand_vars):
        """
        Calculates the size of the values list of a factor with the variables
        in rand_vars
        """

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

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mult(other)

    def __truediv__(self, other):
        return self.div(other)


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
