from persispy import point_cloud
from persispy.samples import points

def test_plots():
    point_cloud.PointCloud.plot3d(points.sphere(1000))
    point_cloud.PointCloud.plot3d(points.flat_torus(1000))
    point_cloud.PointCloud.plot3d(points.cube(4,1000))
    point_cloud.PointCloud.plot3d(points.torus(1000))

def test_weighted_graph():
    pc = points.torus(1000)
    ng = pc.neighborhood_graph(.1, method = "subdivision")
    print ng

    print len(ng.connected_components()), "hello world"
    print "hello world"

def main():
#     test_plots()
    test_weighted_graph()

if __name__=="__main__": main()
