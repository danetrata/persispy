from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
import objgraph

def test_1():
    phc(eqn = "x^2 - y", DEBUG=True)
    phc(eqn = "x^2 + y^2 - 1", DEBUG=True)
    phc(eqn = "x^2 + y^3 - 1", DEBUG=True)
    phc(eqn = "x^2 + y^2 + z^2 - 1", DEBUG=True)
    phc(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
    phc(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
    phc(eqn = "x^2 + y^3 - 1", DEBUG=True, bounds=6)
    
def test_2():
    pc = phc(eqn = "x^2 + y^2 - 1", num_points = 10)
    print pc
    print type(pc)
    print pc.points
    print type(pc.points)


def test_3():
    pc = phc(eqn= "x^2 + y^2 + z^2 - 1", num_points = 100, return_complex = True)
    ng = pc.neighborhood_graph(0.2)
    cp = ng.connected_components_1()
    print pc
    print ng
    print cp

def test_3_ng():
    pc = phc(eqn= "x^3 + y^3 + z^3 - 1", num_points = 5)
    print pc
    ng = pc.neighborhood_graph(1, "subdivision")
    print ng
    cp = ng.connected_components_1()
    print cp

#     pc.plot2d_neighborhood_graph(0.2)
#     pc.plot3d_neighborhood_graph(0.2)


def test_4():
    pc = phc(eqn= "x^2 + y^2 + z^2 - 1", num_points = 2000)
    pc = phc(eqn= "x^3 + y^3 + z^3 - 1", num_points = 1000)
    ng = pc.neighborhood_graph(0.1, "subdivision")
    print ng
    cp = ng.connected_components_1()
    print cp
    pc.plot2d_neighborhood_graph(0.2)
    pc.plot3d_neighborhood_graph(0.2)


from guppy import hpy
import gc

def main():
    gc.collect()
    hp = hpy()
    hp.setrelheap()

#     test_1()
#     test_2()

    before = hp.heap()
    print before
    test_3()
    after = hp.heap()
    leftover = after - before
    print leftover

#     before = hp.heap()
#     test_3_3()
#     after = hp.heap()
#     leftover = after - before
#     print leftover
#     print leftover.rp

    gc.collect()
    
#     before = hp.heap()
#     test_4()
#     after = hp.heap()
#     leftover = after - before

    print "all tests have run"
    print leftover

    gc.collect()  # don't care about stuff that would be garbage collected properly

#     import objgraph
#     objgraph.show_most_common_types()
#     objgraph.show_refs(pc)






if __name__== "__main__": main()

