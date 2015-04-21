import copy


from ProbPy import Factor


class BPMsg:
    """
    TODO
    """

    def __init__(self, factor, sender, receiver, cycle=0):
        self.factor = factor
        self.sender = sender
        self.receiver = receiver
        self.cycle = cycle

    def normalize(self):
        self.factor = self.factor.normalize()

    def __repr__(self):
        return "(Msg %s, (%s -> %s) , Cycle: %s)" % (self.factor, self.sender, self.receiver, self.cycle)


class MarkovNode:
    """
    TODO
    """

    def __init__(self, node_id):
        self.node_id = node_id
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

    def clearBP(self):
        nei_num = len(self.neighbors)
        self.in_msgs = [None] * nei_num
        self.out_msgs = [None] * nei_num


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
        super().__init__(node_id)

        self.var = var
        self.last_out_msgs = [None] * len(self.neighbors)
        self.marginal = None

    def clearBP(self):
        super().clearBP()
        self.last_out_msgs = [None] * len(self.neighbors)

    def putIn(self, msg, sender):
        for i, nei in enumerate(self.neighbors):
            if nei.node_id == sender:
                self.in_msgs[i] = msg
                break

    def calcOut(self, cycle):
        for i, nei in enumerate(self.neighbors):
            # If this neighbor has a message from this cycle, propagate it
            if self.in_msgs[i].cycle == cycle:
                # Send to node j
                for j, nei_j in enumerate(self.neighbors):
                    if i == j:
                        continue

                    msg = self.in_msgs[i].factor

                    for k, nei_k in enumerate(self.neighbors):
                        # Don't propagate to the same node, or the node where
                        # message is sent too
                        if k == i or k == j:
                            continue

                        msg *= self.in_msgs[k].factor
                        some_new = True

                    self.out_msgs[j] = BPMsg(msg, self.node_id, nei_j.node_id, cycle)
                    nei_j.putIn(self.out_msgs[j], self.node_id)

    def getOutMsg(self, receiver):
        for i in self.out_msgs:
            if i.receiver == receiver:
                return i

        return None

    def stopBPTree(self):
        for msg in self.out_msgs:
            if msg is not None:
                return False

        return True

    def stopBPLoop(self, ep):
        for i, msg in enumerate(self.out_msgs):
            if msg is None and self.last_out_msgs[i] is None:
                continue

            elif (msg is None) != (self.last_out_msgs[i] is None):
                return False

            dist = msg.factor.euclideanDist(self.last_out_msgs[i].factor)
            if not (dist < ep):
                return False

        return True

    def clearOutMsgsTree(self):
        nei_num = len(self.neighbors)
        self.out_msgs = [None] * nei_num

    def clearOutMsgsLoop(self):
        self.last_out_msgs = self.out_msgs
        nei_num = len(self.neighbors)
        self.out_msgs = [None] * nei_num

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
        super().__init__(node_id)

        self.factor = factor

    def putIn(self, msg, sender):
        for i, nei in enumerate(self.neighbors):
            if nei.node_id == sender:
                self.in_msgs[i] = msg
                break

    def calcOut(self, cycle):
        # If this is the first cycle, factor sends every message in every
        # direction
        if cycle == 0:
            for i, nei in enumerate(self.neighbors):
                msg_factor = self.factor.marginal(nei.var)
                out_msg = BPMsg(msg_factor, self.node_id, nei.node_id, cycle)

                self.out_msgs[i] = out_msg
                nei.putIn(out_msg, self.node_id)

        # Normal cycle
        else:
            for i, nei in enumerate(self.neighbors):
                # If this neighbor has a message from this cycle, propagate it
                if self.in_msgs[i] is not None and self.in_msgs[i].cycle == cycle-1:
                    # Send to node j
                    for j, nei_j in enumerate(self.neighbors):
                        if i == j:
                            continue

                        msg = self.in_msgs[i].factor

                        for k, nei_k in enumerate(self.neighbors):
                            # Don't propagate to the same node, or the node
                            # where message is sent too
                            if k == i or k == j:
                                continue

                            if self.in_msgs[k] is not None:
                                msg *= self.in_msgs[k].factor

                        msg = (self.factor * msg).marginal(nei_j.var)
                        self.out_msgs[j] = BPMsg(msg, self.node_id, nei_j.node_id, cycle)
                        nei_j.putIn(self.out_msgs[j], self.node_id)

    def getOutMsg(self, receiver):
        for i in self.out_msgs:
            if i.receiver == receiver:
                return i

        return None

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

        self.node_id = 0

        # Make dictionary with variable nodes
        for i in factors:
            self.addVariables(i.rand_vars)

        # Make list with factor nodes
        for i in factors:
            self.addFactor(i)

    def addVariables(self, variables):
        """
        TODO
        """
    
        for i in variables:
            if i.name not in self.var_nodes:
                self.var_nodes[i.name] = MarkovNetVar(i, self.node_id)
                self.node_id += 1

    def addFactor(self, factor):
        """
        TODO
        """

        new_factor_node = MarkovNetFactor(factor, self.node_id)
        self.node_id += 1

        for i in factor.rand_vars:
            neighboring_var = self.var_nodes[i.name]

            new_factor_node.addNeighbor(neighboring_var)
            neighboring_var.addNeighbor(new_factor_node)

        self.factor_nodes.append(new_factor_node)

    def addFactors(self, factors):
        """
        TODO
        """

        if type(factors) != list:
            factors = [factors]

        # Check if the variables in the factor are in the dictionary, add the
        # ones that aren't
        for i in factors:
            self.addVariables(i.rand_vars)

        # Add the factor
        for i in factors:
            self.addFactor(i)

    def BeliefPropagation(self, tree=False, ep=0.01):
        # Clear any values from previous execution of BP
        self.clearBP()

        # Propagate
        cycle = 0
        while True:
            self.BP_factor(cycle)
            self.BP_var(cycle)
            self.BP_normalize()

            if cycle > 0 and self.checkBreak(tree, ep):
                break

            self.BP_prepareNextCycle(tree)
            cycle += 1

        # Calculate marginals
        self.calcVarMarginals()

    def clearBP(self):
        for i in self.factor_nodes:
            i.clearBP()

        for i in self.var_nodes:
            self.var_nodes[i].clearBP()

    def BP_factor(self, cycle):
        for i in self.factor_nodes:
            i.calcOut(cycle)

    def BP_var(self, cycle):
        for i in self.var_nodes:
            self.var_nodes[i].calcOut(cycle)

    def checkBreak(self, tree, ep):
        return tree and self.stopBPTree() or \
                not tree and self.stopBPLoop(ep)

    def stopBPTree(self):
        for i in self.var_nodes:
            if not self.var_nodes[i].stopBPTree():
                return False

        return True

    def stopBPLoop(self, ep):
        for i in self.var_nodes:
            if not self.var_nodes[i].stopBPLoop(ep):
                return False

        return True

    def BP_prepareNextCycle(self, tree):
        for node in self.var_nodes:
            cnode = self.var_nodes[node]

            if tree:
                cnode.clearOutMsgsTree()
            else:
                cnode.clearOutMsgsLoop()

    def BP_normalize(self):
        for node in self.factor_nodes:
            for i, msg in enumerate(node.in_msgs):
                if msg is not None:
                    msg.normalize()

    def calcVarMarginals(self):
        for i in self.var_nodes:
            var = self.var_nodes[i]

            msg = var.in_msgs[0].factor
            for j in var.in_msgs[1:]:
                msg *= j.factor

            var.marginal = msg.normalize()
