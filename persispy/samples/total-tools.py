import matplotlib.pyplot as plt
import matplotlib as mpl
import persispy.weighted_simplicial_complex as wsc
import persispy.points as pp
import persispy.phc.interface as phci
import numpy.random as npr
import numpy as np
import hashlib as hashlib
import cProfile
import time

c=phci.phc_cloud(eqn = "x^2 + y^2 - 1",num_points=1000,return_complex=True,DEBUG=True)
# c=pp.sphere(1000,method='rejection')
g=c.neighborhood_graph(.01,method='exact')
print(g.connected_components_1())
print(g._adj)
