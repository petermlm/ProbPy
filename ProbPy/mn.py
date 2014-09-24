class MarkovNetVar:
    def __init__(self, var):
        self.var = var
        self.neighbors = []

    def addNeighbor(self, neighbor):
        if type(neighbor) == MarkovNetFactor:
            self.neighbors.append(neighbor)

    def getDegree(self):
        len(self.neighbors)


class MarkovNetFactor:
    def __init__(self, factor):
        self.factor = factor
        self.neighbors = []

    def addNeighbor(self, neighbor):
        if type(neighbor) == MarkovNetVar:
            self.neighbors.append(neighbor)

    def getDegree(self):
        len(self.neighbors)


class MarkovNetwork:
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
