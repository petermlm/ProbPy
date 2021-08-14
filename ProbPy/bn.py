"""
Implementation of a Bayesian Network with some algorithms
"""


from ProbPy import Factor, Event

import copy
import random


TS_Unvisited = 0
TS_Processing = 1
TS_Visited = 2


class BayesianNetworkNode:
    """
    This class represents a node in a Bayesian Network. It has the notion of
    it's variable, it's probability distribution represented using a factor and
    it's parents.

    :param node:    A RandVar object, which is going to be this node's variable
    :param factor:  The factor which represents the distribution of this
                    variable in this node
    """

    def __init__(self, node, factor):
        # Attributes of network node
        self.node = node
        self.factor = factor
        self.parents = []

        # Used in the construction of the Bayesian Network class
        self.visited = TS_Unvisited
        self.parent_vars = [i for i in factor.rand_vars if i.name != node.name]


class BayesianNetwork:
    """
    Class that implements a Bayesian Network. It encapsulates some algorithms
    for Bayesian inference and abstract their usage

    :param network: List of tuples, where each tuple represents a node. The
                    variable in each Node goes in the first element of the
                    tuple as a RandVar object. The factor for that variable
                    goes into the second element.

    For example, suppose the following network, in which every edge would be
    pointing from left to right::

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

    def __init__(self, network=[]):
        # Will have nodes after they are topologically sorted
        self.network = []

        # List of unsorted nodes
        unsorted_net = [BayesianNetworkNode(i[0], i[1]) for i in network]
        self.topoSortNet(unsorted_net)

    def topoSortNet(self, unsorted_net):
        # Visit procedure for the sort algorithm
        def visit(cnode):
            # If this has temporary mark, stop. Not a DAG
            if cnode.visited == TS_Processing:
                raise BayesianNetworkArgEx()

            # If it has not been visited
            if cnode.visited == TS_Unvisited:
                # Mark temporally
                cnode.visited = TS_Processing

                # Find node that connects with this one and visit them
                for i in unsorted_net:
                    for j in i.parent_vars:
                        if cnode.node.name == j.name:
                            # Add current node to parents of found node and
                            # visit it
                            i.parents.append(cnode)
                            visit(i)

                # Mark node as visited and add it to sorted list network
                cnode.visited = TS_Visited
                self.network.insert(0, cnode)

        # Sort nodes
        for i in unsorted_net:
            if i.visited == TS_Unvisited:
                visit(i)

    def nodeInGraph(self, node):
        """Look for the node, if the node was not found, return None"""

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
        :param observed:  Instance of Event class, or a list of tuples

        The Event class can be used to make the observations, but it is also
        possible to use a list of observations like the ones used to define an
        Event.

        Example using the event class and the list or observations.

        Without Event class:

            >>> # Assuming X, Y and Z as vars and vz, vy as values of X and Y
            >>> observed = [(X, vx), (Y, vy)]
            >>> res = BN.eliminationAsk(Z, observed)
            >>> res # P(Z | X=vx, Y=vy)

        With Event class:

            >>> observed = Event(tlist=[(X, vx), (Y, vy)])
            >>> res = BN.eliminationAsk(Z, observed)
            >>> res # P(Z | X=vx, Y=vy)

        Another with Event class:

            >>> observed = Event()
            >>> observed.setValue(X, vx)
            >>> observed.setValue(Y, vy)
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
        Returns a random sample of the network in the form of an Event. An
        event will contain a list of tuples. Each tuple is a pair between a
        random variable and it's instance, in the form:

            >>> ret = [(X, "T"), (Y, "F")]

        :param pre_inst: Default=None. Should be a list of tuples. Each tuple
                         is a pair between a random variable and a value of
                         it's domain. That value will be the value in the
                         sample instead of leaving it to random chance.
        """

        net = self.network[:]
        inst_vars = Event()

        for i in net:
            insted = i.factor.instVar(inst_vars)
            var = i.node

            if pre_inst is not None:
                val = pre_inst.value(i.node)

            if pre_inst is None or val is None:
                val = self.pickRandomValue(var.domain, insted.values, random.random())

            inst_vars.setValue(var, val)

        return inst_vars

    def pickRandomValue(self, domain, values, prob):
        """
        Method used with sample(). This method picks one element of the domain
        of a random variable given it's parameters.
        """

        value = values[0]
        for i, dom in enumerate(domain):
            if value > prob:
                return dom
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

    def markovBlanket(self, node):
        """
        Returns a list containing the nodes that make up the Markov Blanket to
        the node in the argument.

        :paran node: The node for which the Markov Blanket is to be
                     calculated. Should be an instance of
                     BayesianNetworkNode
        :return:     A list with nodes that make up the Markov Blanket
        """

        # Get parents
        parents = node.parents

        # Get Children
        children = []
        for i in self.network:
            if node in i.parents:
                children.append(i)

        # Get children's parents
        child_parents = []
        for i in children:
            child_parents += [
                j for j in i.parents if j != node and j not in parents + children
            ]

        return parents + children + child_parents

    def gibbsAsk(self, query_var, observed, samples_num):
        # Result is a list of counts for each value in the domain of the query
        # variable. Initialized with 0
        res = {i: 0 for i in query_var.domain}

        # Assure the observed argument is an Event
        if type(observed) != Event:
            observed = Event(observed)

        # Create non evidence variable list, which are all the variables not
        # present in the observations
        non_evidence_vars = [i for i in self.network if not observed.varInEvent(i.node)]

        # Get markov blankets for each non evidence variable
        mbs = dict()
        for i in non_evidence_vars:
            mbs[i.node.name] = self.markovBlanket(i)

        # Make an initial sample
        sample = self.sample(observed)

        # Execute for samples_num samples
        for i in range(samples_num):
            for j in non_evidence_vars:
                # Get distribution P(j | mb(j))
                dist = j.factor
                for k in mbs[j.node.name]:
                    dist *= k.factor

                # Instantiate with previous sample, except for current j
                # variable
                sample.removeVar(j.node)
                dist = dist.instVar(sample)

                # Set new random value of current variable in sample
                rvalue = self.pickRandomValue(
                    dist.rand_vars[0].domain, dist.values, random.random()
                )
                sample.setValue(j.node, rvalue)

                # Increment count
                res[rvalue] += 1

        # Return the count list normalized
        values = [res[i] for i in query_var.domain]
        return Factor(query_var, values).normalize(query_var)

    def instNode(self, event):
        """
        Makes observation over a network creating a new network in which every
        factor containing one of the observed variables gets instantiated

        Supposing the network (The edges would be "pointing" from top to bottom
        since this is a Bayesian Network)::

            X  Y
            |\ |
            | A
            |/ |
            W  Z

        The factors that describe this network are the following::

            P(X)        = f(X)
            P(Y)        = f(Y)
            P(A | X, Y) = f(A, X, Y)
            P(W | X, A) = f(W, X, A)
            P(Z | A)    = f(Z, A)

        If the A variable is observed, every factor will have its A variable
        instantiated and the network will be composed of the following factors,
        which don't have any A variable::

            f(X)
            f(Y)
            f(A=a, X, Y) = f'(X, Y)
            f(W, X, A=a) = f'(W, X)
            f(Z, A=a)    = f'(Z)

        Or similarly, if X is instantiated::

            f(X=x)       = scalar
            f(Y)
            f(A, X=x, Y) = f'(A, Y)
            f(W, X=x, A) = f'(W, A)
            f(Z, A)      = f'(Z, A)

        Note that the node which only contained X will be reduced to a single
        scalar value.
        """

        # Resulting network list
        res_network = []

        # Assure the event argument is an Event object
        if type(event) != Event:
            event = Event(event)

        # Take each node and instantiate it's factor according to the event
        for i in self.network:
            new_node = BayesianNetworkNode(i.node, i.factor.instVar(event))
            new_node.parents = i.parents
            res_network.append(new_node)

        # Create the network and place the new list directly in the
        # attribute because it is already sorted
        res = BayesianNetwork()
        res.network = res_network
        return res


class BayesianNetworkArgEx(Exception):
    """
    Exception used if the nodes of the Bayesian Network don't form a DAG
    """

    def __str__(self):
        s = (
            "Nodes for the construction of the Bayesian Network don't form a"
            "Direct Acyclic Graph"
        )
        return s
