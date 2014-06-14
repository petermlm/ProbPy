from bayes import dist
from bayes import bn

# These are the variables in the network. The first argument is the actual name
# of the variable and the second is the domain of it
burglary = dist.RandVar("burglary", ["True", "False"])
earthq   = dist.RandVar("earthq", ["True", "False"])
alarm    = dist.RandVar("alarm", ["True", "False"])
john     = dist.RandVar("john", ["True", "False"])
mary     = dist.RandVar("mary", ["True", "False"])

# These are the distributions. First argument are the variables, second is the
# values in the distribution
dist_burglary = dist.Dist([burglary], [0.001, 0.999])
dist_earthq   = dist.Dist([earthq], [0.002, 0.998])
dist_alarm    = dist.Dist([alarm, earthq, burglary], [0.95, 0.05, 0.94, 0.06, 0.29, 0.71, 0.001, 0.999])
dist_john     = dist.Dist([john, alarm], [0.90, 0.10, 0.05, 0.95])
dist_mary     = dist.Dist([mary, alarm], [0.70, 0.30, 0.01, 0.99])

# This array has the nodes of the network. Each element is a tuple. In each
# tuple, the first argument is the variable of that node and the second is the
# distribution
network = [
    (mary,     dist_mary),
    (john,     dist_john),
    (alarm,    dist_alarm),
    (earthq,   dist_earthq),
    (burglary, dist_burglary)
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

