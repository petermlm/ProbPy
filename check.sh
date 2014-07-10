#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Unit tests
nosetests3

# PEP8
pep8 ProbPy/prob/*.py
pep8 ProbPy/tests/*.py
pep8 ProbPy/examples/*.py

# Examples
python3 -m ProbPy.examples.earthquake
python3 -m ProbPy.examples.bayes_theorem
python3 -m ProbPy.examples.channel_capacity
