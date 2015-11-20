# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.points import phc
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex

pointDict = {
    "circle": "x^2 + y^2 - 1",
    "sphere": "x^2 + y^2 + z^2 - 1",
    "torus": "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "hyperbolid": "x^2 + y^2 - z^2 - 1"
}

def test_coefficients():
    pc = phc(eqn = pointDict["circle"], num_points = 1000) 
    ng = pc.neighborhood_graph(.01, "subdivision")
    print ng
    print ng.connected_components_1()

def test_degree():
    pass

def test_number_of_points():
    pass

def main():

    test_coefficients()
    test_number_of_points()
    test_degree()




if __name__ == "__main__": main()
    
