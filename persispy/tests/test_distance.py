# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex
from datetime import datetime
from numpy.random import random_integers
from random import choice

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

def points_setup():

    today = datetime.today()
    filepath = "points-"+str(today.month)+"-"+str(today.day)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    testpath = filepath+'/data.csv'
    if not os.path.isfile(testpath):
        csv = open(testpath, 'w')
        csv.write("Number of points, Distance, Connected components\n")
    else:
        csv = open(testpath, 'a')

    for x in range(200):
        try:
            distance = 0
            connected_components = -1
            while connected_components != 1:
                distance = distance + .01
                for num_points in [150]:
                    connected_components = points_epsilon_tests(num_points, distance, csv)
        except:
            print "skip"
            pass

    print "all tests have run"
    csv.close()

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
        row.append("failed")
        row.append("failed")
        row.append("failed")
        failures.append(inst.args[0])
        return failures

    try:
        ng = pc.neighborhood_graph(distance, method = "subdivision")
        cp = ng.connected_components_1()
        print "connected componenets", cp
        row.append(str(cp))
    except StandardError as inst:
        row.append("failed")
        failures.append(inst.args[0])
        return failures
    
    print ','.join(row)
    row[-1] = row[-1]+"\n"
    csv.write(','.join(row))
    return cp

from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from numpy.random import uniform
import os

def sanity_check():
    pc = phc(pDict["sphere"], num_points = 500)
    ng = pc.neighborhood_graph(0.1)
    cp = ng.connected_components_1()
    print "sanity check"
    print "sphere"
    print "point cloud"
    print pc
    print "neighborhood graph"
    print ng
    print "connected components"
    print cp

    today = datetime.today()
    filepath = str(today.month)+"-"+str(today.day)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    testpath = filepath+'/temp.csv'
    if not os.path.isfile(testpath):
        csv = open(testpath, 'w')
        csv.write("Equation, Dim, Degree, Coefficients, Number of points, Epsilon, Connected components\n")
    else:
        csv = open(testpath, 'a')
    print phc_epsilon_tests(pDict["sphere"], 500, 0.1, csv)
    csv.close()


def random_eqn():
    print "random eqn"

    terms = ['u', 'v', 'w', 'x', 'y', 'z']
    terms = terms[0:random_integers(2, 6)]
    operators = [' + ', ' - ']

    eqn = []
    for term in terms:
        coeff = random_integers(-50, 50)
        degree = random_integers(1, 6) 
        eqn.append(str(coeff)+" * "+term+" ** "+str(degree))

        if terms[-1] != term:
            eqn.append(choice(operators))

    eqn.append(choice(operators))
    constant = random_integers(1, 50) 
    eqn.append(str(constant))

    terms = symbols(" ".join(terms))
    expand = random_integers(1, 1) 
    eqn = parse_expr("("+"".join(eqn)+") ** "+str(expand))
    print eqn.expand()





def main():


    sanity_check()

#     phc_setup()
    
    points_setup()


    




if __name__ == "__main__": main()
    
