#TODO:
#a number n and a polynomial in 2 vars
#create n random lines, solve intersections with polynomial
#spit out a list of points

import phcpy as phcpy

DEBUG = False 



# returns nothing
def phc_print(phcOut):
    for sol in phcOut: print sol
    print "\n\n"

"""
phc_cloud(equation, points)
    returns PointCloud
=====
Given a string equation and a number of lines for intersecting the 
equation, returns a PointCloud.
"""
def phc_2d_cloud(eqn = "x^2 + y^2 - 1", intersectWith = "line", nPoints = 10):

    # returns a set of points given the raw string from phc
    def phc_2d_out(phcOut):
        from phcpy.solutions import coordinates # points
        points = []
        for i in phcOut:
            ([xlabel,ylabel],[x,y]) = coordinates(i)
            points.append((x,y))
        return points

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

    if intersectWith == "line":
        intersects = random_lines(nPoints)

    cloudPoints = []
    for intersect in intersects:
        p = [phcEqn, intersect]
        (q, qsols) = total_degree_start_system(p)

        sol = track(p, q, qsols) 
        if DEBUG:
            for x in sol:
                print x
        for coord in phc_2d_out(sol):
            cloudPoints.append(
                HashPoint(
                    np.array(
                        coord, 
                        dtype=complex
                    )
                )
            )
    
    
    return point_cloud.PointCloud(cloudPoints) 




def phc_3d_cloud(eqn = "x^2 + y^2 - 1", intersectWith = "plane", nPoints = 10, DEBUG=False, treshold = 1.0):
    from phcpy.solver import total_degree
    from phcpy.solver import total_degree_start_system
    from phcpy.trackers import track
    from phcpy.solver import solve
    from numpy.random import uniform
    from phcpy.solutions import strsol2dict # points
    from phcpy.sets import embed
    
    def is_float_eq(a, b, epsilon = 0.1):
        if DEBUG:
            print a,", ",b,",", abs(a-b)
            print abs(a - b) <= epsilon
        return abs(a - b) <= epsilon

    n = 0
    phcEqn = eqn+";"
    points = []
    while (n <= nPoints):
        if intersectWith == "plane":
            a,b,c = uniform(-1,1,size=3)
            q = str(a)+"*x + "+str(b)+"*y +" +str(c)+ "*z;"

            p = [phcEqn, q]
            p = embed(3,1,[phcEqn, q])
            (q, qsols) = total_degree_start_system(p)
            if DEBUG:
                print "system of equations"
                for x in p: print x
                print "total degree start system"
                for x in q: print x
            phcSol = track(p, q, qsols) 

            for i in phcSol:
                d = strsol2dict(i)
                x, y, z = (d['x'], d['y'], d['z'])
                if not is_float_eq(x.imag, 0.0) or not is_float_eq(y.imag, 0.0) or not is_float_eq(z.imag, 0.0):
                    if DEBUG:
                        print "too far"
                        print i
                        print (x,y,z)

                else:
                    points.append((x,y,z))
                    n += 1
                    if DEBUG:
                        print n

    import numpy as np
    import persispy as persispy
    import point_cloud as point_cloud
    import hash_point as hash_point
    from point_cloud import PointCloud
    from hash_point import HashPoint

    cloudPoints = []
    for coord in points:
        cloudPoints.append(
            HashPoint(
                np.array(
                    coord, 
                    dtype=complex
                )
            )
        )
    
    return point_cloud.PointCloud(cloudPoints) 







