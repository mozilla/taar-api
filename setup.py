#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='taar_api_lite',
    version='0.4.6',
    description=""" Flask webservice for deploying Mozilla taar-lite.
This is a fork of the previous Django webservice implementation.""",
    author='Mozilla Foundation',
    url='https://github.com/mozilla/taar-api-lite',
    packages=find_packages(exclude=['tests', 'tests/*']),
)
