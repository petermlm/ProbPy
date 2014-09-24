from ProbPy import MarkovNetwork, Event

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

    def sumProduct(self, query_var, observed=Event()):
        """
        An implementation of the Sum Product algorithms, also known as Belief
        propagation algorithm. The algorithm is used to infer the distribution
        of one query variable in a Markov Network

        :param query_var: RandVar Instance which is going to be inferred
        :param observed:  An event, instance of Event class, that represents
                          the observations made to the Markov Network. It may
                          be empty
        """

        # Get node of this var
        node = self.nodes[query_var.name]

        # Get neighboring factor nodes
        neighbor_factors = node.neighbors

        # Calculate product of neighboring messages to this node
        res = self.factorToVar(neighbor_factors[0], node.var, observed)
        for i in neighbor_factors[1:]:
            res *= self.factorToVar(i, node.var, observed)

        return res

    def factorToVar(self, node, var, observed):
        """
        Used by sumProduct, this method is used to calculate the messages that
        are passed from factor nodes to the variable node in the arguments.

        :param node:     A MarkovNetFactor node. The method will calculate the
                         message that this node passes to the variable in the
                         var argument
        :param var:      Instance of RandVar. The calculated message will pass
                         to the node representing this variable
        :param observed: An event sent from the sumProduct method
        """

        # Get neighboring var nodes
        neighbor_vars = [i for i in node.neighbors if i.var != var]

        # Calculate product of neighboring messages to this node
        res = None
        for i in neighbor_vars:
            vf_res = self.varToFactor(i, node.factor, observed)
            if vf_res is not None:
                if res is None:
                    res = vf_res
                else:
                    res *= vf_res

        # Calculate the product between this factor and the product of the
        # calculated messages
        if res is None:
            res = node.factor
        else:
            res *= node.factor

        # Get marginal and return resulting message
        return res.instVar(observed).marginal(var)

    def varToFactor(self, node, factor, observed):
        """
        Used by sumProduct, this method is used to calculate the messages that
        are passed from variable nodes to the factor node in the arguments.

        :param node:     A MarkovNetVar node. The method will calculate the
                         message that this node passes to the factor in the
                         factor argument
        :param factor:   Instance of Factor. The calculated message will pass
                         to the node representing this factor
        :param observed: An event sent from the sumProduct method
        """

        # Get neighboring factor nodes, except for argument node
        neighbor_factors = [i for i in node.neighbors if i.factor != factor]

        # If the list is empty, there is nothing to calculate in this node
        if neighbor_factors == []:
            return None

        # Otherwise, make the necessary products and return
        res = self.factorToVar(neighbor_factors[0], node.var, observed)
        for i in neighbor_factors[1:]:
            res *= self.factorToVar(i, node.var, observed)

        return res
