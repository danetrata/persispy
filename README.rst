===============================
persispy
===============================

.. image:: https://img.shields.io/travis/benjaminantieau/persispy.svg
        :target: https://travis-ci.org/benjaminantieau/persispy

.. image:: https://img.shields.io/pypi/v/persispy.svg
        :target: https://pypi.python.org/pypi/persispy


A python package for persistent homology including visualization.

* Free software: GNU GPL v3
* Documentation: https://persispy.readthedocs.org.

Features
--------

* TODO



Contributing
------------

Persispy
==

Recommended:
Run 

  pip install -e persispy 

to make persispy available system wide. This is especially important for 
development work when testing in iPython. 
Alternate: 
Run 

  sudo python setup.py develop

if local:
  python setup.py develop --home=~

to tell python this module has code that will change frequently.

PHCpy
==

First, ensure the system has the tools to compile the shared libraries. The 
system will need the following packages:
python2.7
python-dev
gnat-4.8

The shared library "phcpy2c.so" needs to be compiled on each and every 
system. Clone from the remote

  git clone https://github.com/callmetaste/PHCpack

This is a stable release with a few changes to the setup so out-of-the-box
installation on Unix is relatively easy. For other systems, a line in makefile
has to be commented correctly. Also, the system makefile has absolute
references, and any differences in system paths can cause an error. Check your
respective makefile if any errors occur.

  make PHCpack/src/Objects/phcpyy2c.so

If all goes well, the very end of the compilation output will read that 
"phcpy2c.so" was successfully linked and copied. 

Finally, setup the "phcpy" module with

  pip install PHCpack/src/Python/PHCpy

or alternatively,

  sudo python PHCpack/src/Python/PHCpy/setup.py install


