"""
File that implements Information Theory operations over factors
"""


import copy
import math


def entropy(factor, base=2):
    """
    Calculates the entropy of a facto. If the factor represents the
    distribution P(X), returns entropy H(X). If the factor represents P(X, Y),
    returns the join entropy H(X, Y)

    :param factor: A factor for which the entropy is going to be calculated
    :param base:   The base of the logarithm in the operation. Default is 2
    :returns:      Returns the entropy
    """

    res = 0

    for i in factor.values:
        # If i = 0 this would be 0 * log(0)
        if i != 0:
            res += i * math.log(i, base)

    return -res


def kullbackLeiblerDistance(fac1, fac2, base=2):
    """
    Calculates the Kullback-Leibler Distance between fac1 and fac2. The factors should represent
    probability distributions with the same variables, like P(X) and Q(X), or
    P(X, Y) and Q(X, Y)

    :param fac1: First factor in operation
    :param fac2: Second factor in operation
    :param base: Base of logarithms in the operations, defaults to 2
    :returns:    The Kullback-Leibler Distance
    """

    log_arg = fac1/fac2
    log_res = log_arg.log(base)
    to_sum = fac1 * log_res

    res = 0

    for i in to_sum.values:
        res += i

    return res
