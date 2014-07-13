#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Unit tests
nosetests3

# PEP8
pep8 ProbPy/prob/*.py
pep8 ProbPy/tests/*.py
pep8 examples/*.py

# Examples
python3 examples/earthquake.py
python3 examples/bayes_theorem.py
python3 examples/channel_capacity.py
