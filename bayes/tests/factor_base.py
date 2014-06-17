from bayes.prob import factor

class FactorBase:
    def __init__(self):
        # Scalar
        self.scalar = factor.Factor([], [10])

        # Binary variables
        self.X = factor.RandVar("X", ["T", "F"])
        self.Y = factor.RandVar("Y", ["T", "F"])
        self.Z = factor.RandVar("Z", ["T", "F"])
        self.W = factor.RandVar("W", ["T", "F"])
        self.K = factor.RandVar("K", ["T", "F"])
        self.T = factor.RandVar("T", ["T", "F"])

        # Factor distributions
        self.X_factor = factor.Factor([self.X], range(1, 3))
        self.Y_factor = factor.Factor([self.Y], range(3, 5))
        self.Z_factor = factor.Factor([self.Z], range(5, 7))

        self.XY_factor = factor.Factor([self.X, self.Y], range(1, 5))
        self.XZ_factor = factor.Factor([self.X, self.Z], range(5, 9))
        self.ZW_factor = factor.Factor([self.Z, self.W], range(9, 13))

        self.XYZ_factor = factor.Factor([self.X, self.Y, self.Z], range(1, 9))
        self.XYW_factor = factor.Factor([self.X, self.Y, self.W], range(9, 17))
        self.XKW_factor = factor.Factor([self.X, self.K, self.W], range(17, 25))
        self.TKW_factor = factor.Factor([self.T, self.K, self.W], range(25, 33))

