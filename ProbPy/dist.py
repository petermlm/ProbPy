"""
TODO
"""


from ProbPy import RandVar, Factor

import copy


class Dist(Factor):
    def __init__(self, factor=None, left_vars=None, right_vars=None,
                 values=None):

        # If the argument used is a factor
        if factor is not None:
            # Check if there were any variables in left_vars argument. If there
            # weren't, assume every variable in factor is a left variable
            if left_vars is None:
                self.left_vars = factor.rand_vars[:]
                self.right_vars = []

            # If there were variables in left
            else:
                if type(left_vars) == RandVar:
                    self.left_vars = [left_vars]
                elif type(left_vars) == list:
                    self.left_vars = left_vars[:]
                else:
                    raise Exception

                # Check right variables store them if needed
                if right_vars is not None:
                    if type(right_vars) == RandVar:
                        self.right_vars = [right_vars]
                    elif type(right_vars) == list:
                        self.right_vars = right_vars[:]
                    else:
                        raise Exception
                else:
                    self.right_vars = []

            # Copy the factor
            # self.factor = copy.deepcopy(factor)
            Factor.__init__(self, factor.rand_vars, factor.values)

            # Check if the variables are not repeating
            vars_list = self.left_vars + self.right_vars
            for i in range(len(vars_list)):
                for j in range(i+1, len(vars_list)):
                    if vars_list[i].name == vars_list[j].name:
                        raise Exception

        # If there is no factor
        elif left_vars is not None and values is not None:
            # Make left vars list
            rand_vars = []
            if type(left_vars) == RandVar:
                self.left_vars = [left_vars]
            elif type(left_vars) == list:
                self.left_vars = left_vars[:]
            else:
                raise Exception

            # Make right vars list
            if right_vars is not None:
                if type(right_vars) == RandVar:
                    self.right_vars = [right_vars]
                elif type(right_vars) == list:
                    self.right_vars = right_vars[:]
                else:
                    raise Exception
            else:
                self.right_vars = []

            # Make rand_vars list for factor
            rand_vars = self.left_vars + self.right_vars

            # Build values array if it is not a list
            if type(values) is not list:
                values = self.makeValuesFromFunction(rand_vars, values)

            # Make factor
            # self.factor = Factor(rand_vars, values)
            Factor.__init__(self, rand_vars, values)

        else:
            raise Exception

    def makeValuesFromFunction(self, rand_vars, values):
        # Initialize indexes
        ind = [len(i.domain) for i in rand_vars]
        cind = [0] * len(rand_vars)
        cval = [i.domain[0] for i in rand_vars]

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
                cval[inc] = rand_vars[inc].domain[0]
                return doInd(inc+1)

            # Also move the cval index
            cval[inc] = rand_vars[inc].domain[cind[inc]]

            return True

        # Make values array
        res = [values(*cval)]
        while doInd(0):
            res.append(values(*cval))

        return res
