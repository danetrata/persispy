# Summary of changes.
# hash_point.HashPoint moved to ../hash_point.py
# "points_*" in definition removed.
# added backwards compatablity. eg: points/points_2sphere.py

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
from persispy import point_cloud, hash_point
import numpy as np


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
        return point_cloud.PointCloud([hash_point.HashPoint(normalize(2*npr.random(3)-1),index=n) for n in range(num_points)],space='affine')
    elif method=='rectangular':
        angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
        return point_cloud.PointCloud([hash_point.HashPoint(radius*np.array([np.sin(angles[n][0])*np.cos(angles[n][1]),np.sin(angles[n][0])*np.sin(angles[n][1]),np.cos(angles[n][0])]),index=n) for n in range(num_points)],space='affine')
    elif method=='rejection':
        count = 0
        points=[]
        while count<num_points:
            pt=2*npr.random(3)-1
            if np.sqrt(sum(pt*pt)) <= radius:
                points.append(hash_point.HashPoint(normalize(pt),count))
                count=count+1
        return point_cloud.PointCloud(points,space='affine')
    else:
        raise TypeError('The argument "method" should be either "normalized", "rectangular", or "rejection".')

def torus(num_points):
    '''
    EXAMPLES:
    >>> points_3d_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    hp = [hash_point.HashPoint(np.array([(2+np.cos(angles[n][0]))*np.cos(angles[n][1]),
        (2+np.cos(angles[n][0]))*np.sin(angles[n][1]),
        np.sin(angles[n][0])]),index=n) for n in range(num_points)]
    return point_cloud.PointCloud(hp,space='affine')

def flat_torus(num_points):
    '''
    EXAMPES:
    >>> points_flat_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    return point_cloud.PointCloud([hash_point.HashPoint(np.array([np.cos(angles[n][0]),np.sin(angles[n][0]),np.cos(angles[n][1]),np.sin(angles[n][1])]),index=n) for n in range(num_points)],space='affine')

def cube(dim,num_points):
    '''
    EXAMPLES:
    >>> points_cube(4,1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    return point_cloud.PointCloud([hash_point.HashPoint(npr.random(dim),index=n) for n in range(num_points)],space='affine')

def plane(num_points):
    return point_cloud.PointCloud(
            [hash_point.HashPoint(
                npr.uniform(0, 1, size=2), 
                index=n) 
                for n in range(num_points)], 
            space='affine')

