from ProbPy import Factor


class BPMsg:
    """
    TODO
    """

    def __init__(self, factor, cycle=0):
        self.factor = factor
        self.cycle = cycle

    def __repr__(self):
        return "(Msg %s, Cycle: %s)" % (self.factor, self.cycle)


class MarkovNode:
    """
    TODO
    """

    def __init__(self):
        self.neighbors = []
        self.in_msgs = []
        self.out_msgs = []

    def addNeighbor(self, neighbor):
        """
        Adds a factor neighbor node to the list of neighbors

        :param neighbor: An instance of MarkovNetFactor that is a neighbor to
                         this node
        """

        self.neighbors.append(neighbor)
        self.in_msgs.append(None)
        self.out_msgs.append(None)

    def getDegree(self):
        """
        Returns the graphical degree of this node
        """

        return len(self.neighbors)


class MarkovNetVar(MarkovNode):
    """
    Represents a variable node in a Markov Network. Each variable node contains
    the random variable that the node represents itself and a list of neighbors
    which are made up of Factor nodes, that is, objects of the MarkovNetFactor
    class

    :param var: RandVar instance, which will be the variable that is
                represented in this node
    """

    def __init__(self, var, node_id=0):
        super().__init__()

        self.var = var
        self.node_id = node_id

        self.marginal = None

    def __repr__(self):
        return "{Variable Node: %s}" % (self.var.name)


class MarkovNetFactor(MarkovNode):
    """
    Represents a factor node in a Markov Network. Each factor node contains the
    factor that the node represents itself and a list of neighbors which are
    made up of Variable nodes, that is, objects of the MarkovNetVar class

    :param factor: Factor instance, which will be the factor that is
                   represented in this node
    """
    def __init__(self, factor, node_id=0):
        super().__init__()

        self.factor = factor
        self.node_id = node_id

    def __repr__(self):
        return "{Factor Node: %s}" % (self.factor)


class MarkovNetwork:
    """
    This class represents a simple Markov Network which is a bipartite graph.
    One of the groups of the graph is composed only of variable nodes, which
    are instances of the MarkovNetworkVar class, while the other is composed
    only of factor nodes, which are instances of the MarkovNetworkFactor class.

    The constructor of this class only takes a list of factors. The nodes of
    the representing graph are deduced automatically. The variables which make
    up the graph are also deduced automatically.

    Supposing the following Markov Network::

        A B
         \|
          X----Y--C
          |    |\/|
          |    |/\|
          Z----W--D

    One factor graph representation could be::

        A B
         \|
         f1--X--f2--Y  C
             |       \ |
             f3       f5
             |       / |
             Z--f4--W  D

    Each factor can be written like the following::

        f1 = f(A, B, X)
        f2 = f(X, Y)
        f3 = f(X, Z)
        f4 = f(Z, W)
        f5 = f(C, D, Y, W)

    The order of factors is not relevant in anyway.

    :param factors: A list of factors that make up the graph.
    """

    def __init__(self, factors):
        self.var_nodes = {}
        self.factor_nodes = []

        node_id = 0

        # Make dictionary with variable nodes
        for i in factors:
            for j in i.rand_vars:
                if j.name not in self.var_nodes:
                    self.var_nodes[j.name] = MarkovNetVar(j, node_id)
                    node_id += 1

        # Make list with factor nodes
        for i in factors:
            new_factor_node = MarkovNetFactor(i, node_id)
            node_id += 1

            for j in i.rand_vars:
                neighboring_var = self.var_nodes[j.name]

                new_factor_node.addNeighbor(neighboring_var)
                neighboring_var.addNeighbor(new_factor_node)

            self.factor_nodes.append(new_factor_node)

    def BeliefPropagation(self):
        # Calculate an initial outgoing message from every factor node
        for i, factor in enumerate(self.factor_nodes):
            msgs = []

            for j, neighbor in enumerate(factor.neighbors):
                fac = factor.factor.marginal(neighbor.var)
                msgs.out_msgs[j] = BPMsg(fac)

        # Propagate
        var_or_cycle = True
        cycle = 1
        for i in range(10):
            # Variable nodes cycle
            if var_or_cycle:
                self.BP_var(cycle)

            # Factor nodes cycle
            else:
                self.BP_factor(cycle)
                return

            # Change cycle
            var_or_cycle = not var_or_cycle
            cycle += 1

        # Calculate marginals

    def BP_factor(self, cycle):
        pass

    def BP_var(self, cycle):
        pass
