# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex
from datetime import datetime
from sympy import symbols
from numpy.random import random_integers
from random import choice

# import sys
# sys.setrecursionlimit(1000)

pDict = {
    "circle"           : "x^2 + y^2 - 1",
    "sphere"           : "x^2 + y^2 + z^2 - 1",
    "torus"            : "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
#     "eightsurface"     : "4*z^4 + 1 * (x^2 + y^2 - 4*z^2)", # gives me grief
    "wideeightsurface" : "4*z^4 + 1/2 * (x^2 + y^2 - 4*z^2) - 1/4",
    "hyperbolid"       : "x^2 + y^2 - z^2 - 1",
    "degree3sphere"    : "x^3 + y^3 + z^3 - 1"
}

def try_epsilon_tests(eqn, num_points, epsilon, csv, filepath):

    row = []
    failures = []
    try:
        pc = phc(eqn, num_points = num_points, bounds = 20)
        dim = pc.dimension()
        row.append(str(pc.eqn))
        row.append(str(pc.degree))
        row.append(str(pc.total_coeff))
        row.append(str(num_points))
        row.append(str(epsilon))
    except StandardError as inst:
        row.append(str(eqn))
        row.append("failed")
        row.append("failed")
        row.append("failed")
        row.append("failed")
        row.append("failed")
        failures.append(inst.args[0])
        return failures

    try:
        cp = pc.neighborhood_graph(epsilon, method = "subdivision").connected_components_1()
        print "connected componenets", cp
        row.append(str(cp))
    except StandardError as inst:
        row.append("failed")
        failures.append(inst.args[0])
        return failures
    
    print ','.join(row)
    row[-1] = row[-1]+"\n"
    csv.write(','.join(row))

    try:
        if dim == 2 \
                or dim == 3:
            pc.plot2d(save = filepath+"/plot2d/plot2d", title = pc.eqn)
    except StandardError as inst:
        failures.append(inst.args[0])

    try:
        if pc.plot2d_neighborhood_graph(epsilon, save = filepath+"/plot2d_ng/plot2d_ng", title = pc.eqn) != True:
            raise RuntimeError("failed to plot2d "+str(x))
    except StandardError as inst:
        failures.append(inst.args[0])

    try:
        if dim == 3:
            pc.plot3d(save = filepath+"/plot3d/plot3d", title = pc.eqn)
    except StandardError as inst:
        failures.append(inst.args[0])
        
    try:
        if pc.plot3d_neighborhood_graph(epsilon, save = filepath+"/plot3d_ng/plot3d_ng", title = pc.eqn) != True:
            raise RuntimeError("failed to plot3d "+str(x))
    except StandardError as inst:
        failures.append(inst.args[0])


    return failures

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

def main():

    import gc

    sanity_check()

    today = datetime.today()
    filepath = str(today.month)+"-"+str(today.day)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    testpath = filepath+'/plots.csv'
    if not os.path.isfile(testpath):
        csv = open(testpath, 'w')
        csv.write("Equation, Degree, Coefficients, Number of points, Epsilon, Connected components\n")
    else:
        csv = open(testpath, 'a')

    eqn = raw_input("enter an eqn to plot:\n")
    for x in range(1):
        try:
            for num_points in [750, 1000]:
                for epsilon in [0.3, 0.25, 0.2, 0.15, 0.1]:
                    print try_epsilon_tests(eqn, num_points, epsilon, csv, filepath)

        except:
            pass

        gc.collect()


    print "all tests have run"
    
    csv.close()

    


    """ 
    pseudocode:
    let epsilon < 0:
        then plot epsilon
    plot(cp(coeff[small, large]), cp(num_points), cp(degree))
    pc = phc(eqn)
        test_coefficients(pc) = x
            return cp
        test_number_of_points(pc) = y
            return cp
        test_degree(pc) = z
            return cp
    """


if __name__ == "__main__": main()
    
