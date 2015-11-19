from persispy.phc.points import phc
from persispy.point_cloud import PointCloud

def test_1():
#     phc(eqn = "x^2 - y", DEBUG=True)
    phc(eqn = "x^2 + y^2 - 1", DEBUG=True)
#     phc(eqn = "x^2 + y^3 - 1", DEBUG=True)
#     phc(eqn = "x^2 + y^2 + z^2 - 1", DEBUG=True)
#     phc(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
#     phc(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
#     phc(eqn = "x^2 + y^3 - 1", DEBUG=True, bounds=6)
    
def test_2():
    pc = phc(eqn = "x^2 + y^2 - 1", num_points = 10)
    print pc
    print type(pc)
    print pc.points
    print type(pc.points)


def test_3():
    pc = phc(eqn= "x^2 + y^2 + z^2 - 1", num_points = 1000)
    ng = pc.neighborhood_graph(0.1, "subdivision")
    print ng
    cp = ng.connected_components_1()
    print cp


def main():
    test_1()
    test_2()
    test_3()



if __name__== "__main__": main()

