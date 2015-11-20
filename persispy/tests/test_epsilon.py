# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex

pDict = {
    "circle"     : "x^2 + y^2 - 1",
    "sphere"     : "x^2 + y^2 + z^2 - 1",
    "torus"      : "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "hyperbolid" : "x^2 + y^2 - z^2 - 1",
    "line"       : "a*x",
    "quadratic"  : "a*x^2 + b*x + c",
    "cubic"      : "a*x^3 + b*x^2 + c*x + d",
    "quartic"    : "a*x^4 + b*x^3 + c*x^2 + d*x + e"
}



def main():

    runs = 0
    pc = phc(pDict["quadratic"], num_points)
    z = "small"
    while runs < 10:
        runs = runs + 1

        for epsilon in [0.2, 0.1]:
            pc.neighborhood_graph(epsilon, "subdivision")

            x = len(pc.points)
            y = pc.degree

        pc.find_more_points(1000)

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
    
