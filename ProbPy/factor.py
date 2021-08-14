"""
File that implements the Factor class
"""


from ProbPy import RandVar, Event

import copy
import math


class Factor:
    """
    Represents a Factor. A Factor has one or more random variables associated
    with an array of values. The array of values is a vectorization of the
    multi dimensional matrix that represents the factor.

    :param rand_vars: List of Random Variables of this factor, or a single
                      variable
    :param values:    Values of the factor

    Examples:
        >>> # Assuming X, Y, Z, A, B are variables
        >>> X_factor = Factor(X, [0.3, 0.7])
        >>> XY_factor = Factor([X, Y], [0.2, 0.3, 0.1, 0.4])
        >>> XYZ_factor = Factor([X, Y, Z], [[[0.2, 0.3], [0.1, 0.4]],
                                            [[0.7, 0.1], [0.1, 0.1]]])
        >>> AB_factor = Factor([A, B])
        >>> scalar = Factor([], 10)

    In the first two cases the factor is created with the variables in the
    first argument and the valeus given by a list. The third case uses a list
    of lists. In here the outer list is indexed by the first variable, the
    second innermost list is index by the second variable and so on.

    If no values are given, like in the fourth example, the values are built
    from the domain of the variables. For example if A has domain of 4 and B
    has domain of 6, the factor will have values:
        >>> list(range(4*6))

    Lastly, if the factor is a scalar factor, like the last example, the values
    may have a single integer.
    """

    def __init__(self, rand_vars, values=None):
        # Assure the rand_vars argument is always a list
        if type(rand_vars) != list:
            rand_vars = [rand_vars]

        # Check if the type of the variables is correct
        for i in rand_vars:
            if type(i) != RandVar:
                raise FactorRandVarsEx(rand_vars)

        # Store variables
        self.rand_vars = rand_vars

        # Check the types of the values
        if type(values) == list:
            if type(values[0]) == list:
                self.values = self.flattenList(values)

            else:
                for i in values:
                    if type(i) not in [int, float, bool]:
                        raise FactorValuesEx(rand_vars)

                self.values = values

        elif type(values) == int:
            self.values = [values]

        elif callable(values):
            self.values = self.makeValuesFromFunction(values)

        elif values is None:
            size = 1
            for i in self.rand_vars:
                size *= len(i.domain)
            self.values = list(range(size))

        else:
            raise FactorValuesEx(rand_vars)

        # Check if the size of the values is the
        size = 1
        for i in self.rand_vars:
            size *= len(i.domain)

        if size != len(self.values):
            raise FactorValuesEx(rand_vars)

    def flattenList(self, values):
        """
        Receives a list of lists and produces returns its flatten version.

        Supposing the list:
            >>> l = [[1, 2], [3, 4]]

        The flatten result would be:
            >>> fl = [1, 2, 3, 4]

        :param values: A list of lists
        :returns:      The flatten version of values
        """

        if type(values) in [int, float]:
            return [values]

        elif type(values) == list:
            res = []
            for i in values:
                res += self.flattenList(i)
            return res

        raise FactorValuesEx(rand_vars)

    def makeValuesFromFunction(self, values):
        # Initialize indexes.
        ind = [len(i.domain) for i in self.rand_vars]
        cind = [0] * len(self.rand_vars)
        cval = [i.domain[0] for i in self.rand_vars]

        # Increment cind and cval to next value
        def doInd(inc):
            # If inc is out of the bounds of the indexes, the end was reached
            if inc >= len(ind):
                return False

            # Move cind[inc] to next value
            cind[inc] += 1

            # If current cind is at the end, restart it and increment next
            if cind[inc] == ind[inc]:
                cind[inc] = 0
                cval[inc] = self.rand_vars[inc].domain[0]
                return doInd(inc + 1)

            # Also move the cval index
            cval[inc] = self.rand_vars[inc].domain[cind[inc]]

            return True

        # Make values array
        res = [values(*cval)]
        while doInd(0):
            res.append(values(*cval))

        return res

    def mult(self, factor):
        """
        Multiplication operation for factorOp

        :param factor: Other factor in operation
        :returns: Result of operation
        """

        return self.factorOp(factor, lambda x, y: x * y)

    def div(self, factor):
        """
        Division operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        return self.factorOp(factor, lambda x, y: x / y)

    def add(self, factor):
        """
        Addition operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        return self.factorOp(factor, lambda x, y: x + y)

    def sub(self, factor):
        """
        Subtraction operation for factorOp

        :param factor: Other factor in operation
        :returns:      Result of operation
        """

        return self.factorOp(factor, lambda x, y: x - y)

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

        for i in factor.rand_vars:
            dim.append(len(i.domain))

        # Calculate resulting size of factor
        res_values_size = self.getValuesListSize(res_rand_vars)

        # Calculate resulting factor
        index1 = 0
        len_values = len(self.values)

        for i in range(res_values_size):
            # Get index 1
            index1 = i % len_values

            # Get index 2
            index2 = 0
            for j, _ in enumerate(factor.rand_vars):
                index2 += (int(i / div[j]) % dim[j]) * mult[j]

            # Calculate value
            res_values.append(fun(self.values[index1], factor.values[index2]))

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def scalar(self, scalar_value, fun):
        """
        Scalar operation between the factor and a scalar_value. The scalar is
        used in an operation, defined by fun, with the values of the factor.

        :param scalar_value: An int or float value to serve as an operand
        :param fun:          Function used in the operation, may be a lambda
        :returns:            Result of mapping scalar_value to factor's values
                             using fun
        """

        return self.map(lambda x: fun(x, scalar_value))

    def log(self, base):
        """
        Applies the logarithm function to the whole factor. The actual
        logarithm used in the one in Python's library

        :param base: Base of the logarithm
        :returns:    Apply the logarithm function with base given by parameter
                     to the values of self
        """

        return self.map(lambda x: math.log(x, base))

    def pow(self, p):
        """
        Calculates the power of the elements in the factor by p

        :param p: Values of power used
        :returns: Power of the elements in the factor by p
        """

        return self.map(lambda x: x ** p)

    def exp(self, base=None):
        """
        Applies the exp function to the whole factor. The base of exp is given
        by parameter. If omitted, the Exp implemented by Python's library is
        used

        :param base: The base of the exp
        :returns:    Exp function to the factor
        """

        def fun(x):
            if base is None:
                return math.exp(x)
            return base ** x

        return self.map(fun)

    def map(self, fun):
        """
        Returns the result of applying a function the factor. Used in the
        implementation of the log function, exp and power

        :param fun: Function used in the mapping
        :returns:   Result of applying fun to the factors values
        """

        map_res = map(fun, self.values)
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
        for i, value in enumerate(self.values):
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

            res_values[index] += value

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def normalize(self, arg_rand_vars=None):
        """
        Normalizes the factor for random variables in the distribution. If the
        factor of variable X has values [1, 3], the normalization will yield
        the [1/4, 3/4], distribution. If a factor represents the distribution
        P(X, Y), normalizing for X will yield P(X | Y), which would be similar
        to make the division P(X, Y) / P(Y) with the advantage that the
        distribution P(Y) doesn't need to be known or calculated before

        :param arg_rand_vars: List of random variables to normalize. Default is
                              None. If the value is default, the list of
                              variables normalized will be equal to the factors
                              variables
        :returns:             Normalized factor

        Examples:
            >>> # Assuming XYZ_factor as factor of P(X, Y, Z)
            >>> XY_Z_factor = XYZ_factor.normalize([X, Y])
            >>> XY_Z_factor # Will yield conditional distribution P(X, Y | Z)
            >>> X_YZ_factor = XYZ_factor.normalize(X)
            >>> X_YZ_factor # Will yield conditional distribution P(X | Y, Z)


            >>> # Assuming fac to be a factor with an arbitrary number of
            >>> # variables, the following will make all values of the factor
            >>> # sum to a single scalar
            >>> fac.normalize()
        """

        marg_vars = []

        # If the argument is a single variable
        if arg_rand_vars is None:
            rand_vars = self.rand_vars
        elif type(arg_rand_vars) != list:
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

    def instVar(self, arg, value=None):
        """
        Instantiates variables of a factor. Instantiating variable X with value
        vx and Y with vy would yield f(X=vx, Y=vy, Z) = f(Z).

        :param arg:   This argument should be an Event object or contain a list
                      of tuples which represent a pair between a variable and a
                      value to be instantiated in the factor.
        :param value: If the first argument is not a list and is a single
                      variable, this argument should be it's value
        :returns:     Factor equivalent to self but lacking variables in
                      rand_vars, which were initialized

        The method may be used in three ways. First way is single var with
        single value:

            >>> # Suppose fX is the factor f(X)
            >>> fX.instVar(X, vx) # Would yield f(X=vx)

        Second is with an Event object:

            >>> # Suppose fXYZ is the factor f(X, Y, Z)
            >>> event = Event(tlist=[(X, vx), (Y, vy)])
            >>> fXYZ.instVar(event)
            >>> # Would yield f(X=vx, Y=vy, Z) = f(Z)

        Third is with a list of tuple where each tuple is a pair between a
        variable and value. This list is similar to the kind of list used in
        the definition of an event.

            >>> # Suppose fXYZ is the factor f(X, Y, Z)
            >>> fXYZ.instVar([(X, vx), (Y, vy)])
            >>> # Would yield f(X=vx, Y=vy, Z) = f(Z)
        """

        # Check if this is an instantiation of many variables by using only the
        # first argument as a list
        if type(arg) in [list, Event] and value is None:
            res = copy.copy(self)

            # Instantiate one variable at a time
            for i in arg:
                res = res.instVarSingle(i[0], i[1])

            return res

        # If this is actually a single variable instantiation
        else:
            return self.instVarSingle(arg, value)

    def instVarSingle(self, *args):
        """
        Same has instVar, but this method instantiates a single variable and
        it is the one used in the implementation of instVar.

        :param rand_var: Variable to instantiate
        :param inst:     Value for variable
        :returns:        Factor with variable in rand_var instantiated

        Examples:
            >>> # Suppose fXY is the factor f(X, Y)
            >>> fX.instVar(X, vx) # Would yield f(X=vx, Y) = f(Y)
        """

        res_rand_vars = []
        var_index = -1

        # Get arguments
        rand_var = args[0]
        inst = args[1]

        # Get resulting variables and var_index
        for i, rv in enumerate(self.rand_vars):
            # Store current index of variable to instantiate and add rest of
            # variables
            if rv.name == rand_var.name:
                var_index = i
                res_rand_vars += self.rand_vars[i + 1 :]
                break

            # Add current variable to list
            res_rand_vars.append(rv)

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
        for i, dom in enumerate(self.rand_vars[var_index].domain):
            if dom == inst:
                inst_index = i
                break

        # If the value for instance couldn't be found, return None
        if inst_index == -1:
            return None

        # Calculate resulting factor
        res_values = []
        len_domain = len(self.rand_vars[var_index].domain)
        for i, val in enumerate(self.values):
            if int(i / div) % len_domain == inst_index:
                res_values.append(val)

        # Make Factor object and return
        return Factor(res_rand_vars, res_values)

    def expectedValue(self, fun):
        """
        Calculates the expected value for the variables in rand_vars. The
        method should be used if the factor represents a probability
        distribution. Suppose the factor f(X) would represent the distribution
        P(X), this method would calculate the expected value of X, E[X].

        :param fun: A function for the variable.
        :returns:   Expected value of factor

        Examples:
            >>> X_factor = RandVar(X, ["T", "F"])
            >>> X_factor.Factor(X, [0.8, 0.2])
            >>> X_ev.Factor(X, [10, 20])
            >>> X_factor.expectedValue(X, X_ev)
            12.0
        """

        # Check if self and the function factor have the same variables
        if not self.sameVariables(fun):
            return None

        # Make the multiplication
        mult = self * fun

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

    def sameVariables(self, factor):
        """
        Checks if the variables in the factor are the same as the
        variables in self.
        """

        for i, rv in enumerate(self.rand_vars):
            f = False

            for f_rv in factor.rand_vars[i:]:
                if rv == f_rv:
                    f = True
                    break

            if not f:
                return False

        return True

    def euclideanDist(self, factor):
        """
        Calculates the euclidean distance between two factors. They need to
        have the same number of variables.

        :param factor: The other factor for the calculation
        :returns:      The euclidean distance
        """

        if not self.sameVariables(factor):
            return None

        diff = self.factorOp(factor, lambda x, y: (x - y) ** 2)
        return math.sqrt(sum(diff.values))

    def max(self):
        """
        Returns maximum values in factor
        """

        return max(self.values)

    def min(self):
        """
        Returns minimum values in factor
        """

        return min(self.values)

    def argmax(self):
        """
        Returns event with the greatest value

        :returns: Returns an Event object with the event that maximizes the
                  value of this factor
        """

        # Find the maximum value
        maxval = self.values[0]
        index = 0
        for i, value in enumerate(self.values, 1):
            if value > maxval:
                maxval = value
                index = i - 1

        # Make the event
        event = []
        div = 1
        for i, var in enumerate(self.rand_vars):
            doml = len(var.domain)
            val = int(index / div) % doml
            event.append((var, var.domain[val]))
            div *= len(var.domain)

        return Event(event)

    def argmin(self):
        """
        Returns event with the lesser value

        :returns: Returns an Event object with the event that minimizes the
                  value of this factor
        """

        # Find the maximum value
        minval = self.values[0]
        index = 0
        for i, value in enumerate(self.values, 1):
            if value < minval:
                minval = value
                index = i - 1

        # Make the event
        event = []
        div = 1
        for i, var in enumerate(self.rand_vars):
            doml = len(var.domain)
            val = int(index / div) % doml
            event.append((var, var.domain[val]))
            div *= len(var.domain)

        return Event(event)

    def __repr__(self):
        # If this is a scalar factor, meaning that there are no variables and
        # only on value, just return that value
        if len(self.rand_vars) == 0:
            return str(self.values)

        else:
            var_list = ""

            if len(self.rand_vars) == 1:
                var_list = self.rand_vars[0].name

            else:
                var_list = "["

                # Place random variables
                for i in self.rand_vars[:-1]:
                    var_list += str(i) + ", "
                var_list += str(self.rand_vars[-1].name) + "]"

            return "(%s, %s)" % (var_list, str(self.values))

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mult(other)

    def __truediv__(self, other):
        return self.div(other)

    def __eq__(self, other):
        # Check variables
        self.sameVariables(other)

        # Check values
        diff = self.factorOp(other, lambda x, y: x == y)

        for i in diff.values:
            if not i:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        return self.values[index]


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
