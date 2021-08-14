all:
	echo "make tests | black | setup"

.PHONY: tests
tests:
	nosetests

.PHONY: black
black:
	black ProbPy tests examples setup.py

.PHONY: setup
setup:
	python3 setup.py
