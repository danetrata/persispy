#TODO:
# Create a generalized solver
# Uses the black box solver

DEBUG = False 

" must reject equations with with varible t, e, E, i, I"
def phc_cloud(eqn, nPoints=1, DEBUG=False):
    from phcpy.solver import total_degree
    from phcpy.solver import total_degree_start_system
    from phcpy.trackers import track
    from phcpy.solver import solve
    from phcpy.solutions import strsol2dict # points
    from phcpy.sets import embed
    import numpy as np
    from numpy.random import uniform
    from persispy.point_cloud import PointCloud
    from persispy.hash_point import HashPoint
    

# Parsing target variety into a string usable by phcpy and to generate
# intersects
    phcEqn = eqn+";"
    if DEBUG:
        print "input eqn: ",phcEqn
    terms = eqn

# Extracting terms from the target
    for x in ["+","-","*","^"]:
        terms = terms.replace(x," ")
    terms = terms.strip(" ")
    varList = []
    for x in terms:
        if not x.isdigit() and x.isalnum() and x not in varList:
            varList.append(x)
    varList.sort()
    if DEBUG:
        print "list of varibles: ", varList

# To be used to detect solutions with complex parts close to given epsilon
# Adjust epilson to your liking.
# Note: phcpack almost always gives an imaginary parts, as small as 10^-48,
# so epsilon != 0
    def is_float_eq(a, b, epsilon = 0.1):
        if DEBUG:
            print a,", ",b,",", abs(a-b)
            print abs(a - b) <= epsilon
        return abs(a - b) <= epsilon

    n = 0
    points = []
    while(n < nPoints):

# Forming intersects from extracted terms 
        rand_list = uniform(-1,1, size=len(varList)-1)
        i = 0
        intersect = [] 
        for x in rand_list:
            intersect.append(str(x)+" * "+varList[i])
            if i < len(rand_list)-1: # "- 1" because index and we only need "n-1"
                                   # variables
                intersect.append(" + ")
            i = i + 1
        intersect.append(";")
        intersect = "".join(intersect)

#phcpy solver
        p = [phcEqn, intersect]
        phcSol = solve(p)
        if DEBUG:
            print "system of equations"
            for x in p: print x
            print "number of solutions: ", len(phcSol)

# Parsing the output of phcSol
        for i in phcSol:
            if DEBUG:
                print "phc solution: \n", i 
            d = strsol2dict(i)
            if DEBUG:
                print "strsol2dict: ",d
                print "keys: ",d.viewkeys()
                print "values: ", d.viewvalues()
            point = [d[x] for x in varList]
            for x in point:
                if is_float_eq(x.imag, 0.0):
                    if point[-1] == x and n < nPoints: # sometimes phcpy gives
                                                       # more points than we 
                                                       # ask, thus the 
                                                       # additional check
                        points.append(point)
                        n = n + 1
    
    if DEBUG:
        print "points: ",points


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
    
    return PointCloud(cloudPoints) 

