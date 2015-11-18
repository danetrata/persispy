"""
Takes a variety of type string and, after solving intersections with phcpy,
returns a persispy point cloud. We must reject equations with with variables t, 
e, E, i, I because their meanings are reserved.
"""

import numpy as np
from phcpy.solver import total_degree_start_system
from phcpy.trackers import track
from phcpy.solutions import strsol2dict # points
from persispy.point_cloud import PointCloud
from persispy.hash_point import HashPoint

class Singleton(type):
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__instance = None
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance

class phc(object):

    points = []

    def __init__(self, eqn, bounds = 1, num_points = 1, return_complex = False, DEBUG = False):
        self.eqn = eqn
        self.bounds = bounds 
        self.num_points = num_points
        self.return_complex = return_complex
        self.DEBUG = DEBUG
        self.__call__()

# for printing the points
    def __repr__(self):
        return self.points.__repr__()

    def __call__(self):
        eqn = self.eqn
        bounds = self.bounds 
        num_points = self.num_points
        return_complex = self.return_complex
        DEBUG = self.DEBUG
        # for dealing with the fact that PHC always returns complex solutions
        complex_epsilon = 0.1
# For other possible implementations of intersecting the varieties
        relative_epsilon = 0.1

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
        def is_close(a, b = 0, epsilon = complex_epsilon):
            if DEBUG and abs(a - b) <= epsilon: print "Selected component is close" 
            return abs(a - b) <= epsilon

        # "intersect()" forms intersects from extracted the terms. Returns a plane 
        # with random coefficients to intersect the variety. The intersects must be
        # of the same dim as the variety to prevent a overdetermined or 
        # underdetermined systems.
        def intersect():
            rand_list = np.random.uniform(-bounds, bounds, size=len(varList))
            i = 0
            intersect = [] 
            for x in rand_list:
                intersect.append(str(x)+" * "+varList[i])
                if i < len(rand_list)-1: intersect.append(" + ")
                i = i + 1
            intersect.append(";")
            intersect = "".join(intersect)
            return intersect

        def in_bounds(a):
            if bounds <= 0 or abs(bounds-abs(a)) <= bounds:
                if DEBUG: print "Selected component is in bounds"

                return True
            else:
                return False

        n = 0
        # It is possible to use a dictionary instead of a list
        # but is possibly unnecessary to store the intersect
        points = []
        if DEBUG: attempt = 0

        p = [phcEqn]

        #  This first block sets up the start system so the solver
        #  doesn't need to make a new one for each intersection
        #  The for loop ensures the system is "square", where number of
        #  variables = number of equations. The resulting points are regular,
        #  bounded by the variety.
        for x in range(len(varList)-1): p.append(intersect())
        if DEBUG:
            print "system of equations"
            print "--"
            for x in p: print x
            print "--"
            startSystem, startSol = total_degree_start_system(p)
            print "start solutions: ", len(startSol)
            for x in startSystem: print x
            for x in startSol: print x
            attempt = attempt + 1
            print "attempt #"+str(attempt)
        else:
            startSystem, startSol = total_degree_start_system(p)

        # phcpy solver
        while(n < num_points):
            p = [phcEqn]


            #  Uses the already made start system. Otherwise, identical to 
            #  the block
            #  above
            #  The for loop ensures the system is "square", where number of
            #  variables = number of equations. The resulting points are regular,
            #  bounded by the variety.
            for x in range(len(varList)-1): p.append(intersect())
            if DEBUG:
                print "system of equations"
                print "--"
                for x in p: print x
                print "--"
                phcSol = track(p, startSystem, startSol)
                print "number of solutions: ", len(phcSol)
                attempt = attempt + 1
                print "attempt #"+str(attempt)
            else:
                startSystem, startSol = total_degree_start_system(p)
                phcSol = track(p, startSystem, startSol)

            #  Parsing the output of phcSol
            for i in phcSol:
                if DEBUG: print "phc solution: \n", i 
                d = strsol2dict(i)
                point = [d[x] for x in varList]
                if return_complex:
                    points.append(point)
                    n = n + 1
                else:
                    closeness = True 
                    for x in point: 
                    # choses the points we want
                        if is_close(x.imag) and in_bounds(x.real):
                            # sometimes phcpy gives more points than we ask,
                            # thus the additional check
                            if x == point[-1] and closeness == True and \
                                n < num_points: 
                                points.append([x.real for x in point])
                                n = n + 1
                                if DEBUG: print "appended point:",[x.real for x in point]
                        else:
                            closeness = False

        if DEBUG: print "points: ",points

        self.points = points

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

        pointCloud = PointCloud(cloudPoints) 
        return pointCloud

def main():
    pc = phc(eqn = "x^2 + y^2 - 1", num_points = 10, DEBUG = True)
    print pc


if __name__ == "__main__": main()
