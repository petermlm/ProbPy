#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Black
echo "Running Python Black:"
make black
echo "Done"

echo ""
echo ""

# Unit tests
echo "Unit Testing:"
make tests

echo ""
echo ""

# Examples
echo "Bayesian Theorem Example:"
python3 examples/bayes_theorem.py

echo ""
echo "Earthquake Script Example:"
python3 examples/earthquake.py

echo ""
echo "Wet Grass Example:"
python3 examples/wet_grass.py

echo ""
echo "Channel Capacity Example:"
python3 examples/channel_capacity.py

echo ""
echo "Variables and Factors Example:"
python3 examples/vars_factors_example.py
