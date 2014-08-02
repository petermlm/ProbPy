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
