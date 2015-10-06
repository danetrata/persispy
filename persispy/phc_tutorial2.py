#TODO:
#a number n and a polynomial in 2 vars
#create n random lines, solve intersections with polynomial
#spit out a list of points

import phcpy


# returns a set of points given the raw string from phc
def phc_sol_parser(phcOut):
    from phcpy.solutions import coordinates # points
    print "phc raw output: ",phcOut
    points = []
    for i in phcOut:
        ([xlabel,ylabel],[x,y]) = coordinates(i)
        points.append((x,y))

    
    print "points",points
    return points

# returns nothing
def phc_print(phcOut):
    for sol in phcOut: print sol
    print "\n\n"

def plot2d_circle(points = 10):
    from phcpy.solver import total_degree
    from phcpy.solver import total_degree_start_system
    from phcpy.trackers import track
    from phcpy.solver import solve

    from scipy.constants import pi 
    import numpy as np
    from numpy.random import uniform

    import persispy
    import point_cloud
    import hash_point
    from point_cloud import PointCloud
    from hash_point import HashPoint

    linearIntersects = [] 
# creating a list of random lines to intersect
    for item in range(0,points):
        a,b = uniform(-1,1,size=2)
        line = str(a)+"*x + "+str(b)+"*y;"
        linearIntersects.append(line)

    persispyPoints = []
    for line in linearIntersects:
        p = ["x^2 + y^2 - 1;",line]
        (q, qsols) = total_degree_start_system(p)
        sol = track(p, q, qsols) 
        for coord in phc_sol_parser(sol):
            print "solSet",coord
            persispyPoints.append(coord)
           


    npPoints=np.array(persispyPoints, dtype=complex)
    print npPoints 
    print "length",len(npPoints)
    print "length of element",len(npPoints[0])
    cloudPoints = []
    for point in persispyPoints:
        print "persipyPoint",point

        cloudPoints.append(HashPoint(npPoints))

#PointCloud.plot2d(point_cloud.PointCloud(cloudPoints))





