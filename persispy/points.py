# Summary of changes.
# hash_point.HashPoint moved to ../hash_point.py
# "points_*" in definition removed.

'''
File: examples.py

Several functions that produce instances of the PointCloud class.

AUTHORS:

    - Benjamin Antieau (2015-04)

This module contains several functions that produce PointClouds, and it
contains the definition of the hash_point.HashPoint class. This provids a wrapping up a
numpy.array that is suitable for hashing. A hashable 'point' is necessary for
certain subroutines of the PointCloud class, especially the neighborhood_graph
function.
'''

import numpy.random as npr
import scipy.constants as scic
import numpy as np

from point_cloud import PointCloud
from hash_point import HashPoint


# 3d examples
def sphere(num_points,radius=1,method='rejection'):
    '''
    Returns a PointCloud with num_points random points on the 2-sphere of given radius. With
    method=='normalized', random points are plotted in the unit cube, and then divided by
    their length. With method=='rectangular', random polar coordinates are given. With
    method=='rejection', a rejection method is given to produce actually equidistributed
    points on the 2-sphere with its usual measure.

    EXAMPLES:
    >>> points_2sphere(1000,radius=4)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    def normalize(x):
        return (1/np.sqrt(sum(x*x)))*x
    if method=='normalized':
        return PointCloud([HashPoint(normalize(2*npr.random(3)-1),index=n) for n in range(num_points)],space='affine')
    elif method=='rectangular':
        angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
        return PointCloud([HashPoint(radius*np.array([np.sin(angles[n][0])*np.cos(angles[n][1]),np.sin(angles[n][0])*np.sin(angles[n][1]),np.cos(angles[n][0])]),index=n) for n in range(num_points)],space='affine')
    elif method=='rejection':
        count = 0
        points=[]
        while count<num_points:
            pt=2*npr.random(3)-1
            if np.sqrt(sum(pt*pt)) <= radius:
                points.append(HashPoint(normalize(pt),count))
                count=count+1
        return PointCloud(points,space='affine')
    else:
        raise TypeError('The argument "method" should be either "normalized", "rectangular", or "rejection".')

def torus(num_points, gui = False):
    '''
    EXAMPLES:
    >>> points_3d_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    hp = [HashPoint(np.array([(2+np.cos(angles[n][0]))*np.cos(angles[n][1]),
        (2+np.cos(angles[n][0]))*np.sin(angles[n][1]),
        np.sin(angles[n][0])]),index=n) for n in range(num_points)]
    return PointCloud(hp, space='affine', gui = gui)

def flat_torus(num_points):
    '''
    EXAMPES:
    >>> points_flat_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    return PointCloud([HashPoint(np.array([np.cos(angles[n][0]),np.sin(angles[n][0]),np.cos(angles[n][1]),np.sin(angles[n][1])]),index=n) for n in range(num_points)],space='affine')

def cube(dim,num_points):
    '''
    EXAMPLES:
    >>> points_cube(4,1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    return PointCloud([HashPoint(npr.random(dim),index=n) for n in range(num_points)],space='affine')

def plane(num_points, side_length = 1, seed = False, return_seed = False):
    """
    takes the number of points and returns a list of 
    uniform distribution of points
    {(x,y): 0 < x < 1, 0 < y < 1}
    Optional:
    seed        - sets a particular random state
    return_seed - returns a descriptive tuple of the random state
    """
    if seed:
        npr.seed(seed)

    if return_seed:
        return_seed = npr.get_state()
        return (PointCloud(
                [HashPoint(
                    npr.uniform(-side_length, side_length, size=2), 
                    index=n) 
                    for n in range(num_points)], 
                space='affine'),
                return_seed
                )

    else:
        return PointCloud(
                [HashPoint(
                    npr.uniform(-side_length, side_length, size=2), 
                    index=n) 
                    for n in range(num_points)], 
                space='affine')





def wrapper():
    npr.seed(1991)
    pc = plane(1500, 3)
    ng = pc.neighborhood_graph(0.2)
    return ng.connected_components()

def wrapper1():
    npr.seed(1991)
    pc = plane(1500, 3)
    ng = pc.neighborhood_graph(0.2)
    return ng.connected_components_1()

def time_cp():
    import timeit as t
    print ".connected_components(): %f" % t.timeit(wrapper, number = 10)
    print ".connected_components_1(): %f" % t.timeit(wrapper1, number = 10)


def main():
    

    import time
    import sys

    toolbar_width = 40

# setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    for i in xrange(toolbar_width):
        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")




def save_to_file(data):
    """
    Prompts the user for a file name
    and writes the data to file.
    """
    name = raw_input("give a file name : ")
    datafile = open(name, 'w')
    datafile.write(str(data))
    datafile.close()


if __name__ == "__main__": main()

