class RandVar:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return self.name

class Dist:
    def __init__(self, rand_vars, values):
        self.rand_vars = rand_vars
        self.values = values

    def mult(self, dist):
        f = lambda x, y: x*y
        return self.factorOp(dist, f)

    def div(self, dist):
        f = lambda x, y: x/y
        return self.factorOp(dist, f)

    def factorOp(self, dist, fun):
        res_rand_vars = []
        res_values = []

        # Res will have every variable in self
        for i in self.rand_vars:
            res_rand_vars.append(i)

        # And the variables in dist that are not in self
        for i in dist.rand_vars:
            var_in_self = True
            for j in self.rand_vars:
                if i.name == j.name:
                    var_in_self = False
                    break

            if var_in_self:
                res_rand_vars.append(i)

        # Calculate mult list
        mult = []
        c_mult = 1

        for i in dist.rand_vars:
            mult.append(c_mult)
            c_mult *= len(i.domain)

        # Calculate div list
        div = []

        for i in dist.rand_vars:
            c_div = 1

            for j in res_rand_vars:
                if i.name == j.name:
                    break

                c_div *= len(j.domain)

            div.append(c_div)

        # Calculate resulting size of distribution
        res_values_size = 1
        for i in res_rand_vars:
            res_values_size *= len(i.domain)

        # Calculate resulting distribution
        target1 = 0
        for i in range(res_values_size):
            target2 = 0
            for j in range(len(dist.rand_vars)):
                target2 += ((i / div[j]) % len(dist.rand_vars[j].domain)) * mult[j]

            res_values.append(fun(self.values[target1], dist.values[target2]))

            target1 = (target1 + 1) % len(self.values)

        # Make Dist object and return
        return Dist(res_rand_vars, res_values)

    def marginal(self, rand_vars):
        res_rand_vars = []

        # Get resulting variables
        for i in self.rand_vars:
            var_in_self = False

            for j in rand_vars:
                if i.name == j.name:
                    var_in_self = True
                    break

            if var_in_self:
                res_rand_vars.append(i)

        # Calculate resulting size of distribution
        res_values_size = 1
        for i in res_rand_vars:
            res_values_size *= len(i.domain)

        # Initialized Resulting distribution
        res_values = [0] * res_values_size

        # Calculate marginal
        for i in range(len(self.values)):
            target = 0
            div = 1
            mult = 1
            k = 0

            for j in self.rand_vars:
                if k < len(res_rand_vars) and j.name == res_rand_vars[k].name:
                    target += ((i / div) % len(res_rand_vars[k].domain)) * mult
                    mult *= len(res_rand_vars[k].domain)
                    k += 1

                div *= len(j.domain)

            res_values[target] += self.values[i]

        # Make Dist object and return
        return Dist(res_rand_vars, res_values)

    def instVar(self, rand_var, inst):
        # Get div factor
        div = 1
        for i in self.rand_vars:
            if i.name == rand_var:
                break
            div *= len(i.domain)

        # Get resulting variables and var_index
        res_rand_vars = []
        var_index = 0
        for i in range(len(self.rand_vars)):
            if self.rand_vars[i].name == rand_var:
                res_rand_vars += self.rand_vars[i+1:]
                var_index = i
                break
            res_rand_vars.append(self.rand_vars[i])

        # Get inst index
        for i in range(len(self.rand_vars[var_index].domain)):
            if self.rand_vars[var_index].domain[i] == inst:
                inst_index = i
                break

        # Calculate resulting
        res_values = []
        for i in range(len(self.values)):
            if (i/div) % len(self.rand_vars[var_index].domain) == inst_index:
                res_values.append(self.values[i])

        # Make Dist object and return
        return Dist(res_rand_vars, res_values)

    def normalize(self, rand_vars):
        # Get marginal
        marg = self.marginal(rand_vars)

        # Make division
        return self.div(marg)

