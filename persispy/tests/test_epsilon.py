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

def try_epsilon_tests(eqn, num_points, epsilon, csv):

    row = []
    failures = []
    try:
        pc = phc(eqn, num_points = num_points, bounds = 20, return_complex = True)
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
        ng = pc.neighborhood_graph(epsilon, method = "subdivision")
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

    return failures


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
        csv.write("Equation, Degree, Coefficients, Number of points, Epsilon, Connected components\n")
    else:
        csv = open(testpath, 'a')
    print try_epsilon_tests(pDict["sphere"], 500, 0.1, csv)
    csv.close()

def main():

    import gc

    sanity_check()
    pass

    today = datetime.today()
    filepath = str(today.month)+"-"+str(today.day)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    testpath = filepath+'/data.csv'
    if not os.path.isfile(testpath):
        csv = open(testpath, 'w')
        csv.write("Equation, Degree, Coefficients, Number of points, Epsilon, Connected components\n")
    else:
        csv = open(testpath, 'a')

    for x in range(100):
        print "random eqn"

        terms = ['u', 'v', 'w', 'x']
        terms = terms[0:random_integers(2, 4)]
        operators = [' + ', ' - ']

        eqn = []
        for term in terms:
#             coeff = uniform(-5, 5)
            coeff = random_integers(-50, 50)
            degree = random_integers(1, 4) 
            eqn.append(str(coeff)+" * "+term+" ** "+str(degree))

            if terms[-1] != term:
                eqn.append(choice(operators))

        eqn.append(choice(operators))
        constant = random_integers(1, 5) 
        eqn.append(str(constant))

        terms = symbols(" ".join(terms))
        expand = random_integers(1, 2) 
        eqn = parse_expr("("+"".join(eqn)+") ** "+str(expand))
        print eqn.expand()

        try:
            for num_points in [250, 500, 750, 1000]:
                for epsilon in [0.3, 0.25, 0.2, 0.15, 0.1]:
                    
#                 before = hp.heap()

                    print try_epsilon_tests(str(eqn.expand()), num_points, epsilon, csv)

#                 after = hp.heap()
#                 print after - before
        
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
    
