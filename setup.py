#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name="pipeline",
    version='v1.2.0',
    packages=find_packages(exclude=["test*.*", "tests"]),
)
