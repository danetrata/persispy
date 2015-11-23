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
    "doubletorus"      : "((x^2 + y^2)^2 - x^2 +y^2)^2 + z - 1/2",
    "eightsurface"     : "4*z^4 + 1 * (x^2 + y^2 - 4*z^2)",
    "wideeightsurface" : "4*z^4 + 1/2 * (x^2 + y^2 - 4*z^2) - 1/4",
    "hyperbolid"       : "x^2 + y^2 - z^2 - 1",
    "cubic"            : "x^3 + x^2 + x - 1"
}



def main():
    today = datetime.today()
    save = str(today.month)+"-"+str(today.day)
    print save
    print pDict.keys()
    for x in pDict.keys():
        try:
            try:
                pc = phc(pDict[x], num_points = 1000)
                print pc
                epsilon = 0.2
            except:
                raise RuntimeError("failed to get enough points of "+str(x))

            try:
                cp = pc.neighborhood_graph(epsilon, method = "subdivision").connected_components_1()
                print "connected componenets",cp

            except:
                raise RuntimeError("failed to get the connected components of "+str(x))

# plotting based on dimension
            dim = pc.dimension()

            try:
                if dim == 2:
                    pc.plot2d(save = save)
                    if pc.plot2d_neighborhood_graph(epsilon, save = save) != True:
                        raise RuntimeError("failed to plot2d "+str(x))
                if dim == 3:
                    pc.plot3d(save = save)
                    if pc.plot3d_neighborhood_graph(epsilon, save = save) != True:
                        raise RuntimeError("failed to plot3d "+str(x))

            except:
                raise RuntimeError("failed to generate a plot of dimension \""+str(dim)+"\"")

        except RuntimeError as inst:
            print inst.args[0], " uh oh, trying next test"
    


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
    
