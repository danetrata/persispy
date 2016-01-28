from shapely.geometry import Point
from shapely.ops import cascaded_union
from persispy.point_cloud import PointCloud
# takes a point cloud and returns an approximate area
def area(points, radius):

    if isinstance(points, PointCloud):
        points = [point._coords.tolist() for point in points._points]
    if type(points[0]) == 'numpy.ndarray':
        points = points.tolist()
    polygons = [Point(coord).buffer(radius) for coord in points]
    union = cascaded_union(polygons)
    return union.area

import numpy.random as npr
from persispy.samples.points import plane
from persispy.phc.points import phc
def main():

    npplane = [npr.uniform(0, 1, size=2) for _ in range(240)]
    print type(npplane[0])
    area(npplane)

    pc = phc("x^2 + y^2 - 1", 100)
    print type(pc)

    area([[0,0]])

    ppyplane = plane(100)
    print ppyplane
    area(ppyplane)
    



if __name__ == "__main__" : main()
