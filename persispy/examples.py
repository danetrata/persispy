'''
File: examples.py

Several functions that produce instances of the PointCloud class.

AUTHORS:

    - Benjamin Antieau (2015-04)

This module contains several functions that produce PointClouds, and it
contains the definition of the HashPoint class. This provids a wrapping up a
numpy.array that is suitable for hashing. A hashable 'point' is necessary for
certain subroutines of the PointCloud class, especially the neighborhood_graph
function.
'''

import numpy as np
import numpy.random as npr
import scipy.constants as scic
import point_cloud as point_cloud
import hashlib as hashlib

class HashPoint:
    '''
    A wrapped numpy array to allow hashing.

    Vars: _coords (a numpy array).

    EXAMPLES:
    >>> HashPoint([1,2,3])
    array([1, 2, 3])
    '''
    def __init__(self,coords,index):
        self._coords=np.array(coords)
        self._index=index
    def __hash__(self):
        try:
            out=self._hash
            return out
        except:
            self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
            return self._hash

    def __repr__(self):
        return "point "+str(self._index)+": "+str(self._coords.__repr__())[6:-1]
    def __cmp__(self,other):
        return self._index.__cmp__(other._index)

def points_2sphere(num_points,radius=1,method='normalized'):
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
        return point_cloud.PointCloud([HashPoint(normalize(2*npr.random(3)-1),n) for n in range(num_points)],space='affine')
    elif method=='rectangular':
        angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
        return point_cloud.PointCloud([HashPoint(radius*np.array([np.sin(t[0])*np.cos(t[1]),np.sin(t[0])*np.sin(t[1]),np.cos(t[0])])) for t in angles],space='affine')
    elif method=='rejection':
        count = 0
        points=[]
        while count<num_points:
            pt=2*npr.random(3)-1
            if np.sqrt(sum(pt*pt)) <= radius:
                points.append(HashPoint(normalize(pt)))
                count=count+1
        return point_cloud.PointCloud(points,space='affine')
    else:
        raise TypeError('The argument "method" should be either "normalized", "rectangular", or "rejection".')

def points_3d_torus(num_points):
    '''
    EXAMPLES:
    >>> points_3d_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 3
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    print angles
    print "length",len(angles)
    print "length of element",len(angles[0])
    hp = [HashPoint(np.array([(2+np.cos(t[0]))*np.cos(t[1]),
        (2+np.cos(t[0]))*np.sin(t[1]),
        np.sin(t[0])])) for t in angles]
    print "hp",hp
    return point_cloud.PointCloud(hp,space='affine')


def points_flat_torus(num_points):
    '''
    EXAMPES:
    >>> points_flat_torus(1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    angles=np.array([2*scic.pi*npr.random(2) for n in range(num_points)])
    return point_cloud.PointCloud([HashPoint(np.array([np.cos(t[0]),np.sin(t[0]),np.cos(t[1]),np.sin(t[1])])) for t in angles],space='affine')

def points_cube(dim,num_points):
    '''
    EXAMPLES:
    >>> points_cube(4,1000)
    Point cloud with 1000 points in real affine space of dimension 4
    '''
    return point_cloud.PointCloud([HashPoint(npr.random(dim)) for n in range(num_points)],space='affine')
