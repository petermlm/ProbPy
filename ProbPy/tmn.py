from ProbPy import MarkovNetwork, Factor


class TreeMarkovNetwork(MarkovNetwork):
    """
    This class is very similar to the MarkovNetwork class but only allows tree
    networks, meaning that cyclic networks aren't allowed. The constructor
    works in a similar way.

    :param factors: A list of factors that make up the graph.
    """

    def __init__(self, factors):
        super().__init__(factors)

        # TODO, nothing in this class assures that the network is a tree, yet

    def beliefProp(self):
        # Dictionary from node to list of messages to key node
        self.msg_node = {}

        # Select any root node
        root_node = self.nodes[next(iter(self.nodes))]

        # Get messages to this node
        res = self.factorToVar(root_node.neighbors[0], root_node)
        self.msg_node[root_node.var.name] = [(res, root_node.neighbors[0].factor)]
        for i in root_node.neighbors[1:]:
            msg = self.factorToVar(i, root_node)
            self.msg_node[root_node.var.name].append((msg, i.factor))
            res *= msg

        # Store the calculated marginal
        root_node.setMarginal(res)

        # Propagate this message to other nodes
        for i in root_node.neighbors:
            new_msg = Factor(root_node.var, [1, 1])

            for j in self.msg_node[root_node.var.name]:
                if j[1] != i.factor:
                    new_msg *= j[0]

            self.progMsgVarToFactor(i, root_node, new_msg)

    def factorToVar(self, node, prev_var):
        # Get neighboring var nodes
        neighbor_vars = [i for i in node.neighbors if i.var != prev_var.var]

        # Get messages to this node
        res = None
        for i in neighbor_vars:
            msg = self.varToFactor(i, node)
            if msg is not None:
                if res is None:
                    res = msg
                else:
                    res *= msg

        # Calculate the product between this factor and the product of the
        # calculated messages
        if res is None:
            res = node.factor
        else:
            res *= node.factor

        return res.marginal(prev_var.var)

    def varToFactor(self, node, prev_factor):
        # Get neighboring factor nodes
        neighbor_factors = [i for i in node.neighbors if i.factor != prev_factor.factor]

        # Get messages to this node
        res = None
        for i in neighbor_factors:
            msg = self.factorToVar(i, node)
            if msg is not None:
                if node.var.name in self.msg_node:
                    self.msg_node[node.var.name].append((msg, i))
                else:
                    self.msg_node[node.var.name] = [(msg, i)]

                if res is None:
                    res = msg
                else:
                    res *= msg

        # Return this message
        return res

    def progMsgVarToFactor(self, node, prev_var, msg):
        # Get neighboring factor nodes
        neighbor_vars = [i for i in node.neighbors if i.var != prev_var.var]

        # Propagate this message to other nodes
        for i in neighbor_vars:
            self.progMsgFactorToVar(i, node, msg)

    def progMsgFactorToVar(self, node, prev_factor, msg):
        if node.var.name == 'B':
            print(msg)

        # Calculate the marginal for this node and store it
        this_msg = (msg * prev_factor.factor).marginal(node.var)
        res = this_msg
        if node.var.name in self.msg_node:
            for i in self.msg_node[node.var.name]:
                res *= i[0]

        node.setMarginal(res)

        # Get neighboring factor nodes
        neighbor_factors = [i for i in node.neighbors if i.factor != prev_factor.factor]

        # Propagate this message to other nodes
        for i in neighbor_factors:
            new_msg = this_msg

            for j in self.msg_node[node.var.name]:
                if j[1] != i:
                    new_msg *= j[0]

            self.progMsgVarToFactor(i, node, new_msg)
