
# import sys
# sys.setrecursionlimit(1000)

pDict = {
    "circle"           : "x^2 + y^2 - 1",
    "sphere"           : "x^2 + y^2 + z^2 - 1",
    "torus"            : "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "eightsurface"     : "4*z^4 + 1 * (x^2 + y^2 - 4*z^2)",
    "wideeightsurface" : "4*z^4 + 1/2 * (x^2 + y^2 - 4*z^2) - 1/4",
    "hyperbolid"       : "x^2 + y^2 - z^2 - 1",
    "degree3sphere"    : "x^3 + y^3 + z^3 - 1"
}


from persispy.samples import points
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from numpy.random import uniform
import os
from datetime import datetime
from numpy.random import random_integers
from random import choice

def make_csv(testName, columnNames):
    today = datetime.today()
    dirpath = "data/"
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)
    i = 1
    while True:
        filepath = dirpath+testName+"-"+str(today.month)+"-"+str(today.day)+'-'+str(i)+'.csv'
        if not os.path.isfile(filepath): # if the file doesn't exist
            csv = open(filepath, 'w')
            csv.write(columnNames+"\n")
            return csv
        else:
            i += 1

def points_setup(testName, eqn = False):

    import sys, time

    def up():
        # My terminal breaks if we don't flush after the escape-code
        sys.stdout.write('\x1b[1A')
        sys.stdout.flush()

    def down():
        # I could use '\x1b[1B' here, but newline is faster and easier
        sys.stdout.write('\n')
        sys.stdout.flush()

    try: # runs if shapely if installed
        import shapely
        from persispy.tests.area import shapely_area
        csv = make_csv("Number of points, Distance, Connected components, Area")
    except:
        csv = make_csv(testName, "Number of points, Distance, Connected components")

    from persispy.gui.loading_bar import ProgressBar, Percentage, Bar, ETA, RotatingMarker, ET

    widgetsOverall = ['Iter:0',
            ' ',
            'Skip:0', 
            ' ',
            Percentage(), 
            ' ',
            Bar(marker= RotatingMarker(),
                    left='[',
                    right=']'),
            ' ',
            ET(),
            ' ',
            ETA(), 
            ' '
    ]


    import numpy.random as npr
    distance = 0.001
    minDistance = 0.05
    maxDistance = .2
    incDistance = 0.05 # increment
    minPoints = 1
    maxPoints = 1000
    incPoints = 25

    iteration = 0
    iterations = 10000
    pbar = ProgressBar(widgets = widgetsOverall, maxval = iterations)
    pbar.start()

    padding = 15

    skip = 0
    while(iteration < iterations):

        distance = npr.uniform(minDistance, maxDistance)

        if DEBUG: print "running test", distance

        try:
            num_points = npr.random_integers(minPoints, maxPoints)
            points_epsilon_tests(num_points, distance, csv, eqn)
            widgetsOverall[0] = "Iteration:"+str(iteration)
        except StandardError as inst:
            skip += 1
            widgetsOverall[2] = "Skipped:"+str(skip)
            if DEBUG: print inst
            if DEBUG: print "skip"
            pass

        pbar.update(iteration)
        if DEBUG: print iteration
        iteration += 1

    pbar.finish()
    down()

    print "all tests have run"
    csv.close()


from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex

def points_epsilon_tests(num_points, distance, csv, eqn = False):

    row = []
    failures = []

    try:
        if eqn:
            pc = phc(eqn, num_points = num_points, return_complex = True)
        else:
            pc = points.plane(num_points)
        row.append(str(num_points))
        row.append(str(distance))
    except StandardError as inst:
        if DEBUG: print inst
        failures.append(inst.args[0])
        return failures

    try:
        ng = pc.neighborhood_graph(distance, method = "subdivision")
        cp = len(ng.connected_components())
        if DEBUG: print "connected components", cp
        row.append(str(cp))
    except StandardError as inst:
        if DEBUG: print inst
        failures.append(inst.args[0])
        return failures
    
    try: # runs if shapely is installed
        diskArea = shapely_area(pc, distance)
        if DEBUG: print "area:", diskArea
        row.append(str(diskArea))
    except:
        pass

    if DEBUG: print ','.join(row)
    row[-1] = row[-1]+"\n"
    csv.write(','.join(row))
    return cp


DEBUG = False
def main():

#     points_setup("sphere", "x^2 + y^2 + z^2 - 1")
    points_setup("plane")

if __name__ == "__main__": main()
    
