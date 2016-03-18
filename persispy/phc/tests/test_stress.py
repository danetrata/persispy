from ..points import phc
from ...point_cloud import PointCloud

import gc
from guppy import hpy

hp = hpy()
hp.setrelheap()
print hp.heap()
pc = phc(eqn= "x^2 + y^2 + z^2 - 1", num_points = 1000)
print pc
print hp.heap()

def test_1(pc):
    before = hp.heap()
    print before
    ng = pc.neighborhood_graph(0.1, method = "subdivision")
    print ng
    after = hp.heap()
    leftover = after - before
    print leftover


def main():
    gc.collect()


    before = hp.heap()
    print before
    test_1(pc)
    after = hp.heap()
    leftover = after - before
    print leftover

    gc.collect()  # don't care about stuff that would be garbage collected properly

    print "all tests have run"
    print leftover








if __name__== "__main__": main()

