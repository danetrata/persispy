import persispy as persispy
from phc_interface import phc_2d_cloud
from phc_interface import phc_3d_cloud
from point_cloud import PointCloud

def main():
    # PointCloud.plot2d(phc_2d_cloud())
    # PointCloud.plot2d(phc_2d_cloud(nTimes =1000))
    # PointCloud.plot3d(phc_2d_cloud(intersectWith="plane"))
    # TODO: decision to make a 2d/3d cloud
    # PointCloud.plot3d(phc_cloud())
    # PointCloud.plot3d(phc_3d_cloud(eqn= "x^2 + y^2 + z^2 - 1",nTimes = 100))

    PointCloud.plot3d(phc_3d_cloud())
    PointCloud.plot3d(phc_3d_cloud(nPoints = 1000,LOUD=True))
    PointCloud.plot3d(phc_3d_cloud(eqn = "x^2 + y^2 + z^2 -1", nPoints = 1000,LOUD=True))

    

if __name__== "__main__": main()



