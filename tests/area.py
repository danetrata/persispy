from persispy.point_cloud import PointCloud
# takes a point cloud and returns an approximate area
def shapely_area(points, radius):
    from shapely.geometry import Point
    from shapely.ops import cascaded_union

    if isinstance(points, PointCloud):
        points = [point._coords.tolist() for point in points._points]
    if type(points[0]) == 'numpy.ndarray':
        points = points.tolist()
    polygons = [Point((float(coord[0]), float(coord[1]))).buffer(radius) for coord in points]
    union = cascaded_union(polygons)

    return union.area



import numpy.random as npr
import numpy as np



from persispy.samples.points import plane
from persispy.phc.points import phc
def main():

#     npplane = [npr.uniform(0, 1, size=2) for _ in range(240)]
#     print type(npplane[0])
# 
#     pc = phc("x^2 + y^2 - 1", 100)
#     print type(pc)
# 
# 
#     ppyplane = plane(190)
#     print ppyplane

    points = []

    with open("disks", "r") as openFile:
        for line in openFile:
            points.append( line.split()[0:2])


    print points

    area = shapely_area(points, 0.1)

    print "converting curves to splines"

    print "estimated area:", area
    

    




if __name__ == "__main__" : main()

#     radius = 0.1
# 
#     area(ppyplane, radius)
#
#     ppyplane.plot3d()
#     ppyplane.plot3d_neighborhood_graph(0.1)
# def segment_from_distance(distance, radius):
#     x = distance/2.0
#     angle = 2.0 * myacos(x/radius)
#     result = 1.0/2.0 * (angle - np.sin(angle)) * radius**2.0
#     print "intersection", result
#     return result
# 
# def myasin(x):
#     tempExp = x
#     factor = 1.0
#     divisor = 1.0
#     summ = x
#     for i in range(0, 100):
#         tempExp *= x*x
#         divisor += 2.0
#         factor *= ((2.0*i) + 1.0) / ((i + 1.0) *2)
#         summ += factor*tempExp/divisor
# 
#     return summ
# 
# def myacos(x):
#     return np.pi/2.0 - myasin(x)
# 
# 
# 
# def area(pointCloud, radius):
#     ng = pointCloud.neighborhood_graph(radius)
#     radius = ng.epsilon
#     counter = 0.0
#     circle = np.pi * radius**2
#     totalCircle = 0.0
#     totalDiff = 0.0
# 
#     for key, value in ng._adj.iteritems():
#         print key
# 
#         totalCircle += circle
# 
#         for point, distanceFromKey in value:
#             print point
#             print distanceFromKey
#             totalDiff += segment_from_distance(distanceFromKey, radius)
#         print type(value)
#         counter += 1
#         print counter
# 
#     print totalCircle
#     print totalDiff
#     print totalCircle - totalDiff
#     print ng.connected_components_1()
#     print ng.adjacency_matrix().data[0]
