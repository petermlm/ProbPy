from ProbPy import MarkovNetwork, Factor


class TreeMarkovNetwork(MarkovNetwork):
    """
    This class is very similar to the MarkovNetwork class but only allows tree
    networks, meaning that cyclic networks aren't allowed. The constructor
    works in a similar way.

    :param factors: A list of factors that make up the graph.

    Alternatively, if the constructor is used with the keyword
    *markov_network*, it will simply take a MarkovNetwork instance and copy its
    variable and factor nodes.

    :param markov_network: Instance of MarkovNetwork.
    """

    def __init__(self, factors=None, markov_network=None):
        if factors is not None:
            super().__init__(factors)
        else:
            self.nodes = markov_network.nodes
            self.factors = markov_network.factors

        # TODO, nothing in this class assures that the network is a tree, yet

    def instNode(self, event):
        res = super().instNode(event)
        return TreeMarkovNetwork(markov_network=res)

    def beliefProp(self):
        """
        Belief propagation algorithm, also known as sum-product algorithm. The
        result of the algorithm is stored in the *marginal* attribute of every
        variable node which is part of the network. This implementation only
        works with tree networks.
        """

        # Select any root node
        root_node = self.nodes[next(iter(self.nodes))]

        # Get messages to this node
        res = self.factorToVar(root_node.neighbors[0], root_node)
        root_node.messages[0] = res

        for i, neighbor in enumerate(root_node.neighbors[1:]):
            msg = self.factorToVar(neighbor, root_node)
            root_node.messages[i + 1] = msg
            res *= msg

        for i in root_node.obs_factors:
            res *= i

        # Store the calculated marginal
        root_node.setMarginal(res)

        # Propagate this message to other nodes
        for i, neighbor in enumerate(root_node.neighbors):
            new_msg = Factor(root_node.var, [1, 1])

            for j in range(len(root_node.neighbors)):
                if i != j:
                    new_msg *= root_node.messages[j]

            for j in root_node.obs_factors:
                new_msg *= j

            self.progMsgVarToFactor(neighbor, root_node, new_msg)

    def factorToVar(self, node, prev_var):
        """
        Calculates initial message sent from every leaf node to the root node
        recursively. This method call deal with a message from a factor node to
        a variable node.

        :param node:     Node for which the message is going to be calculated.
        :param prev_var: Previous variable node in recursion.
        """

        # Get messages to this node
        res = None
        for i, neighbor in enumerate(node.neighbors):
            if neighbor.var != prev_var.var:
                msg = self.varToFactor(neighbor, node)
                if msg is not None:
                    if res is None:
                        res = msg
                    else:
                        res *= msg

                node.messages[i] = msg

        # Calculate the product between this factor and the product of the
        # calculated messages
        if res is None:
            res = node.factor
        else:
            res *= node.factor

        return res.marginal(prev_var.var)

    def varToFactor(self, node, prev_factor):
        """
        Calculates initial message sent from every leaf node to the root node
        recursively. This method call deal with a message from a variable node
        to a factor node.

        :param node:        Node for which the message is going to be
                            calculated.
        :param prev_factor: Previous factor node in recursion.
        """

        # Get messages to this node
        res = None
        for i, neighbor in enumerate(node.neighbors):
            if neighbor.factor != prev_factor.factor:
                msg = self.factorToVar(neighbor, node)
                if msg is not None:
                    if res is None:
                        res = msg
                    else:
                        res *= msg

                node.messages[i] = msg

        if len(node.obs_factors) > 0:
            if res is None:
                res = node.obs_factors[0]
            else:
                res *= node.obs_factors[0]

            for i in node.obs_factors[1:]:
                res *= i

        # Return this message
        return res

    def progMsgVarToFactor(self, node, prev_var, msg):
        """
        Propagates message from root node to every other node recursively. This
        method call deals with step from a variable node to a factor node.

        :param node:     Node that receives message. Message is also propagated
                         from this node to other nodes except for prev_var
                         node.
        :param prev_var: Previous variable node during message propagation.
        :param msg:      Message from previous nodes to this one.
        """

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
        """
        Propagates message from root node to every other node recursively. This
        method call deals with step from a factor node to variable node.

        :param node:        Node that receives message. Message is also
                            propagated from this node to other nodes except for
                            prev_factor node.
        :param prev_factor: Previous factor node during message propagation.
        :param msg:         Message from previous nodes to this one.
        """

        marginal = msg
        for i, neighbor in enumerate(node.neighbors):
            if node.messages[i] is not None:
                marginal *= node.messages[i]

        for i in node.obs_factors:
            marginal *= i

        node.setMarginal(marginal)

        # Propagate this message to other nodes
        for i, neighbor in enumerate(node.neighbors):
            new_msg = msg

            for j, nn in enumerate(node.neighbors):
                if i != j and node.messages[j] is not None:
                    new_msg *= node.messages[j]

            for j in node.obs_factors:
                new_msg *= j

            if neighbor.factor != prev_factor.factor:
                self.progMsgVarToFactor(neighbor, node, new_msg)
