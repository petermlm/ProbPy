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
        # Select any root node
        root_node = self.nodes[next(iter(self.nodes))]

        # Get messages to this node
        res = self.factorToVar(root_node.neighbors[0], root_node)
        root_node.messages.append(res)

        for i in root_node.neighbors[1:]:
            msg = self.factorToVar(i, root_node)
            root_node.messages.append(msg)
            res *= msg
        print("::", root_node.messages)

        # Store the calculated marginal
        root_node.setMarginal(res)

        # Propagate this message to other nodes
        for i, neighbor in enumerate(root_node.neighbors):
            new_msg = Factor(root_node.var, [1, 1])

            for j in range(len(root_node.neighbors)):
                if i != j:
                    new_msg *= root_node.messages[j]

            self.progMsgVarToFactor(neighbor, root_node, new_msg)

    def factorToVar(self, node, prev_var):
        # Get messages to this node
        res = None
        for i in node.neighbors:
            if i.var != prev_var.var:
                msg = self.varToFactor(i, node)
                if msg is not None:
                    if res is None:
                        res = msg
                    else:
                        res *= msg

                node.messages.append(msg)
            else:
                node.messages.append(None)
        print(";;", node.factor, node.messages)

        # Calculate the product between this factor and the product of the
        # calculated messages
        if res is None:
            res = node.factor
        else:
            res *= node.factor

        return res.marginal(prev_var.var)

    def varToFactor(self, node, prev_factor):
        # Get messages to this node
        res = None
        for i in node.neighbors:
            if i.factor != prev_factor.factor:
                msg = self.factorToVar(i, node)
                if msg is not None:
                    if res is None:
                        res = msg
                    else:
                        res *= msg

                node.messages.append(msg)

            else:
                node.messages.append(None)
        print("--", node.var, node.messages)

        # Return this message
        return res

    def progMsgVarToFactor(self, node, prev_var, msg):
        # Propagate this message to other nodes
        for i, neighbor in enumerate(node.neighbors):
            new_msg = msg

            for j, nn in enumerate(node.neighbors):
                if i != j and node.messages[j] is not None:
                    new_msg *= node.messages[j]

            if neighbor.var != prev_var.var:
                new_msg = (node.factor * new_msg).marginal(neighbor.var)
                self.progMsgFactorToVar(neighbor, node, new_msg)

    def progMsgFactorToVar(self, node, prev_factor, msg):
        marginal = msg
        for i, neighbor in enumerate(node.neighbors):
            if node.messages[i] is not None:
                marginal *= node.messages[i]

        node.setMarginal(marginal)

        # Propagate this message to other nodes
        for i, neighbor in enumerate(node.neighbors):
            new_msg = msg

            for j, nn in enumerate(node.neighbors):
                if i != j and node.messages[j] is not None:
                    new_msg *= node.messages[j]

            if neighbor.factor != prev_factor.factor:
                self.progMsgVarToFactor(neighbor, node, new_msg)
