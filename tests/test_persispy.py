#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_persispy
----------------------------------

Tests for `persispy` module.
"""

import unittest

"""
from persispy import persispy


class TestPersispy(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass
"""


from persispy.phc.points import phc
from persispy.points import sphere 

class TestPHCPack(unittest.TestCase):

    def setUp(self):
        self.points = 500


    def test_sampling_points_2sphere(self):

        selection = "x^2 + y^2 + z^2 - 1"
        pc = phc(eqn = selection, num_points = self.points, bounds = 30)

    def test_time_sampling_points(self):

        def wrapper():
            pc = sphere(self.points)

        def wrapper1():
            selection = "x^2 + y^2 + z^2 - 1"
            pc = phc(eqn = selection, num_points = self.points)

        print ""
        print "sphere(): %f" % t.timeit(wrapper, number = 10)
        print "phc():    %f" % t.timeit(wrapper1, number = 10)

    def test_time_sampling_points_complex(self):

#         def wrapper():

        def wrapper1():
            selection = "x^2 + y^2 + z^2 - 1"
            pc = phc(eqn = selection, num_points = self.points, return_complex = True)

        print ""
#         print "sphere(): %f" % t.timeit(wrapper, number = 10)
        print "phc():    %f" % t.timeit(wrapper1, number = 10)

import numpy.random as npr
from persispy.points import plane
import timeit as t
from time import sleep

class TestConnectedComponents(unittest.TestCase):
    
    def setUp(self):
        npr.seed(1991)
        pc = plane(200)
        self.ng = pc.neighborhood_graph(0.2)

    def test_time_cp(self):

        def wrapper():
            self.ng.connected_components()

        def wrapper1():
            self.ng.connected_components_1()

        print ""
        print ".connected_components():   %f" % t.timeit(wrapper, number = 10)
        print ".connected_components_1(): %f" % t.timeit(wrapper1, number = 10)

    def test_connected_components_equal_to_3(self):
        self.assertEqual(len(self.ng.connected_components()), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
