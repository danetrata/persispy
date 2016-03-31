# Summary of changes.
# hash_point.HashPoint moved to ../hash_point.py
# "points_*" in definition removed.

'''
File: examples.py

Several functions that produce instances of the PointCloud class.

AUTHORS:

    - Benjamin Antieau (2015-04)

This module contains several functions that produce PointClouds, and it
contains the definition of the hashing.HashPoint class. This provides a wrapping up a
numpy.array that is suitable for hashing. A hashable 'point' is necessary for
certain subroutines of the PointCloud class, especially the neighborhood_graph
function.
'''

import numpy as np
import numpy.random as npr
import scipy.constants as scic

from persispy.point_cloud import PointCloud
from persispy.hashing import HashPoint

def circle(num_points,radius=1):
    '''
    Returns a PointCloud with num_points random points on the circle (1-sphere) of given
    radius centered at the origin in R^2.

    EXAMPLES:
    >>> circle(1000,radius=4)
    PointCloud with 1000 points in real affine space of dimension 2
    '''
    angles = np.array([(2*scic.pi)*npr.random() for n in range(num_points)])
    return PointCloud([HashPoint([np.cos(theta),np.sin(theta)],index) for index,theta in
        enumerate(angles)])

# 3d examples
def sphere(num_points,radius=1,method='rejection'):
    '''
    Returns a PointCloud with num_points random points on the 2-sphere of given radius. With
    method=='normalized', random points are plotted in the unit cube, and then divided by
    their length. With method=='rectangular', random polar coordinates are given. With
    method=='rejection', a rejection method is given to produce actually equidistributed
    points on the 2-sphere with its usual measure.

    EXAMPLES:
    >>> sphere(1000,radius=4)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    def normalize(x):
        return (1/np.sqrt(sum(x*x)))*x
    if method == 'normalized':
        return PointCloud([HashPoint(normalize(2*npr.random(3)-1),index=n) for n in range(num_points)],space='affine')
    elif method == 'rectangular':
        angles = np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
        return PointCloud([HashPoint(radius*np.array([np.sin(angles[n][0])*np.cos(angles[n][1]),np.sin(angles[n][0])*np.sin(angles[n][1]),np.cos(angles[n][0])]),index=n) for n in range(num_points)],space='affine')
    elif method == 'rejection':
        count = 0
        points = []
        while count < num_points:
            pt = 2*npr.random(3)-1
            if np.sqrt(sum(pt*pt)) <= radius:
                points.append(HashPoint(normalize(pt), count))
                count = count+1
        return PointCloud(points, space='affine')
    else:
        raise TypeError('The argument "method" should be either "normalized", "rectangular", or "rejection".')

def torus(num_points, gui = False):
    '''
    EXAMPLES:
    >>> torus(1000)
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
    >>> flat_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    return PointCloud([HashPoint(np.array([np.cos(angles[n][0]),np.sin(angles[n][0]),np.cos(angles[n][1]),np.sin(angles[n][1])]),index=n) for n in range(num_points)],space='affine')

def box(number_of_points, 
        dimension = 2, 
        side_length = 1, 
        seed = False, 
        return_seed = False):
    """
    We return a set of points in a box of given dimension. On default, returns
    a unit box in the plane. We can specify a str or int seed. We can also ask to return the seed
    used to generate a run. Note, the returned seed is a ndarray of 624 uints.
    """
    if seed:
        npr.seed(seed)

    result = PointCloud(
                [HashPoint(
                    npr.uniform(-side_length/2, 
                        side_length/2, 
                        size = dimension), 
                    index=n) 
                    for n in range(number_of_points)], 
                space='affine')

    if return_seed:
        return_seed = npr.get_state()
        result = (result, return_seed)

    return result

# How is this different from box?
def cube(dim,num_points):
    '''
    EXAMPLES:
    >>> cube(4,1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    return PointCloud([HashPoint(npr.random(dim),index=n) for n in range(num_points)],space='affine')

# How is this different from box?
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

    result = PointCloud(
                [HashPoint(
                    npr.uniform(-side_length, side_length, size=2), 
                    index=n) 
                    for n in range(num_points)], 
                space='affine')

    if return_seed:
        return_seed = npr.get_state()
        result = (result, return_seed)

    return result

def save_to_file(data):
    """
    Prompts the user for a file name
    and writes the data to file.
    """
    name = raw_input("give a file name : ")
    datafile = open(name, 'w')
    datafile.write(str(data))
    datafile.close()

def main():
    
    pass





if __name__ == "__main__": main()

