from ..phc.points import phc
from ...point_cloud import PointCloud

import gc
from guppy import hpy


pc = phc(eqn= "x^2 + y^2 + z^2 - 1", num_points = 10000)
print pc

ng = pc.neighborhood_graph(0.15, method = "subdivision")
print ng

def test_1():
    cp = ng.connected_components_1()
    print cp


def main():
    hp = hpy()
    hp.setrelheap()
    print hp.heap()
    for x in range(100):
        before = hp.heap()
        test_1()
        after = hp.heap()
        leftover = after - before
        print leftover

    gc.collect()  # don't care about stuff that would be garbage collected properly

    print "all tests have run"
    print leftover








if __name__== "__main__": main()

