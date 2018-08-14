#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='taar_api',
    description='This is https://github.com/mozilla/taar_api',
    version='0.5.1',
    author='Mozilla Corporation',
    author_email='vng@mozilla.com',
    url='https://github.com/mozilla/taar_api',
    packages=find_packages(exclude=['tests', 'tests/*']),
)
