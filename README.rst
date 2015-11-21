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
========


* TODO



Contributing
============


Persispy
--------


We recommend installing with pip. The -e flag tells python that module will be edited frequently.

::

  pip install -e persispy 

An alternative to pip is to call the setup file directly. For a local installation, the --home flag tells to install to a particular directory. Be sure to append non-standard paths to your sys.path.

::

  sudo python setup.py develop [--home=~]

PHCpy
-----


First, we ensure the system has the tools to compile the shared libraries. The system will need the following packages:

* python2.7
* python-dev
* gnat-4.8

Clone from the remote PHCpack git repo.

::

  git clone https://github.com/callmetaste/PHCpack


Next, the shared library "phcpy2c.so" needs to be compiled on each and every system.
This fork is a stable release with of PHCpack a few changes to the setup so out-of-the-box installation on Unix is relatively easy.
For other systems, a line in makefile has to be commented correctly.
Also, the system makefile has absolute references, and any differences in system paths can cause an error.
Check your respective makefile matches system variables if any errors occur.

::

  make PHCpack/src/Objects/phcpyy2c.so

If all goes well, the very end of the compilation output will read that 
"phcpy2c.so" was successfully linked and copied. 

Finally, setup the "phcpy" module with

::

  pip install PHCpack/src/Python/PHCpy

or alternatively, we can again call the setup.py file with

::

  sudo python PHCpack/src/Python/PHCpy/setup.py install


