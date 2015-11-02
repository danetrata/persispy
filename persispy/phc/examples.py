from persispy.phc.interface import phc_2d_cloud, phc_3d_cloud, phc_cloud 
from persispy.point_cloud import PointCloud

def main():
    # PointCloud.plot2d(phc_2d_cloud())
    # PointCloud.plot2d(phc_2d_cloud(nTimes =1000))
    # PointCloud.plot3d(phc_2d_cloud(intersectWith="plane"))
    # TODO: decision to make a 2d/3d cloud
    # PointCloud.plot3d(phc_cloud())
    # PointCloud.plot3d(phc_3d_cloud(eqn= "x^2 + y^2 + z^2 - 1",nTimes = 100))

    #PointCloud.plot3d(phc_3d_cloud())
#     PointCloud.plot3d(phc_3d_cloud(eqn = "x^2 + t^2 - 1", nPoints = 200,DEBUG=True))
#     PointCloud.plot3d(phc_3d_cloud(eqn = "x^2 + y^2 -1", nPoints = 200,DEBUG=True))
#     PointCloud.plot3d(phc_3d_cloud(eqn = "x^2 + y^2 + z^2 -1", nPoints = 1000))

    PointCloud.plot2d(phc_cloud(eqn = "x^2 + y^2 - 1", nPoints = 100, DEBUG=True))
    
    

if __name__== "__main__": main()



