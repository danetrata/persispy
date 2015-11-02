#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setuptools
from setuptools import setup
print "setup using setuptools"

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='persispy',
    version='0.0.1',
    description="A python package for persistent homology.",
    long_description=readme + '\n\n' + history,
    author="Benjamin Antieau",
    author_email='benjamin.antieau@gmail.com',
    url='https://github.com/benjaminantieau/persispy',
    packages = setuptools.find_packages(),
    platforms='any',
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='persispy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL v2',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
