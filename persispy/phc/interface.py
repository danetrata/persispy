#TODO:
# Create a generalized solver
# Uses the black box solver

DEBUG = False 

" must reject equations with with variable t, e, E, i, I"
def phc_cloud(eqn, nPoints=1, DEBUG=False):
    from phcpy.solver import solve
    from phcpy.solutions import strsol2dict # points
    import numpy as 
    from numpy.random import uniform
    from persispy.point_cloud import PointCloud
    from persispy.hash_point import HashPoint
    

# Parsing target variety into a string usable by phcpy and to generate
# intersects
    phcEqn = eqn+";"
    if DEBUG:
        print "====="
        print "input eqn: ",phcEqn
        print "====="
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
    def is_close(a, b, epsilon = 0.1):
        if DEBUG:
            print a,", ",b,",", abs(a-b)
            print abs(a - b) <= epsilon
        return abs(a - b) <= epsilon

    n = 0
    points = []
    def intersect():
        rand_list = uniform(-1,1, size=len(varList))
        i = 0
        intersect = [] 
        for x in rand_list:
            intersect.append(str(x)+" * "+varList[i])
            if i < len(rand_list)-1: 
                intersect.append(" + ")
            i = i + 1
        intersect.append(";")
        intersect = "".join(intersect)
        return intersect
    if DEBUG:
        attempt = 0
    while(n < nPoints):

# Forming intersects from extracted terms 

# phcpy solver
        p = [phcEqn]
        for x in range(len(varList)-1):
            p.append(intersect())
        if DEBUG:
            print "system of equations"
            print "--"
            for x in p: print x
            print "--"
        phcSol = solve(p)
        if DEBUG:
            print "number of solutions: ", len(phcSol)
            attempt = attempt + 1
            print "attempt #"+str(attempt)

# Parsing the output of phcSol
        for i in phcSol:
            if DEBUG:
                print "phc solution: \n", i 
            d = strsol2dict(i)
            point = [d[x] for x in varList]
            closeness = True 
            for x in point: # choses the points we want
                if is_close(x.imag, 0.0):
                    if x == point[-1] and closeness == True and n < nPoints: 
                        # sometimes phcpy gives more points than we ask,
                        # thus the  additional check
                        points.append([x.real for x in point])
                        n = n + 1
                else:
                    closeness = False


    
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

