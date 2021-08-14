"""
Implements the Parallel Factor class.
"""


from ProbPy import RandVar, Factor, Event

from multiprocessing import Process, Queue


class ParFactor(Factor):
    """
    Parallel factor is a child class of Factor with some operations
    reimplemented to execute in parallel. The usage of this class is in all
    similar to the Factor class. The difference is that operations done with
    this class will execute in parallel.

    :param factor:    Non parallel Factor. New factor will have the exact same
                      information, but it will now be a parallel class
    :param rand_vars: List of Random Variables of this factor, or single
                      variable
    :param values:    Values of the factor
    :param max_depth: Maximum recursion depth to which the algorithms can keep
                      creating processes

    Examples:
        >>> # Assuming X and Y are variables
        >>> XY_factor = Factor([X, Y], [0.2, 0.3, 0.1, 0.4])
        >>> ParFactor(factor=XY_factor)

    The new factor in the example above will the same but it will now execute
    some operations in parallel.

        >>> XY_factor = ParFactor([X, Y], [0.2, 0.3, 0.1, 0.4])

    The new factor will execute in parallel.
    """

    def __init__(self, rand_vars=None, values=None, factor=None, max_depth=0):
        if factor is not None:
            super().__init__(factor.rand_vars[:], factor.values[:])
        else:
            super().__init__(rand_vars, values)

        self.max_depth = max_depth

    def setMaxDepth(self, new_max_depth):
        """
        Maximum recursion depth to which the algorithms can keep creating
        processes

        :param new_max_depth: new maximum depth
        """

        self.max_depth = new_max_depth

    """
    Factor Op Stuff
    """

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

        # Get res div
        res_div = []
        c_res_div = 1
        for i in res_rand_vars:
            res_div.append(c_res_div)
            c_res_div *= len(i.domain)

        # Calculate resulting size of factor
        res_values_size = self.getValuesListSize(res_rand_vars)

        # Calculate resulting factor
        res_values = self.calcResFactor(
            mult,
            div,
            dim,
            res_div,
            factor.rand_vars,
            factor.values,
            res_rand_vars,
            res_values_size,
            fun,
            indexes=(0, 0, res_values_size),
        )
        return ParFactor(rand_vars=res_rand_vars, values=res_values)

    def getAuxLists(self, factor_rand_vars, res_rand_vars):
        """
        Only used internally with factorOp.
        """

        # Calculate mult list
        mult = []
        c_mult = 1

        for i in factor_rand_vars:
            mult.append(c_mult)
            c_mult *= len(i.domain)

        # Calculate div list
        div = []

        for i in factor_rand_vars:
            c_div = 1

            for j in res_rand_vars:
                if i.name == j.name:
                    break

                c_div *= len(j.domain)

            div.append(c_div)

        # Calculate dim list
        dim = []

        for i in factor_rand_vars:
            dim.append(len(i.domain))

        return mult, div, dim

    def calcResFactor(
        self,
        mult,
        div,
        dim,
        res_div,
        factor_rand_vars,
        factor_values,
        res_rand_vars,
        res_values_size,
        fun,
        arg_queue=None,
        indexes=(0, 0, -1),
        depth=0,
    ):
        """
        Only used internally with factorOp.
        """

        if depth <= self.max_depth and (depth + 1) <= len(div):
            top_var = res_rand_vars[-(depth + 1)]
            top_var_div = res_div[-(depth + 1)]

            # Generate a process for each value of the top variable
            queue = Queue()
            procs = []
            for i, _ in enumerate(top_var.domain):
                work_begin = i * top_var_div + indexes[1]
                work_end = work_begin + top_var_div

                p = Process(
                    target=ParFactor.calcResFactor,
                    args=(
                        self,
                        mult,
                        div,
                        dim,
                        res_div,
                        factor_rand_vars,
                        factor_values,
                        res_rand_vars,
                        res_values_size,
                        fun,
                        queue,
                        (i, work_begin, work_end),
                        depth + 1,
                    ),
                )
                p.start()
                procs.append(p)

            # Get results from processes
            ret_res_values = [0] * (indexes[2] - indexes[1])
            for i, _ in enumerate(top_var.domain):
                sub_res = queue.get()

                res_index = sub_res[0]
                res_list = sub_res[1]

                # Place sub list resulting from parallel processing into values
                # to return
                ret_res_values = (
                    ret_res_values[: res_index * top_var_div]
                    + res_list
                    + ret_res_values[res_index * top_var_div + top_var_div :]
                )

            # If this is the top process, return results, if not, put results
            # in queue
            if depth > 0:
                arg_queue.put((indexes[0], ret_res_values))
            else:
                return ret_res_values

        else:
            res_values = []
            len_values = len(self.values)

            final_index = indexes[0]
            work_begin = indexes[1]
            work_end = indexes[2] if indexes[2] != -1 else len(factor_values)

            index1 = 0
            for i in range(work_begin, work_end):
                # Get index 1
                index1 = i % len_values

                # Get index 2
                index2 = 0
                for j, _ in enumerate(factor_rand_vars):
                    index2 += (int(i / div[j]) % dim[j]) * mult[j]

                # Calculate value
                res_values.append(fun(self.values[index1], factor_values[index2]))

            # Put result in queue
            arg_queue.put((final_index, res_values))

    """
    Marginal Stuff
    """

    def marginal(self, arg_rand_vars):
        """
        Same as marginal() in Factor class, but implemented using Python's
        multiprocessing library

        :param arg_rand_vars: List of random variables that will make up the
                              returning factor
        :returns:             Marginal factor
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

        res_values = self.marginalPar(res_values_size, res_rand_vars)

        # Make Factor object and return
        return ParFactor(rand_vars=res_rand_vars, values=res_values)

    def marginalPar(
        self,
        res_values_size,
        res_rand_vars,
        arg_queue=None,
        indexes=(0, 0, -1),
        depth=0,
    ):
        """
        Only used internally for marginal.
        """

        if depth <= 1:
            # Divide the work through processes
            queue = Queue()

            if indexes[2] == -1:
                len_values = len(self.values)
            else:
                len_values = indexes[2] - indexes[1]

            begin_work = indexes[1]
            mid_index = indexes[1] + len_values // 2
            end_index = indexes[2] if indexes[2] != -1 else len_values

            p1 = Process(
                target=ParFactor.marginalPar,
                args=(
                    self,
                    res_values_size,
                    res_rand_vars,
                    queue,
                    (0, begin_work, mid_index),
                    depth + 1,
                ),
            )

            p2 = Process(
                target=ParFactor.marginalPar,
                args=(
                    self,
                    res_values_size,
                    res_rand_vars,
                    queue,
                    (1, mid_index, end_index),
                    depth + 1,
                ),
            )

            p1.start()
            p2.start()

            # Get results from processes
            res1 = queue.get()
            res2 = queue.get()

            final_res = []
            for i, _ in enumerate(res1[1]):
                final_res.append(res1[1][i] + res2[1][i])

            if depth > 0:
                arg_queue.put((indexes[0], final_res))
            else:
                return final_res

        else:
            final_index = indexes[0]
            begin = indexes[1]
            end = indexes[2]

            # Calculate marginal
            res_values = [0] * res_values_size
            for pre_i, value in enumerate(self.values[begin:end]):
                i = pre_i + begin
                index = 0
                div = 1
                mult = 1
                k = 0

                for j in self.rand_vars:
                    if k < len(res_rand_vars) and j.name == res_rand_vars[k].name:
                        rv_len = len(res_rand_vars[k].domain)
                        index += (int(i / div) % rv_len) * mult
                        mult *= len(res_rand_vars[k].domain)
                        k += 1

                    div *= len(j.domain)

                res_values[index] += value

            # Put results in queue
            arg_queue.put((final_index, res_values))
