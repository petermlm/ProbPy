import copy

class MarkovNetVar:
    """
    Represents a variable node in a Markov Network. Each variable node contains
    the random variable that the node represents itself and a list of neighbors
    which are made up of Factor nodes, that is, objects of the MarkovNetFactor
    class

    :param var: RandVar instance, which will be the variable that is
                represented in this node
    """

    def __init__(self, var):
        self.var = var
        self.neighbors = []
        self.messages = []

        self.marginal = None

    def addNeighbor(self, neighbor):
        """
        Adds a factor neighbor node to the list of neighbors

        :param neighbor: An instance of MarkovNetFactor that is a neighbor to
                         this node
        """

        if type(neighbor) == MarkovNetFactor:
            self.neighbors.append(neighbor)

    def getDegree(self):
        """
        Returns the graphical degree of this node
        """

        return len(self.neighbors)

    def setMarginal(self, marginal):
        self.marginal = copy.deepcopy(marginal)


class MarkovNetFactor:
    """
    Represents a factor node in a Markov Network. Each factor node contains the
    factor that the node represents itself and a list of neighbors which are
    made up of Variable nodes, that is, objects of the MarkovNetVar class

    :param factor: Factor instance, which will be the factor that is
                   represented in this node
    """
    def __init__(self, factor):
        self.factor = factor
        self.neighbors = []
        self.messages = []

    def addNeighbor(self, neighbor):
        """
        Adds a variable neighbor node to the list of neighbors

        :param neighbor: An instance of MarkovNetVar that is a neighbor to this
                         node
        """

        if type(neighbor) == MarkovNetVar:
            self.neighbors.append(neighbor)

    def getDegree(self):
        """
        Returns the graphical degree of this node
        """

        return len(self.neighbors)


class MarkovNetwork:
    """
    This class represents a simple Markov Network which is a bipartite graph.
    One of the groups of the graph is composed only of variable nodes, which
    are instances of the MarkovNetworkVar class, while the other is composed
    only of factor nodes, which are instances of the MarkovNetworkFactor class.

    The constructor of this class only takes a list of factors. The nodes of
    the representing graph are deduced automatically. The variables which make
    up the graph are also deduced automatically.

    Supposing the following Markov Network:::

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
        self.nodes = {}
        self.factors = []

        # Make dictionary with nodes
        for i in factors:
            for j in i.rand_vars:
                if j.name not in self.nodes:
                    self.nodes[j.name] = MarkovNetVar(j)

        # Make factors list
        for i in factors:
            # Node for factor
            new_factor_node = MarkovNetFactor(i)
            for j in i.rand_vars:
                new_factor_node.addNeighbor(self.nodes[j.name])
                self.nodes[j.name].addNeighbor(new_factor_node)

            self.factors.append(new_factor_node)
