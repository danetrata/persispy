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


from random import choice
import os
from datetime import datetime
from csv import writer

def make_csv(testName, columnNames):
    today = datetime.today()
    dirpath = "data/"
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)
    i = 1
    while True:
        filepath = dirpath+testName+"-"+str(today.month)+"-"+str(today.day)+'-'+str(i)+'.csv'
        if not os.path.isfile(filepath): # if the file doesn't exist
            fileObject = open(filepath, 'w')
            csv = writer(fileObject)
            csv.writerow(columnNames)
            return csv
        else:
            i += 1

import sys, time


def up():
    # My terminal breaks if we don't flush after the escape-code
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def down():
    # I could use '\x1b[1B' here, but newline is faster and easier
    sys.stdout.write('\n')
    sys.stdout.flush()


def radius(num_points):
#    return (np.log(num_points))**(1.0/4.0)/(num_points**(1.0/2.0))
    return (np.log(np.log(num_points)))**(1.0/2.0)/(num_points**(1.0/2.0))


from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from numpy.random import uniform, random_integers
from persispy.gui.loading_bar import ProgressBar, Percentage, Bar, ETA, RotatingMarker, ET

defaultWidget = ['Iter:0',
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

pointWidget =     ['Point:', 
        Percentage(), 
        ' ',
        Bar(marker = RotatingMarker(),
                left='[(',
                right=')]'),
        ' ', 
        ET(),
        ' ',
        ETA(), 
        ' '
]

def updatePointBar(bar, numPoints):
    bar.widgets[0] = "Points %i:" % numPoints
    bar.update(numPoints)

distanceWidget =     ['Distance:', 
        Percentage(), 
        ' ',
        Bar(marker = RotatingMarker(),
                left='[(',
                right=')]'),
        ' ', 
        ET(),
        ' ',
        ETA(), 
        ' '
]

def updateDistanceBar(bar, distance):
    bar.widgets[0] = "Distance %.2f:" % distance
    bar.update(distance)


def double_stratified(
        (minPoints, maxPoints, incPoints),
        (minDistance, maxDistance, incDistance)):
    """
    We then step through through a range of points, and then for these points,
    step through a range of distances, and count the number of connected
    components
    """
    eqn = False
    testName = "plane"
    csv = make_csv(testName+"_double_stratified", ["Number of points", "Distance", "Connected components"])


    pointBar = ProgressBar(widgets = pointWidget, maxval = maxPoints)
    pointBar.start()


    for numPoints in range(minPoints, maxPoints, incPoints):

        down() # To prepare for subBar
        distanceBar = ProgressBar(widgets = distanceWidget, maxval = maxDistance)
        distanceBar.start()

        distance = minDistance
        while(distance < maxDistance):
            if DEBUG: print "running test", distance

            try:
                points_epsilon_tests(numPoints, distance, csv, eqn)
                
            except StandardError as inst:
                pass

            updateDistanceBar(distanceBar, distance)
            distance += incDistance


        distanceBar.finish()
        up() # to cancel the '\n' of subBar
        up() # to be at position of pBar
        updatePointBar(pointBar, numPoints)

    pointBar.finish()
    down()

    print "all tests have run"

def stratified((minPoints, maxPoints, incPoints),
        repeat = 1):
    """
    We let distance be a function of the number of points. We then step
    through a range of points count the number of connected
    components
    """
    eqn = False
    testName = "plane"

    csv = make_csv(testName, ["Number of points", "Distance", "Connected components"])

    iteration = 0
    iterations = repeat

    pBar = ProgressBar(widgets = defaultWidget, maxval = iterations)
    pBar.start()

    skip = 0
    while(iteration < iterations):
        down() # To prepare for subBar
        subBar = ProgressBar(widgets = distanceWidget, maxval = maxPoints)
        subBar.start()
        for numPoints in range(minPoints, maxPoints, incPoints):


            distance = radius(numPoints)
            if DEBUG: print "running test", distance

            try:
                points_epsilon_tests(numPoints, distance, csv, eqn)
                
            except StandardError as inst:
                skip += 1
                defaultWidget[2] = "Skip:"+str(skip)
                if DEBUG: print inst
                if DEBUG: print "skip"
                pass
            subBar.widgets[0] = "Points %i:" % numPoints
            subBar.update(numPoints)

        subBar.finish()
        up() # to cancel the '\n' of subBar
        up() # to be at position of pBar
        defaultWidget[0] = "Iter:"+str(iteration)
        pBar.update(iteration)
        if DEBUG: print iteration
        iteration += 1

    pBar.finish()
    down()

    print "all tests have run"

import numpy.random as npr

def monte_carlo(testName, eqn = False):
    """
    We run a Monte Carlo test, choosing number of points and a distance at 
    random uniformly and count the number of connected components.
    """

    csv = make_csv(testName, ["Number of points", "Distance", "Connected components"])

    minDistance = 0.01
    maxDistance = 1

    minPoints = 1
    maxPoints = 1500

    iteration = 0
    iterations = 10000
    pBar = ProgressBar(widgets = defaultWidget, maxval = iterations)
    pBar.start()


    skip = 0
    while(iteration < iterations):

        distance = npr.uniform(minDistance, maxDistance)

        if DEBUG: print "running test", distance

        try:
            num_points = npr.random_integers(minPoints, maxPoints)
            points_epsilon_tests(num_points, distance, csv, eqn)
            widgetsOverall[0] = "Iter:"+str(iteration)
        except StandardError as inst:
            skip += 1
            widgetsOverall[2] = "Skip:"+str(skip)
            if DEBUG: print inst
            if DEBUG: print "skip"
            pass

        pBar.update(iteration)
        if DEBUG: print iteration
        iteration += 1

    pBar.finish()
    down()

    print "all tests have run"
    csv.close()

import numpy as np
# from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex
from persispy.points import plane

def points_epsilon_tests(num_points, distance, csv, eqn = False):

    row = []
    failures = []

    try:
        if eqn:
            pc = phc(eqn, num_points = num_points, return_complex = True)
        else:
            pc = plane(num_points)
        row.append(str(num_points))
        row.append(str(distance))
        ng = pc.neighborhood_graph(distance, method = "subdivision")
        cp = len(ng.connected_components())
        if DEBUG: print "connected components", cp
        row.append(str(cp))
    except StandardError as inst:
        if DEBUG: print inst
        failures.append(inst.args[0])
        return failures
    

    if DEBUG: print ','.join(row)
    csv.writerow(row)
    return cp

def repeat():
    """
    repeats the test
    """
    prompt = input("How many times to run the test?")
    for _ in range(prompt):
        stratified(
                (10, 1500, 10)) 

def main():
    repeat()


if __name__ == "__main__": main()
    
