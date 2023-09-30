#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="ac",
    version="0.1",
    description="Audio cutter based on Dash",
    author="Mizaimao",
    packages=find_packages(include=["ac", "ac.*"]),
)
