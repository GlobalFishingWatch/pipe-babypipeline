#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name="pipe-babypipeline",
    version="1.3.0",
    packages=find_packages(exclude=["test*.*", "tests"]),
)
