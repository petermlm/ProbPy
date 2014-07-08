from ProbPy.prob.rand_var import RandVar
from ProbPy.prob.factor import Factor


class FactorBase:
    def __init__(self):
        # Scalars
        self.scalar = 10
        self.scalarf = Factor([], [10])

        # Binary variables
        self.X = RandVar("X", ["T", "F"])
        self.Y = RandVar("Y", ["T", "F"])
        self.Z = RandVar("Z", ["T", "F"])
        self.W = RandVar("W", ["T", "F"])
        self.K = RandVar("K", ["T", "F"])
        self.T = RandVar("T", ["T", "F"])

        # Domains
        self.X_domain = list(range(1, 3))
        self.Y_domain = list(range(3, 5))
        self.Z_domain = list(range(5, 7))

        self.XY_domain = list(range(1, 5))
        self.XZ_domain = list(range(5, 9))
        self.ZW_domain = list(range(9, 13))

        self.XYZ_domain = list(range(1, 9))
        self.XYW_domain = list(range(9, 17))
        self.XKW_domain = list(range(17, 25))
        self.TKW_domain = list(range(25, 33))

        # Factors
        self.X_factor = Factor(self.X, self.X_domain)
        self.Y_factor = Factor(self.Y, self.Y_domain)
        self.Z_factor = Factor(self.Z, self.Z_domain)

        self.XY_factor = Factor([self.X, self.Y], self.XY_domain)
        self.XZ_factor = Factor([self.X, self.Z], self.XZ_domain)
        self.ZW_factor = Factor([self.Z, self.W], self.ZW_domain)

        self.XYZ_factor = Factor([self.X, self.Y, self.Z], self.XYZ_domain)
        self.XYW_factor = Factor([self.X, self.Y, self.W], self.XYW_domain)
        self.XKW_factor = Factor([self.X, self.K, self.W], self.XKW_domain)
        self.TKW_factor = Factor([self.T, self.K, self.W], self.TKW_domain)

        # Factors for normalization
        self.X_factor_n = Factor(self.X, [1, 2])
        self.XY_factor_n = Factor([self.X, self.Y], [1, 1, 2, 2])
        self.XYZ_factor_n = Factor([self.X, self.Y, self.Z],
                                   [1, 1, 2, 2, 3, 3, 4, 4])

        # Distributions for expected value
        self.X_dist = Factor(self.X, [0.8, 0.2])
        self.Y_dist = Factor(self.Y, [0.1, 0.9])
        self.XY_dist = Factor([self.X, self.Y], [0.1, 0.2, 0.3, 0.4])

        # Function for expected values f(X)
        self.x_ev = Factor(self.X, [10, 20])
        self.y_ev = Factor(self.Y, [15, 25])
        self.xy_ev = Factor([self.X, self.Y], [25, 35, 35, 45])
