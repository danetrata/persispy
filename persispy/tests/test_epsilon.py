# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex
from datetime import datetime
import sys
sys.setrecursionlimit(1000)

pDict = {
    "circle"           : "x^2 + y^2 - 1",
    "sphere"           : "x^2 + y^2 + z^2 - 1",
    "torus"            : "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "eightsurface"     : "4*z^4 + 1 * (x^2 + y^2 - 4*z^2)",
    "wideeightsurface" : "4*z^4 + 1/2 * (x^2 + y^2 - 4*z^2) - 1/4",
    "hyperbolid"       : "x^2 + y^2 - z^2 - 1",
    "degree3sphere"    : "x^3 + y^3 + z^3 - 1"
}

def try_persispy(eqn, num_points, csv):

    totalFailures = []
    for epsilon in [0.3, 0.25, 0.2, 0.15, 0.1]:
        failures = [eqn+" e: "+str(epsilon)]
        row = []
        try:
            pc = phc(eqn, num_points = num_points, bounds = 3)
            row.append(pc.eqn)
            row.append(pc.degree)
            row.append("coeffs")
            row.append(num_points)
            row.append(epsilon)
        except StandardError as inst:
            row.append(eqn)
            row.append("failed")
            row.append("failed")
            row.append("failed")
            row.append("failed")
            failures.append(inst.args[0])

        try:
            cp = pc.neighborhood_graph(epsilon, method = "subdivision").connected_components_1()
            print "connected componenets",cp
            row.append(cp)
        except StandardError as inst:
            row.append("failed")
            failures.append(inst.args[0])

# plotting based on dimension
        dim = pc.dimension()

        try:
            if dim == 2 \
                    or dim == 3:
                pc.plot2d(save = save, title = pc.eqn)
        except StandardError as inst:
            failures.append(inst.args[0])

        try:
            if pc.plot2d_neighborhood_graph(epsilon, save = save, title = pc.eqn) != True:
                raise RuntimeError("failed to plot2d "+str(x))
        except StandardError as inst:
            failures.append(inst.args[0])

        try:
            if dim == 3:
                pc.plot3d(save = save, title = pc.eqn)
        except StandardError as inst:
            failures.append(inst.args[0])
            
        try:
            if pc.plot3d_neighborhood_graph(epsilon, save = save, title = pc.eqn) != True:
                raise RuntimeError("failed to plot3d "+str(x))
        except StandardError as inst:
            failures.append(inst.args[0])


    return totalFailures


def main():
    today = datetime.today()
    save = str(today.month)+"-"+str(today.day)
    print save
    print pDict.keys()
    for x in pDict.keys():


        # catches all errors thrown and continues with next equation
            
        totalFailures.append(failures)
        if len(failures) != 1:
            print "collected the following errors"
            for x in failures:
                print x
        print "running next test"


    print "total failures"
    for x in totalFailures:
        print x
    print "all tests have run"

    


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
    
