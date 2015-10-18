#TODO:
#a number n and a polynomial in 2 vars
#create n random lines, solve intersections with polynomial
#spit out a list of points

import phcpy as phcpy

LOUD = False 



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
def phc_2d_cloud(eqn = "x^2 + y^2 - 1", intersectWith = "line", nTimes = 10):

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
        intersects = random_lines(nTimes)

    cloudPoints = []
    for intersect in intersects:
        p = [phcEqn, intersect]
        (q, qsols) = total_degree_start_system(p)

        sol = track(p, q, qsols) 
        if LOUD:
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




def phc_3d_cloud(eqn = "x^2 + y^2 - 1", intersectWith = "plane", nTimes = 10, LOUD=False):

    # returns a set of points given the raw string from phc
    def phc_3d_out(phcOut):
        from phcpy.solutions import strsol2dict # points
        points = []
        for i in phcOut:
            d = strsol2dict(i)
            coords = (d['x'], d['y'], d['z'])

            tres = 1.0
            if abs(d['x'].imag) > tres or abs(d['y'].imag) > tres or abs(d['z'].imag) > tres:
                print "too complex"
                print i

            else:
                points.append(coords)
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
    def random_planes(n):
        lines = []
        for item in range(0,n):
            a,b,c = uniform(-1,1,size=3)
            line = str(a)+"*x + "+str(b)+"*y +" +str(c)+ "*z;"
            lines.append(line)
        return lines


    if intersectWith == "plane":
        intersects = random_planes(nTimes)

    cloudPoints = []
    from phcpy.sets import embed
    for intersect in intersects:
        p = [phcEqn, intersect]
        p = embed(3,1,p)
        (q, qsols) = total_degree_start_system(p)
        sol = track(p, q, qsols) 

        if False:
            for x in sol:
                print x

        for coord in phc_3d_out(sol):
            cloudPoints.append(
                HashPoint(
                    np.array(
                        coord, 
                        dtype=complex
                    )
                )
            )
    
    
    return point_cloud.PointCloud(cloudPoints) 







