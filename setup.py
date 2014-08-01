#!/usr/bin/env python3

from distutils.core import setup

setup(name="ProbPy",
      version="1.0",
      description="Probability Calculus Library",
      long_description=open('README.md').read(),
      license='LICENSE',

      author="Pedro Melgueira",
      author_email="pedromelgueira@gmail.com",

      url="https://github.com/petermlm/ProbPy",

      packages=["ProbPy", "ProbPy.tests", "ProbPy.examples"],
      )
