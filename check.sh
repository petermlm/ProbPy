#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Unit tests
echo "Unit Testing:"
nosetests3

echo ""
echo ""

# PEP8
echo "PEP8 Checking:"
pep8 ProbPy/*.py
pep8 ProbPy/tests/*.py
pep8 ProbPy/examples/*.py
echo "Done"

echo ""
echo ""

# Examples
echo "Bayesian Theorem Example:"
python3 ProbPy/examples/bayes_theorem.py

echo ""
echo "Earthquake Script Example:"
python3 ProbPy/examples/earthquake.py

echo ""
echo "Wet Grass Example:"
python3 ProbPy/examples/wet_grass.py

echo ""
echo "Channel Capacity Example:"
python3 ProbPy/examples/channel_capacity.py
