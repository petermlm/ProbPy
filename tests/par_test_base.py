from ProbPy import RandVar, ParFactor

from tests.test_base import TestBase


class ParTestBase(TestBase):
    def __init__(self):
        super().__init__()

        # Scalars
        self.par_scalarf = ParFactor(factor=self.scalarf)

        # Factors
        self.X_par_factor = ParFactor(factor=self.X_factor)
        self.Y_par_factor = ParFactor(factor=self.Y_factor)
        self.Z_par_factor = ParFactor(factor=self.Z_factor)

        self.XY_par_factor = ParFactor(factor=self.XY_factor)
        self.XZ_par_factor = ParFactor(factor=self.XZ_factor)
        self.ZW_par_factor = ParFactor(factor=self.ZW_factor)

        self.XYZ_par_factor = ParFactor(factor=self.XYZ_factor)
        self.XYW_par_factor = ParFactor(factor=self.XYW_factor)
        self.XKW_par_factor = ParFactor(factor=self.XKW_factor)
        self.TKW_par_factor = ParFactor(factor=self.TKW_factor)
