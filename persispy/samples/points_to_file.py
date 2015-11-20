"""
generating 1000 points of the following varities:
    
    sphere
    x^2 + y^2 + z^2 - 1
    
    torus
    16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2

    hyperbolid:
    x^2 + y^2 - z^2 - 1

outputs to .txt files of the same name
"""

pointDict = {
    "sphere": "x^2 + y^2 + z^2 - 1",
    "torus": "16*x^2 + 16*y^2 - (x^2 + y^2 + z^2 + 3)^2",
    "hyperbolid": "x^2 + y^2 - z^2 - 1"
}

from persispy.phc.interface import phc_cloud

def main():
    for name in pointDict.viewkeys():
        f = open(name + ".txt", 'w')
        phcCloud = phc_cloud(pointDict[name], num_points = 1000, bounds = 6, DEBUG=True, point_cloud=False)
        f.write(str(phcCloud))
        f.close()


if __name__=="__main__": main()
