# Not needed if library is installed
from os import sys, path

sys.path.insert(0, path.join("..", "ProbPy"))
from ProbPy import *


# Various ways to declare variables
coin = RandVar("Coin", ["Head", "Tail"])
ball = RandVar("Ball", ["Red", "Green", "Blue"])
generic = RandVar(10, list(range(10)))
X = RandVar("X", 4)
Y = RandVar("Y")
Anon1 = RandVar("_anonymous", [True, False])
Anon2 = RandVar(domain=[True, False])

# Execute to see their output
print(coin)
print(ball)
print(generic)
print(X)
print(Y)
print(Anon1)
print(Anon2)

# Variables to be used next
X = RandVar("X", [True, False])
Y = RandVar("Y", [True, False])
Z = RandVar("Z", [True, False])
A = RandVar("A", 4)
B = RandVar("B", 6)

# Also, various ways to declare factors
X_factor = Factor(X, [0.3, 0.7])
XY_factor = Factor([X, Y], [0.2, 0.3, 0.1, 0.4])
XYZ_factor = Factor([X, Y, Z], [[[0.2, 0.3], [0.1, 0.4]], [[0.7, 0.1], [0.1, 0.1]]])
AB_factor = Factor([A, B])
scalar = Factor([], 10)

# Check output of factors
print(X_factor)
print(XY_factor)
print(XYZ_factor)
print(AB_factor)
print(scalar)
