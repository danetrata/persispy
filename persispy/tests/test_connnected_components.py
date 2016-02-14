
DEBUG = False

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

def make_csv(columnNames):
    today = datetime.today()
    filepath = "points-"+str(today.month)+"-"+str(today.day)
    i = 1
    while True:
        testpath = filepath+'-data'+'('+str(i)+').csv'
        if not os.path.isfile(testpath): # if the file doesn't exist
            csv = open(testpath, 'w')
            csv.write(columnNames+"\n")
            return csv
        else:
            i += 1

def points_setup():

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
        from persispy.tests.area import shapely_area
        csv = make_csv("Number of points, Distance, Connected components, Area")
    except:
        csv = make_csv("Number of points, Distance, Connected components")

    from persispy.gui.loading_bar import ProgressBar, Percentage, Bar, ETA, RotatingMarker

    widgetsOverall = ['Distance:', 
            Percentage(), 
            ' ',
            Bar(marker= ">",
                    left='[',
                    right=']'),
            ' ', 
            ETA(), 
            ' '
    ]

    widgetsSub =     ['Point:', 
            Percentage(), 
            ' ',
            Bar(marker = RotatingMarker(),
                    left='[(',
                    right=')]'),
            ' ', 
            ETA(), 
            ' '
    ]

    distance = 0.05
    maxDistance = .3
    incDistance = 0.05 # increment
    minPoints = 500
    maxPoints = 10000
    incPoints = 500

    pbar = ProgressBar(widgets = widgetsOverall, maxval = maxDistance)
    pbar.start()

    padding = 15

    while(distance <= maxDistance):

        pbar.widgets[0] = "Distance %.2f" % distance
        pbar.widgets[0] += ' ' * (padding - len(pbar.widgets[0])) + ':'
        if DEBUG: print "running test", distance

        subBar = ProgressBar(widgets = widgetsSub, maxval = maxPoints)
        subBar.start()

        pbar.update(distance)
        down() # To prepare for subBar

        try:
            for num_points in range(minPoints, maxPoints, incPoints):
                subBar.widgets[0] = "Points %i:" % num_points
                subBar.widgets[0] += ' ' * (padding - len(subBar.widgets[0])) + ':'
                points_epsilon_tests(num_points, distance, csv)
                subBar.update(num_points)
            subBar.finish()
        except StandardError as inst:
            if DEBUG: print inst
            if DEBUG: print "skip"
            pass

        distance += incDistance

        up() # to cancel the '\n' of subBar
        up() # to be at position of pBar

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


def main():

    points_setup()


if __name__ == "__main__": main()
    
