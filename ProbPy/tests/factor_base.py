from ProbPy.prob import factor


class FactorBase:
    def __init__(self):
        # Scalars
        self.scalar = 10
        self.scalarf = factor.Factor([], [10])

        # Binary variables
        self.X = factor.RandVar("X", ["T", "F"])
        self.Y = factor.RandVar("Y", ["T", "F"])
        self.Z = factor.RandVar("Z", ["T", "F"])
        self.W = factor.RandVar("W", ["T", "F"])
        self.K = factor.RandVar("K", ["T", "F"])
        self.T = factor.RandVar("T", ["T", "F"])

        # Factors
        self.X_factor = factor.Factor(self.X, list(range(1, 3)))
        self.Y_factor = factor.Factor(self.Y, list(range(3, 5)))
        self.Z_factor = factor.Factor(self.Z, list(range(5, 7)))

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
        self.X_factor_n = factor.Factor(self.X, [1, 2])
        self.XY_factor_n = factor.Factor([self.X, self.Y], [1, 1, 2, 2])
        self.XYZ_factor_n = factor.Factor([self.X, self.Y, self.Z],
                                          [1, 1, 2, 2, 3, 3, 4, 4])

        # Distributions for expected value
        self.X_dist = factor.Factor(self.X, [0.8, 0.2])
        self.Y_dist = factor.Factor(self.Y, [0.1, 0.9])
        self.XY_dist = factor.Factor([self.X, self.Y], [0.1, 0.2, 0.3, 0.4])

        # Function for expected values f(X)
        self.x_ev = factor.Factor(self.X, [10, 20])
        self.y_ev = factor.Factor(self.Y, [15, 25])
        self.xy_ev = factor.Factor([self.X, self.Y], [25, 35, 35, 45])
