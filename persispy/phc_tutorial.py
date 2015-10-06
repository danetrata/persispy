import numpy as np
import hashlib
class HashPoint:
  '''
  A wrapped numpy array to allow hashing.
  Vars: _coords (a numpy array).
  EXAMPLES:
  >>> HashPoint([1,2,3])
  array([1, 2, 3])
  '''
  def __init__(self,coords):
    self._coords=np.array(coords)
    def __hash__(self):
      try:
        out=self._hash
        print "out:",out
        return out
      except:
        self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
        return self._hash
      def __repr__(self):
        return self._coords.__repr__()

"""
This file is only meant to demonstrate some of the functions of phcpy.
See 'phc_interface.py' for persispy
"""

import phcpy

# returns nothing
def phc_print(phcOut):
  for sol in phcOut: print sol
  print "\n\n"

# prototype for interface 
# returns a set of points given the raw string from phc
def solution_parser(raw_sol):
  from phcpy.solutions import coordinates # points
  points = []
  for i in raw_sol:
    point = coordinates(i)
    coords = point[1][0],point[1][1]
    points.append(coords)
  return points

def example1(): 
# returns nothing, prints coordinates with a fixed seed
  from phcpy.solver import random_trinomials # gen polynomials
  from phcpy.solver import solve # main solver
  from phcpy.solutions import coordinates # points
  from phcpy.phcpy2c import py2c_set_seed # for fixed runs

  py2c_set_seed(2015) # setting seed
  f = random_trinomials()
  print "trinomial:",f
  s = solve(f)

# each element of 's' looks like 
  """
  t :  1.00000000000000E+00   0.00000000000000E+00
  m : 1
  the solution for t :
   x :  7.07106781186547E-01   7.59645419660784E-65
   y :  7.07106781186547E-01   3.79822709830392E-65
  == err :  1.570E-16 = rco :  4.142E-01 = res :  2.220E-16 =
  """
    
  points = []
  for i in s:
    point = coordinates(i)
    points.append(point)

  print points 
# structure of points
  """
  [(['x', 'y'], [(4.49888308849791e-45+6.12143301552416e-45j), (-6.86339249904575e-47-2.58723623936925e-47j)]),... 
  """
  print type(points[0][1][0])
  for i in points:
    print "x:",i[1][0]
    print "y:",i[1][1]

# hacking together a working copy
# from examples.py
def example3():
  import numpy as np
  import hashlib
  class HashPoint:
    '''
    A wrapped numpy array to allow hashing.
    Vars: _coords (a numpy array).
    EXAMPLES:
    >>> HashPoint([1,2,3])
    array([1, 2, 3])
    '''
    def __init__(self,coords):
      self._coords=np.array(coords)
      def __hash__(self):
        try:
          out=self._hash
          print "out:",out
          return out
        except:
          self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
          return self._hash
        def __repr__(self):
          return self._coords.__repr__()

  def points_3d_torus(num_points):
    import numpy as np
    import numpy.random as npr
    import scipy.constants as scic
    import point_cloud
    '''
    EXAMPLES:
    >>> points_3d_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    # step 1: generate a list of random coefficients 
    angles=np.array(
      [2*scic.pi*npr.random(2) for n in range(num_points)]
    )
    print angles
    print "length of angles",len(angles)
    npPoints = [np.array([
      (2+np.cos(t[0]))*np.cos(t[1]),#the equation of a torus 
      (2+np.cos(t[0]))*np.sin(t[1]),#as a parametric equation
      np.sin(t[0])]) 
      for t in angles] #using the list of coefficients 
    print npPoints
    return(
      point_cloud.PointCloud(
        [HashPoint(np.array([
          (2+np.cos(t[0]))*np.cos(t[1]),#the equation of a torus 
          (2+np.cos(t[0]))*np.sin(t[1]),#as a parametric equation
          np.sin(t[0])])) 
          for t in angles], #using the list of coefficients 
          space='affine'
      )
    )

  import persispy
  from point_cloud import PointCloud
  PointCloud.plot3d(points_3d_torus(1000))

def example2():
  from phcpy.solver import total_degree
  from phcpy.solver import total_degree_start_system
  from phcpy.trackers import track
  # design note: input is in strings?!
  p = ['x^2 + y^2 -1;','x - y;']
  print "total degrees:",total_degree(p)
  (q,qsols)=total_degree_start_system(p)
  print "length of solutions:",len(qsols)
  print "homotopy:",q
  print "\n\nq solutions:"
  phc_print(qsols)
  s = track(p,q,qsols)
  print "length of paths:",len(s)
  print "\n\ns solutions:"
  phc_print(s)

def example4():
  import numpy as np
  from phcpy import solver
  """
  array = np.array()
  goal
  cloudPoints = HashPoint
  to plot
  PointCloud.plot3d(cloudPoints)
  """



# just randomize x and y
def example5():
  from phcpy.solver import total_degree
  from phcpy.solver import total_degree_start_system
  from phcpy.trackers import track
  from scipy.constants import pi 
  from numpy.random import uniform
  from phcpy.solver import solve

  POINTS = 1000
  linearIntersects = [] 
  # creating a list of random lines to intersect
  for item in range(0,POINTS):
    a,b = uniform(-1,1,size=2)
    line = str(a)+"*x + "+str(b)+"*y;"
    linearIntersects.append(line)
    
  points_raw = []
  for line in linearIntersects:
    p = ["x^2 + y^2 - 1;",line]
    (q, qsols) = total_degree_start_system(p)
    sol = track(p, q, qsols) 
    for item in solution_parser(sol):
      points_raw.append(solution_parser(sol))
  print points_raw[0]
  points = []
  for item in points_raw:
    points.append(np.array(item[0])) #
  print len(points)
  print points

  import persispy
  import point_cloud
  from point_cloud import PointCloud

  cloudPoints = [HashPoint(x) for x in points]
  PointCloud.plot2d(point_cloud.PointCloud(cloudPoints))
  
        


