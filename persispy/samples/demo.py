from persispy import point_cloud
from persispy.samples import points



def main():
  point_cloud.PointCloud.plot3d(points.sphere(1000))
  point_cloud.PointCloud.plot3d(points.torus(1000))
  point_cloud.PointCloud.plot3d(points.flat_torus(1000))
  point_cloud.PointCloud.plot3d(points.cube(4,1000))

if __name__=="__main__": main()
