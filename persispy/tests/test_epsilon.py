# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.interface import phc_cloud
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wSimplex, wGraph, wSimplicialComplex

pointDict = {
    "circle": "x^2 + y^2 - 1",
    "sphere": "x^2 + y^2 + z^2 - 1",
    "torus": "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "hyperbolid": "x^2 + y^2 - z^2 - 1"
}

def main():
    phcCloud = phc_cloud(eqn = pointDict["circle"], num_points = 1000) 
    ng = phcCloud.neighborhood_graph(.01, "subdivision")
    print ng
    print ng.connected_components_1()





if __name__ == "__main__": main()
    
