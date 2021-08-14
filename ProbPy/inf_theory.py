"""
File that implements Information Theory operations over factors
"""


import copy
from math import log

from ProbPy import Factor


def entropy(factor, base=2):
    """
    Calculates the entropy of a facto. If the factor represents the
    distribution P(X), returns entropy H(X). If the factor represents P(X, Y),
    returns the join entropy H(X, Y)

    :param factor: A factor for which the entropy is going to be calculated
    :param base:   The base of the logarithm in the operation. Default is 2
    :returns:      Returns the entropy
    """

    def ent(x):
        return x * log(x) / log(base) if x != 0 else 0

    return -sum(factor.map(ent).values)


def kullbackLeiblerDistance(fac1, fac2, base=2):
    """
    Calculates the Kullback-Leibler Distance between fac1 and fac2. The factors
    should represent probability distributions with the same variables, like
    P(X) and Q(X), or P(X, Y) and Q(X, Y)

    :param fac1: First factor in operation
    :param fac2: Second factor in operation
    :param base: Base of logarithms in the operations, defaults to 2
    :returns:    The Kullback-Leibler Distance
    """

    def kld(f1, f2):
        return f1 * log(f1 / f2) / log(base)

    return sum(Factor.factorOp(fac1, fac2, kld).values)


def mutualInformation(joint, fac1, fac2, base=2):
    """ """

    denom = fac1 * fac2
    return kullbackLeiblerDistance(joint, denom, base)
