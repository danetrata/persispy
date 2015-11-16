# TODO: epsilon is a function of coefficients, number of points, and degree
from persispy.phc.interface import phc_cloud
from persispy.weighted_simplicial_complex import wGraph

pointDict = {
    "sphere": "x^2 + y^2 + z^2 - 1",
    "torus": "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "hyperbolid": "x^2 + y^2 - z^2 - 1"
}

def main():
    phcCloud = phc_cloud(eqn = pointDict["sphere"], num_points = 500) 
    wGraph.neighborhood_graph(wGraph(phcCloud),0.1)





if __name__ == "__main__": main()
    
