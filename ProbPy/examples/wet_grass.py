from ProbPy import RandVar, Factor
from ProbPy import bn

if __name__ == "__main__":
    # Variables for this example
    cloudy = RandVar("cloudy", ["True", "False"])
    sprinkler = RandVar("sprinkler", ["True", "False"])
    rain = RandVar("rain", ["True", "False"])
    wet_grass = RandVar("wet_grass", ["True", "False"])

    # Factors representing the conditional distributions of this network
    factor_cloudy = Factor(cloudy, [0.5, 0.5])
    factor_sprinkler = Factor([sprinkler, cloudy], [0.1, 0.9, 0.5, 0.5])
    factor_rain = Factor([rain, cloudy], [0.8, 0.2, 0.2, 0.8])
    factor_wet_grass = Factor([wet_grass, rain, sprinkler],
                              [0.99, 0.01, 0.9, 0.1, 0.9, 0.1, 0.0, 1.0])

    # Actual network representation
    network = [
        (cloudy,    factor_cloudy,    []),
        (sprinkler, factor_sprinkler, [cloudy]),
        (rain,      factor_rain,      [cloudy]),
        (wet_grass, factor_wet_grass, [rain, sprinkler])
    ]

    # Create a Bayesian Network
    BN = bn.BayesianNetwork(network)

    # Run Rejection Sample with the following observations
    observed = [(sprinkler, "True")]
    estimate = BN.rejectionSample(rain, observed, 1000)

    print("P(Rain | Sprinkler=true)")
    print(estimate.values)
