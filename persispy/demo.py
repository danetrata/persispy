import persispy
from examples import *
from point_cloud import PointCloud 

def main():
  PointCloud.plot3d(points_2sphere(1000))
  PointCloud.plot3d(points_3d_torus(1000))
  PointCloud.plot3d(points_flat_torus(1000))
  PointCloud.plot3d(points_cube(4,1000))

if __name__=="__main__": main()
