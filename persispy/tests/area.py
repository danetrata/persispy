from persispy.point_cloud import PointCloud
# takes a point cloud and returns an approximate area
def shapely_area(points, radius):
    from shapely.geometry import Point
    from shapely.ops import cascaded_union

    if isinstance(points, PointCloud):
        points = [point._coords.tolist() for point in points._points]
    if type(points[0]) == 'numpy.ndarray':
        points = points.tolist()
    polygons = [Point(coord).buffer(radius) for coord in points]
    union = cascaded_union(polygons)
    return union.area

import numpy.random as npr
import numpy as np
from persispy.samples.points import plane
from persispy.phc.points import phc
def main():

    npplane = [npr.uniform(0, 1, size=2) for _ in range(240)]
    print type(npplane[0])
#     area(npplane)

    pc = phc("x^2 + y^2 - 1", 100)
    print type(pc)

#     area([[0,0]])

    ppyplane = plane(100)
    print ppyplane
#     area(ppyplane)
    
    radius = 0.1
    ng = ppyplane.neighborhood_graph(radius)
    print ng._adj
    print ng._adj.iterkeys().next()
    counter = 0

    totalCircle = 0
    circle = np.pi * radius**2

    totalDiff = 0
    for key, value in ng._adj.iteritems():
        print key
        print value
        print len(value)
        totalCircle += circle

        for point, distanceFromKey in value:
            print point
            print distanceFromKey
            totalDiff -= radius**2 * np.arccos(distanceFromKey/radius) - \
                    distanceFromKey *np.sqrt(4*radius**2 - distanceFromKey**2) 
        print type(value)
        counter += 1
        print counter

    print totalCircle
    print totalDiff
    print totalCircle - totalDiff
    print ng.connected_components_1()
    print ng.adjacency_matrix().data[0]
    ppyplane.plot3d()
    ppyplane.plot3d_neighborhood_graph(0.1)




if __name__ == "__main__" : main()
