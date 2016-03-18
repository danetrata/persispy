# What is interface? I'm not sure if this is the correct path.
from .interface import phc_cloud
from ...point_cloud import PointCloud

def test_1():
#     phc_cloud(eqn = "x^2 - y", DEBUG=True)
    phc_cloud(eqn = "x^2 + y^2 - 1", DEBUG=True)
#     phc_cloud(eqn = "x^2 + y^3 - 1", DEBUG=True)
#     phc_cloud(eqn = "x^2 + y^2 + z^2 - 1", DEBUG=True)
#     phc_cloud(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
#     phc_cloud(eqn = "x^2 + y^2 + z^2 + a - 1", DEBUG=True)
#     phc_cloud(eqn = "x^2 + y^3 - 1", DEBUG=True, bounds=6)
    
def test_2():
    phc_cloud(eqn = "x^2 + y^2 - 1", point_cloud=False)

def test_3():
    pc = phc_cloud(eqn= "x^2 + y^2 + z^2 - 1", num_points = 1000)
#     PointCloud.plot3d(pc)
    ng = pc.neighborhood_graph(0.1, "subdivision")
    print ng

def main():
    test_1()
    test_2()
    test_3()



if __name__== "__main__": main()

