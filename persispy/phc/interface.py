<<<<<<< HEAD
"""
Takes a variety of type string and, after solving intersections with phcpy,
returns a persispy point cloud. We must reject equations with with variables t, 
e, E, i, I because their meanings are reserved.
"""
def phc_cloud(eqn, num_points=1, allow_complex=False, DEBUG=False):
    import numpy as np
    from phcpy.solver import solve
    from phcpy.solutions import strsol2dict # points
=======
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
>>>>>>> f90353a504d2dec06a7dbef858141273a2391ec8
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
    for x in ["+","-","*","^"]: terms = terms.replace(x," ")
    terms = terms.strip(" ")
    varList = []
    for x in terms:
        if x in ["e", "E", "i", "I", "t"]:
            raise RuntimeError("\""+x+"\" is reserved. Please use a " \
                "different variable.")
        if not x.isdigit() and x.isalnum() and x not in varList:
            varList.append(x)
    varList.sort()
    if DEBUG: print "list of variables: ", varList

    # To be used to detect solutions with complex parts close to given epsilon
    # Adjust epsilon to your liking.
    # Note: phcpack almost always gives an imaginary parts, as small as 10^-48,
    # so epsilon != 0
    def is_close(a, b = 0, epsilon = 0.1):
        if DEBUG and abs(a - b) <= epsilon: print "Selected point is close" 
        return abs(a - b) <= epsilon

    # "intersect()" forms intersects from extracted the terms. Returns a plane 
    # with random coefficients to intersect the variety. The intersects must be
    # of the same dim as the variety to prevent a overdetermined or 
    # underdetermined systems.
    def intersect():
        rand_list = np.random.uniform(-1,1, size=len(varList))
        i = 0
        intersect = [] 
        for x in rand_list:
            intersect.append(str(x)+" * "+varList[i])
            if i < len(rand_list)-1: intersect.append(" + ")
            i = i + 1
        intersect.append(";")
        intersect = "".join(intersect)
        return intersect

    n = 0
    points = []
    if DEBUG: attempt = 0

    # phcpy solver
    while(n < num_points):
        p = [phcEqn]

        # The for loop ensures the system is "square", where number of 
        # variables = number of equations. The resulting points are regular, 
        # bounded by the variety.
        for x in range(len(varList)-1): p.append(intersect())
        if DEBUG:
            print "system of equations"
            print "--"
            for x in p: print x
            print "--"
            phcSol = solve(p)
            print "number of solutions: ", len(phcSol)
            attempt = attempt + 1
            print "attempt #"+str(attempt)
        else:
            phcSol = solve(p,silent=True)

        # Parsing the output of phcSol
        for i in phcSol:
            if DEBUG: print "phc solution: \n", i 
            d = strsol2dict(i)
            point = [d[x] for x in varList]
            if allow_complex:
                points.append(point)
                n = n + 1
            else:
                closeness = True 
                for x in point: 
                # choses the points we want
                    if is_close(x.imag):
                        # sometimes phcpy gives more points than we ask,
                        # thus the additional check
                        if x == point[-1] and closeness == True and \
                            n < num_points: 
                            points.append([x.real for x in point])
                            n = n + 1
                    else:
                        closeness = False

    if DEBUG: print "points: ",points

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

