from bayes.bayes import factor
from bayes.bayes import bn

# These are the variables in the network. The first argument is the actual name
# of the variable and the second is the domain of it
burglary = factor.RandVar("burglary", ["True", "False"])
earthq   = factor.RandVar("earthq", ["True", "False"])
alarm    = factor.RandVar("alarm", ["True", "False"])
john     = factor.RandVar("john", ["True", "False"])
mary     = factor.RandVar("mary", ["True", "False"])

# These are the distributions. First argument are the variables, second is the
# values in the distribution
factor_burglary = factor.Dist([burglary], [0.001, 0.999])
factor_earthq   = factor.Dist([earthq], [0.002, 0.998])
factor_alarm    = factor.Dist([alarm, earthq, burglary], [0.95, 0.05, 0.94, 0.06, 0.29, 0.71, 0.001, 0.999])
factor_john     = factor.Dist([john, alarm], [0.90, 0.10, 0.05, 0.95])
factor_mary     = factor.Dist([mary, alarm], [0.70, 0.30, 0.01, 0.99])

# This array has the nodes of the network. Each element is a tuple. In each
# tuple, the first argument is the variable of that node and the second is the
# distribution
network = [
    (mary,     factor_mary),
    (john,     factor_john),
    (alarm,    factor_alarm),
    (earthq,   factor_earthq),
    (burglary, factor_burglary)
]

# The network object
BN = bn.BayesianNetwork(network)

# An array with observed values for some variables. In this example the
# variable john was observed being true. Same for variable mary
observed = [("john", "True"), ("mary", "True")]

# Run the elimination_ask algorithm (Variable Elimination) for the example.
# Result should be approximately [0.284, 0.716]
burglary_k_john_mary = BN.elimination_ask(burglary, observed)
print(burglary_k_john_mary.values)
