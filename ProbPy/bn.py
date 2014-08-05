"""
Implementation of a Bayesian Network with some algorithms
"""


from ProbPy import Factor

import copy
import random


class BayesianNetworkNode:
    """
    This class represents a node in a Bayesian Network. It has the notion of
    it's variable, it's probability distribution represented using a factor and
    it's parents.

    Arguments:
    :param node:    A RandVar object, which is going to be this node's variable
    :param factor:  The factor which represents the distribution of this
                    variable in this node
    """

    def __init__(self, node, factor):
        self.node = node
        self.factor = factor
        self.parents = [i for i in factor.rand_vars if i.name != node.name]

        # Used in the construction of the Bayesian Network class while sorting
        self.visited = 0


class BayesianNetwork:
    """
    Class that implements a Bayesian Network. It encapsulates some algorithms
    for Bayesian inference and abstract their usage

    :param network: List of tuples, where each tuple represents a node. The
                    variable in each Node goes in the first element of the
                    tuple as a RandVar object. The factor for that variable
                    goes into the second element.

    For example, suppose the following network::

        X --- Y --- W
         \ -- Z -- /

    It's representation for this constructor would be:

        >>> network = [
        ...     (X, X_factor)
        ...     (Y, Y_factor)
        ...     (Z, Z_factor)
        ...     (W, W_factor)
        ... ]

    Where the factors are::

        X_factor -- P(X)
        Y_factor -- P(Y | X)
        Z_factor -- P(Z | X)
        W_factor -- P(W | Y, Z)
    """

    def __init__(self, network):
        # Will have nodes after they are topologically sorted
        self.network = []

        # List of unsorted nodes
        unsorted_net = [BayesianNetworkNode(i[0], i[1]) for i in network]
        self.topoSortNet(unsorted_net)

    def topoSortNet(self, unsorted_net):
        # Keep number of unvisited nodes
        self.un_num = len(unsorted_net)

        # Visit procedure for the sorted algorithm
        def visit(n):
            # If this has temporary mark, stop. Not a DAG
            if n.visited == 1:
                raise BayesianNetworkArgEx()

            # If it has not been visited
            if n.visited == 0:
                # Mark temporally
                n.visited = 1

                # Find node that connects with this one and visited
                for i in unsorted_net:
                    for j in i.parents:
                        if n.node.name == j.name:
                            visit(i)

                # Mark this node has visited, add it to sorted network
                self.un_num -= 1
                n.visited = 2
                self.network.insert(0, n)

        # Sort nodes
        while self.un_num > 0:
            # Select unmarked
            n = None
            for i in unsorted_net:
                if i.visited == 0:
                    n = i
                    break

            # Visited
            visit(n)

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

        :param query_var: Random variable of type RandVar
        :param observed:  List of observations. Each element of the list should
                          be a tuple, which first element is a RandVar and
                          second element is the observed value for that
                          variable

        Example:
            >>> # Assuming X, Y and Z as vars and vz, vy as values of X and Y
            >>> observed = [(X, vx), (Y, vy)]
            >>> res = BN.eliminationAsk(Z, observed)
            >>> res # P(Z | X=vx, Y=vy)
        """

        rev_network = self.network[:]
        rev_network.reverse()

        factors = []
        for i in rev_network:
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

        :param arg_factor: Factor in question
        :param observed:   Array with observations following the convention of
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

        :param var:       RandVar object with variable that is being tests if
                          it's hidden or not
        :param query_var: Query variable for the algorithm
        :param observed:  Array with observations following the convention of
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

        :param var:         RandVar object that will be summed out
        :param arg_factors: Factors which will have var summed out
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

    def sample(self, pre_inst=None):
        """
        Returns a random sample of the network in the form of a list of tuples.
        Each tuple is a pair between a random variable and it's instance, in
        the form:

            >>> ret = [(X, "T"), (Y, "F")]

        :param pre_inst: Default=None. Should be a list of tuples. Each tuple
                         is a pair between a random variable and a value of
                         it's domain. That value will be the value in the
                         sample instead of leaving it to random chance.
        """

        net = self.network[:]
        inst_vars = []

        for i in net:
            insted = i.factor.instVar(inst_vars)
            var = insted.rand_vars[0]

            in_pre_inst = False
            for j in pre_inst:
                if i.node.name == j[0].name:
                    val = j[1]
                    in_pre_inst = True

            if not in_pre_inst:
                val = self.pickRandomValue(var.domain, insted.values,
                                           random.random())

            inst_vars.append((var, val))

        return inst_vars

    def pickRandomValue(self, domain, values, prob):
        """
        Method used with sample(). This method picks one element of the domain
        of a random variable given it's parameters.
        """

        value = values[0]
        for i in range(len(domain)):
            if value > prob:
                return domain[i]
            value += values[i]

        return domain[-1]

    def rejectionSample(self, query_var, observed, samples_num):
        """
        Implementation of the rejection sample algorithm. This algorithms
        estimates a distribution P(X | e), where X is a query variable and e
        are observations made in the network.

        :param query_var:   Random variable of type RandVar
        :param observed:    List of observations. Each element of the list
                            should be a tuple, which first element is a RandVar
                            and second element is the observed value for that
                            variable
        :param samples_num: Number of samples the algorithm is going to take to
                            calculate the estimative
        """

        # List of counts for each value of the domain. Initialized with 0
        count = {i: 0 for i in query_var.domain}

        # The samples_num of samples
        for i in range(samples_num):
            # Take a sample
            sample = self.sample()

            # Check if it should be rejected
            rejected = False
            for j in observed:
                for k in sample:
                    # If the value of the sampled variable is different from
                    # the value of the observed one, rejected
                    if j[0].name == k[0].name and j[1] != k[1]:
                        rejected = True
                        break

                # If the sample was already rejected, get out of the cycle
                if rejected:
                    break

            # If the sample is not rejected, increment the counts
            if not rejected:
                for j in sample:
                    if j[0].name == query_var.name:
                        count[j[1]] += 1

        # Make resulting factor
        values = [count[i] for i in query_var.domain]
        return Factor([query_var], values).normalize(query_var)


class BayesianNetworkArgEx(Exception):
    """
    Exception used if the nodes of the Bayesian Network don't form a DAG
    """

    def __str__(self):
        s = ("Nodes for the construction of the Bayesian Network don't form a"
             "Direct Acyclic Graph")
        return s
