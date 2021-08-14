# Not needed if library is installed
from os import sys, path

sys.path.insert(0, path.join("..", "ProbPy"))

# Import ProbPy modules
from ProbPy import RandVar, Factor, Event
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
    factor_wet_grass = Factor(
        [wet_grass, rain, sprinkler], [0.99, 0.01, 0.9, 0.1, 0.9, 0.1, 0.0, 1.0]
    )

    # Actual network representation
    network = [
        (cloudy, factor_cloudy),
        (sprinkler, factor_sprinkler),
        (rain, factor_rain),
        (wet_grass, factor_wet_grass),
    ]

    # Create a Bayesian Network
    BN = bn.BayesianNetwork(network)

    # Set one observation
    observed = Event(var=sprinkler, val="True")

    # Run Rejection Sample algorithm
    estimate = BN.eliminationAsk(rain, observed)
    print("P(Rain | Sprinkler=true)")
    print(estimate)

    # Run Rejection Sample algorithm
    estimate = BN.rejectionSample(rain, observed, 1000)
    print("P(Rain | Sprinkler=true)")
    print(estimate)

    # Run Gibbs Ask algorithm
    estimate = BN.gibbsAsk(rain, observed, 1000)
    print("P(Rain | Sprinkler=true)")
    print(estimate)
