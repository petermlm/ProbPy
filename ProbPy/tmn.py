from ProbPy import MarkovNetwork

class TreeMarkovNetwork(MarkovNetwork):
    def __init__(self, factors):
        super().__init__(factors)

        # TODO, nothing in this class assures that the network is a tree.

    def sumProduct(self, query_var):
        # Get node of this var
        node = self.nodes[query_var.name]

        # Get neighboring factor nodes
        neighbor_factors = node.neighbors
        print("+++", [i.factor for i in neighbor_factors])

        # Calculate product of neighboring messages to this node
        res = self.factorToVar(neighbor_factors[0], node.var)
        for i in neighbor_factors[1:]:
            res *= self.factorToVar(i, node.var)

        return res

    def factorToVar(self, node, var):
        # Get neighboring var nodes
        neighbor_vars = [i for i in node.neighbors if i.var != var]
        print("::", node.factor, " ---- ", [i.var for i in neighbor_vars if i.var != var])

        # Calculate product of neighboring messages to this node
        res = None
        for i in neighbor_vars:
            vf_res = self.varToFactor(i, node.factor)
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
        return res.marginal(var)

    def varToFactor(self, node, factor):
        # Get neighboring factor nodes, except for argument node
        neighbor_factors = [i for i in node.neighbors if i.factor != factor]
        print("--", node.var, " ---- ", [i.factor for i in neighbor_factors])

        # If the list is empty, there is nothing to calculate in this node
        if neighbor_factors == []:
            return None

        # Otherwise, make the necessary products and return
        res = self.factorToVar(neighbor_factors[0], node.var)
        for i in neighbor_factors[1:]:
            res *= self.factorToVar(i, node.var)

        return res
