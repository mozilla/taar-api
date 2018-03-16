#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='taar_api',
    version='0.2dev',
    description='This is https://github.com/mozilla/taar_api',
    author='Mozilla Foundation',
    author_email='',
    url='https://github.com/mozilla/taar_api',
    packages=find_packages(exclude=['tests', 'tests/*']),
)
