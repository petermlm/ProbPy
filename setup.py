#!/usr/bin/env python3

from distutils.core import setup
import sys

sys.path.append("ProbPy")
import ProbPy

setup(name="ProbPy",
      version="1.0",
      description="Multi Variable Probability Calculus Library",
      long_description=open('README.md').read(),

      author="Pedro Melgueira",
      author_email="pedromelgueira@gmail.com",

      url="https://github.com/petermlm/ProbPy",

      package_dir={"": "ProbPy"},
      py_modules=['ProbPy'],
      provides=['ProbPy'],

      keywords='probability calculus random variable bayes bayesian network \
               information theory',
      license="MIT License",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development'
                   ]
      )
