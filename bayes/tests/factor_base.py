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

        # Factors
        self.X_factor = factor.Factor([self.X], list(range(1, 3)))
        self.Y_factor = factor.Factor([self.Y], list(range(3, 5)))
        self.Z_factor = factor.Factor([self.Z], list(range(5, 7)))

        self.XY_factor = factor.Factor([self.X, self.Y], list(range(1, 5)))
        self.XZ_factor = factor.Factor([self.X, self.Z], list(range(5, 9)))
        self.ZW_factor = factor.Factor([self.Z, self.W], list(range(9, 13)))

        self.XYZ_factor = factor.Factor([self.X, self.Y, self.Z],
                                        list(range(1, 9)))
        self.XYW_factor = factor.Factor([self.X, self.Y, self.W],
                                        list(range(9, 17)))
        self.XKW_factor = factor.Factor([self.X, self.K, self.W],
                                        list(range(17, 25)))
        self.TKW_factor = factor.Factor([self.T, self.K, self.W],
                                        list(range(25, 33)))

        # Factors for normalization
        self.X_factor_n = factor.Factor([self.X], [1, 2])
        self.XY_factor_n = factor.Factor([self.X, self.Y], [1, 1, 2, 2])
        self.XYZ_factor_n = factor.Factor([self.X, self.Y, self.Z],
                                          [1, 1, 2, 2, 3, 3, 4, 4])

        # Expected value functions f(x)
        self.x_ev = [10, 20]
        self.y_ev = [15, 25]
        self.xy_ev = [10, 20, 30, 40]
