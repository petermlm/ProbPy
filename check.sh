#!/bin/sh

# This script will run unit tests, check for conventions and run the examples.
# If anything is wrong after running this script, you should probably not
# commit your code.

# Unit tests
nosetests3

# PEP8
pep8 bayes/prob/*.py
pep8 bayes/tests/*.py

# Examples
python3 example.py

