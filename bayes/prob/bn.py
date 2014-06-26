"""
Contains
========

* BayesianNetworkNode
* BayesianNetwork
"""

from bayes.prob import factor

import copy


class BayesianNetworkNode:
    """
    This class represents a node in a Bayesian Network. It has the notion of
    it's variable, it's probability distribution represented using a factor and
    it's parents.
    """

    def __init__(self, node, factor, parents):
        """
        Constructor for the BayesianNetworkNode

        Arguments:
        node   -- A RandVar object, which is going to be this node's variable
        factor -- The factor which represents the distribution of this variable
                  in this node
        """

        self.node = node
        self.factor = factor
        self.parents = parents


class BayesianNetwork:
    """
    Class that implements a Bayesian Network. It encapsulates some algorithms
    for Bayesian inference and abstract their usage
    """

    def __init__(self, network):
        """
        Constructor for class BayesianNetwork

        Argument:
        network -- List of tuples, where each tuple represents a node. The
                   variable in each Node goes in the first element of the tuple
                   as a RandVar object. The factor for that variable goes into
                   the second element. The parents of the node go in  a list in
                   the third element of the tuple

        For example, suppose the following network:

         / -- Y -- \
        X           W
         \ -- Z -- /

        It's representation for this constructor would be:
        >>> network = [
        ...     (X, X_factor, [])
        ...     (Y, Y_factor, [X])
        ...     (Z, Z_factor, [X])
        ...     (W, W_factor, [Y, Z])
        ... ]

        Where the factors are:

        X_factor -- P(X)
        Y_factor -- P(Y | X)
        Z_factor -- P(Z | X)
        W_factor -- P(W | Y, Z)
        """

        self.network = []
        for i in network:
            node = BayesianNetworkNode(i[0], i[1], i[2])
            self.network.append(node)

    def nodeInGraph(self, node):
        """ Look for the node, if the node was not found, return None """

        # Look for the node
        for i in self.network:
            if node.name == i.node.name:
                return i

        # If the node was not found, return None
        return None

    def eliminationAsk(self, query_var, observed):
        """
        Executes the Elimination Ask algorithm, receiving a query variable (q)
        and observations (E), returning a factor which corresponds to the
        distribution P(q | E)

        Arguments:
        query_var -- Random variable of type RandVar
        observed  -- List of observations. Each element of the list should be
                     a tuple, which first element is a RandVar and second
                     element is the observed value for that variable

        Example:
            >>> # Assuming X, Y and Z as vars and vz, vy as values of X and Y
            >>> observed = [(X, vx), (Y, vy)]
            >>> res = BN.eliminationAsk(Z, observed)
            >>> res # P(Z | X=vx, Y=vy)
        """

        factors = []
        for i in self.network:
            # Append factor to factors list, removing observations
            factors.append(self.makeFactor(i.factor, observed))

            # If the variable is hidden sum it out of the factors
            if self.isHidden(i.node, query_var, observed):
                factors = self.sumOut(i.node, factors)

        # Calculate the product of every last factor
        prod = factors[0]
        for i in factors[1:]:
            prod = prod.mult(i)

        # Normalize and return
        res = prod.normalize(query_var)
        return res

    def makeFactor(self, arg_factor, observed):
        """
        Takes a factor and instantiates what is observed

        arg_factor -- Factor in question
        observed   -- Array with observations following the convention of
                    eliminationAsk method
        """

        fac = copy.deepcopy(arg_factor)

        for i in observed:
            res = fac.instVar(i[0], i[1])
            if res is not None:
                fac = res

        return fac

    def isHidden(self, var, query_var, observed):
        """
        Checks if the variable is the query variable or has any observation. If
        it doesn't, then the variable is hidden

        var       -- RandVar object with variable that is being tests if it's
                     hidden or not
        query_var -- Query variable for the algorithm
        observed  -- Array with observations following the convention of
                     eliminationAsk method
        """

        # If it is the query variable
        if var.name == query_var.name:
            return False

        # If it is observed
        for i in observed:
            if var.name == i[0].name:
                return False

        return True

    def sumOut(self, var, arg_factors):
        """
        Sums the variable in var out, meaning that this function will return
        the product of the factors in arg_factors and will take var out

        var         -- RandVar object that will be summed out
        arg_factors -- Factors which will have var summed out
        """

        # Calculate the product of factors
        prod = arg_factors[0]
        for i in arg_factors[1:]:
            prod = prod.mult(i)

        # Get variables for marginal
        marg_vars = []
        for i in prod.rand_vars:
            if i.name != var.name:
                marg_vars.append(i)

        # Return the final factor in the form of a list
        return [prod.marginal(marg_vars)]
