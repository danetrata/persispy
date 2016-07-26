#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

def is_package(path): # find packages helper function
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
    )

def find_packages(path, base=""):
                                  #| given a path,
                                  #| recursively walks the directory to find
                                  #| submodules
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'numpy',
    'scipy'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='persispy',
    version='0.0.1',
    description="A python package for persistent homology.",
    long_description=readme + '\n\n' + history,
    packages=['persispy'],
    author="Benjamin Antieau",
    author_email='benjamin.antieau@gmail.com',
    url='https://github.com/benjaminantieau/persispy',
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
