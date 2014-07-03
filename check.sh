#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Unit tests
nosetests3

# PEP8
pep8 earthquake.py
pep8 bayes_theorem.py
pep8 ProbPy/prob/*.py
pep8 ProbPy/tests/*.py

# Examples
python3 earthquake.py
python3 bayes_theorem.py
