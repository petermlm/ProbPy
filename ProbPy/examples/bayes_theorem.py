"""
This is an example of the Bayes Theorem, in which to simple random variables
are used in the calculation, X and Y.
"""


from ProbPy import RandVar, Factor


if __name__ == "__main__":
    """
    Supposing the following example
    P(X | Y) P(Y) 1/P(X) = P(Y | X)
    """

    # Random Variables
    X = RandVar("X", ["T", "F"])
    Y = RandVar("Y", ["T", "F"])

    # Prior distribution, P(Y)
    fy = Factor(Y, [0.2, 0.8])

    # Conditional distribution, P(X | Y)
    fx_y = Factor([X, Y], [0.1, 0.9, 0.5, 0.5])

    # Bayes theorem to get P(Y | X)
    fy_x = (fx_y * fy).normalize(Y)

    print("P(X | Y) P(Y) 1/P(X) = P(Y | X)")
    print(fy_x, fy_x.values)

    # Alternative way of getting P(Y | X) without using the normalize() method
    fxy = fx_y * fy
    fx = fxy.marginal(X)
    fx_y = fxy / fx

    print("P(X | Y) P(Y) 1/P(X) = P(Y | X)")
    print(fx_y, fx_y.values)
