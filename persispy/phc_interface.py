#TODO:
#a number n and a polynomial in 2 vars
#create n random lines, solve intersections with polynomial
#spit out a list of points

import phcpy as phcpy


# returns a set of points given the raw string from phc
def phc_sol_parser(phcOut):
    from phcpy.solutions import coordinates # points
    points = []
    for i in phcOut:
        ([xlabel,ylabel],[x,y]) = coordinates(i)
        points.append((x,y))

    
    return points

# returns nothing
def phc_print(phcOut):
    for sol in phcOut: print sol
    print "\n\n"

"""
2d_cloud(equation, points)
    returns PointCloud
=====
Given a string equation and a number of lines for intersecting the 
equation, returns a PointCloud.
"""
def dd_cloud(eqn = "x^2 + y^2 - 1", intersectWith = "line", nTimes = 10):
    from phcpy.solver import total_degree
    from phcpy.solver import total_degree_start_system
    from phcpy.trackers import track
    from phcpy.solver import solve

    import numpy as np
    from numpy.random import uniform

    import persispy as persispy
    import point_cloud as point_cloud
    import hash_point as hash_point
    from point_cloud import PointCloud
    from hash_point import HashPoint

    phcEqn = eqn+";"

    intersects = [] 
    
    # creating a list of random lines to intersect
    def random_lines(n):
        lines = []
        for item in range(0,n):
            a,b = uniform(-1,1,size=2)
            line = str(a)+"*x + "+str(b)+"*y;"
            lines.append(line)
        return lines

    def random_circles(n):
        circles = []
        for item in range(0,n):
            a,b,h,k = uniform(-1,1,size=4)
            circle = str(a)+"*(x+"+str(h)+")^2 + "+str(b)+"*(y+"+str(k)+")^2;"
            circles.append(circle)
        return circles


    if intersectWith == "line":
        intersects = random_lines(nTimes)
    if intersectWith == "circle":
        intersects = random_circles(nTimes)

    persispyPoints = []
    for intersect in intersects:
        p = [phcEqn, intersect]
        (q, qsols) = total_degree_start_system(p)
        sol = track(p, q, qsols) 
        for coord in phc_sol_parser(sol):
            persispyPoints.append(coord)
    npPoints=np.array(persispyPoints, dtype=complex)
    
    cloudPoints = []
    for point in npPoints:
        cloudPoints.append(HashPoint(point))
    return point_cloud.PointCloud(cloudPoints) 





