"""
This is an example of using ProbPy to define a simple Bayesian Network and
executing the Elimination Ask algorithm. The network is defined like so:

B   E
 \ /
  A
 / \
J   M

Each node of the network corresponds with the following Random Variables:
 * Burglary - P(B)
 * Earthq   - P(E)
 * Alarm    - P(A | B, E)
 * John     - P(J | A)
 * Mary     - P(M | A)

Their distributions are bellow.
"""


from ProbPy.prob.rand_var import RandVar
from ProbPy.prob.factor import Factor
from ProbPy.prob import bn


# These are the variables in the network. The first argument is the actual name
# of the variable and the second is the domain of it
burglary = RandVar("burglary", ["True", "False"])
earthq = RandVar("earthq", ["True", "False"])
alarm = RandVar("alarm", ["True", "False"])
john = RandVar("john", ["True", "False"])
mary = RandVar("mary", ["True", "False"])

# These are the distributions. First argument are the variables, second is the
# values in the distribution
factor_burglary = Factor([burglary], [0.001, 0.999])
factor_earthq = Factor([earthq], [0.002, 0.998])
factor_alarm = Factor([alarm, earthq, burglary], [
    0.95, 0.05, 0.94, 0.06, 0.29, 0.71, 0.001, 0.999
])
factor_john = Factor([john, alarm], [0.90, 0.10, 0.05, 0.95])
factor_mary = Factor([mary, alarm], [0.70, 0.30, 0.01, 0.99])

# This array has the nodes of the network. Each element is a tuple. In each
# tuple, the first argument is the variable of that node, the second is the
# distribution, and the third is the list of parents of that node. Note that
# the nodes were place in the list at random
network = [
    (earthq,   factor_earthq,   []),
    (alarm,    factor_alarm,    [earthq,  burglary]),
    (john,     factor_john,     [alarm]),
    (burglary, factor_burglary, []),
    (mary,     factor_mary,     [alarm])
]

# The network object
BN = bn.BayesianNetwork(network)

# An array with observed values for some variables. In this example the
# variable john was observed being true. Same for variable mary
observed = [(john, "True"), (mary, "True")]

# Run the elimination ask algorithm (Variable Elimination) for the example.
# Result should be approximately [0.284, 0.716]
burglary_k_john_mary = BN.eliminationAsk(burglary, observed)

print("P(Burglary | John=true, Mary=true)")
print(burglary_k_john_mary.values)

print("----------")

# Another example with the same network. The observation and query variable
# changed, but the order of the distributions is the same. The result should
# be approximately [0.849, 0.150]

observed = [(burglary, "True")]
john_k_burglary = BN.eliminationAsk(john, observed)

print("P(John | Burglary=true)")
print(john_k_burglary.values)
