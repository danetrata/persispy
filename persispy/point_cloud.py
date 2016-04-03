'''
File: point_cloud.py

The PointCloud data structure and related functions.

AUTHORS:

    - Daniel Etrata (2015-11)
    - Benjamin Antieau (2015-04)

TODO: We should look to seperate the methods that generate points
and the methods that act on those points.
Left alone for now because many modules rely on this.

'''

import math
import os as os

import numpy as np
# from numpy import array
# import matplotlib as mpl
import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d.axes3d as plt3
# import mpl_toolkits.mplot3d as a3

from persispy.weighted_simplicial_complex import wGraph
from persispy.hashing import HashPoint
# from persispy.hashing import HashEdge


class PointCloud(object):

    '''
    Points should be a list of hashable objects.
    Variables   :
        _points : a array of hashable points.
        _space  : either 'affine' or 'projective'.
    '''

    def __init__(self, points, space='affine', gui=False):
        try:
            self._points = list(points)
            import sys
            if len(self._points) > 1000:
                sys.setrecursionlimit(len(self._points)**2)
        except TypeError:
            raise TypeError('Input points should be a list of points.')
        try:
            hash(self._points[0])
        except TypeError:
            print("Detected points are not hashable." +
                  "Attempting to convert to HashPoints.")
            self._points = [
                HashPoint(points[n],
                          index=n) for n in range(
                    len(points))]
#             raise TypeError('Input points should be of hashable points.')
        if space != 'affine' and space != 'projective':
            raise TypeError('The argument "space" should be set to' +
                            'either "affine" or "projective".')

        self._space = space
        self._fig = None
        self.gui = gui

    def __repr__(self):
        try:
            repr(self.dimension())
        except AttributeError:
            raise AttributeError(
                'The numpy array must be a single set of points.')
        return 'Point cloud with ' + repr(self.num_points()) + \
            ' points in real ' + self._space + \
            ' space of dimension ' + repr(self.dimension())

    def get_points(self):
        """
        We return the PointCloud's points.
        """
        return self._points

    def get_space(self):
        """
        We return the PointCloud's space.
        """
        return self._space

    def __len__(self):
        return len(self._points)

    def size(self):
        return len(self._points)

    def __getitem__(self, key):
        return tuple(self._points[key]._coords)

    def num_points(self):
        return len(self._points)

    def dimension(self):
        if self._space == 'affine':
            return len(self._points[0]._coords)
        elif self._space == 'projective':
            return len(self._points[0]._coords) - 1

    def plot2d(self, *args, **kwargs):
        """
        redirecting plotting methods
        """
        from persispy.plot import plot2d
        print ("warning: PointCloud.plot2d() depreciated, use instead")
        print (">>> persispy.plot.plot2d(PointCloud)")
        plot2d(self, *args, **kwargs)

    def plot3d(self, *args, **kwargs):
        """
        redirecting plotting methods
        """
        from persispy.plot import plot3d
        print ("warning: PointCloud.plot3d() depreciated, use instead")
        print (">>> persispy.plot.plot3d(PointCloud)")
        plot3d(self, *args, **kwargs)

    def plot2d_neighborhood_graph(self, epsilon, *args, **kwargs):
        """
        redirecting plotting methods
        """
        from persispy.plot import plot2d
        print ("warning: PointCloud.plot2d_neighborhood_graph()" +
               "depreciated, use instead")
        print (">>> persispy.plot.plot2d(wGraph)")
        wgraph = self.neighborhood_graph(epsilon)
        plot2d(wgraph, *args, **kwargs)

    def plot3d_neighborhood_graph(self, epsilon, *args, **kwargs):
        """
        redirecting plotting methods
        """
        from persispy.plot import plot3d
        wgraph = self.neighborhood_graph(epsilon)
        print ("warning: PointCloud.plot3d_neighborhood_graph()" +
               "depreciated, use instead")
        print (">>> persispy.plot.plot3d(wGraph)")
        plot3d(wgraph, *args, **kwargs)

    # Makes movie of 2-dimensional plots
    def film_neighborhood_graph(
            self,
            step,
            num_steps,
            fps=24,
            method='subdivision',
            file_name='movie.mp4'):
        '''
        WARNING: do not run this in a Dropbox folder.

        WARNING: this function rewrites movie.mp4 in the working
        directory by default. To change this, add
        file_name='your_file_name.mp4' to the function call.

        WARNING: this function is currently very slow for large data
        sets, thanks it seems to the slowness in plotting so many
        points.
        '''
        if self._space == 'affine':
            epsilon = 0
            h = self.neighborhood_graph(step * num_steps, method)
            os.system("rm _tmp*.png")
            fig, (ax) = plt.subplots(1, 1)
            # Resolution of video
            # Example: (10,10) gives a 1000x1000 pixel resolution video
            fig.set_size_inches(10.0, 10.0)
            for i in range(num_steps):
                epsilon = epsilon + step
                g = h.neighborhood_graph(epsilon)
                for p in self._points:
                    if p._coords[2] <= 0:
                        for e in g._adj[p]:
                            ax.plot([e[0]._coords[0], p._coords[0]], [e[0]._coords[1], p._coords[
                                    1]], color=(.5 * p._coords[2] + .5, .5, .5, .5))
                for p in self._points:
                    if p._coords[2] > 0:
                        for e in g._adj[p]:
                            ax.plot([e[0]._coords[0], p._coords[0]], [e[0]._coords[1], p._coords[
                                    1]], color=(.5 * p._coords[2] + .5, .5, .5, .5))

                ax.grid(True)
                ax.set_aspect('equal')
                plt.setp([a.get_xticklabels()
                          for a in fig.axes[:-1]], visible=False)
                # Graph bounds
                # Depends on point cloud used, values (-3,3) and (-3,3) work for
                # torus
                ax.set_xlim(-3, 3)
                ax.set_ylim(-3, 3)
                fname = '_tmp%05d.png' % i
                plt.savefig(fname)
                plt.cla()
            plt.close(fig)
            os.system("rm " + file_name)
            # Movie maker command
            # Changed to "avconv" from "ffmpeg", change back if older system
            # (options are the same)
            os.system("avconv -r " + str(fps) + " -i _tmp%05d.png " + file_name)
            os.system("rm _tmp*.png")
            return None
        else:
            return None

    def neighborhood_graph(self,
                           epsilon,
                           method="subdivision"):
        """
        calls the recursive function ._neighborhood_graph(...)
        """
        return self._neighborhood_graph(
            epsilon,
            method,
            self._points,
            {v: set() for v in self._points})

    def _neighborhood_graph(self,
                            epsilon,
                            method,
                            pointarray,
                            dictionary):
        '''
        The 'method' string is separated by spaces. Acceptable values:

        "exact"                     does "exact"
        "subdivision"               does "subdivision" to infinite depth
        "subdivision 3"             does "subdivision" to depth 3, then "exact"
        "subdivision 7 approximate" does "subdivision" to depth 7, then "approximate"

        '''
        methodarray = method.split(' ')

        if methodarray[0] == 'subdivision':

            if self._space == 'projective':
                return self.neighborhood_graph(epsilon, method='exact')
            elif self._space == 'affine':
                if len(methodarray) > 1:
                    d = int(methodarray[1])
                    m = ''
                    for i in range(len(methodarray) - 2):
                        m = m + methodarray[i + 2]
                        m = m + ' '

                    if m == '':
                        self._subdivide_neighbors(epsilon,
                                                  dictionary,
                                                  pointarray,
                                                  depth=d)
                        return wGraph(dictionary, epsilon)
                    else:
                        self._subdivide_neighbors(epsilon,
                                                  dictionary,
                                                  pointarray,
                                                  coordinate=m,
                                                  depth=d)
                        return wGraph(dictionary, epsilon)
                else:  # most calls end up here
                      #  also starts the recursion
                    self._subdivide_neighbors(epsilon, dictionary, pointarray)
                    # mystery dictionary assignments..?
                    # {point: {adj points:distance}}
                    return wGraph(dictionary, epsilon)

        elif methodarray[0] == 'exact':
            '''
            Issue: this doesn't work because lists and numpy arrays are not hashable.
            '''
            for i in range(len(self._points)):
                for j in range(i + 1, len(self._points)):
                    if self._space == 'affine':
                        dist = np.sqrt(
                            sum((self._points[i]._coords - self._points[j]._coords)**2))
                        if dist < epsilon:
                            dictionary[self._points[i]].add(
                                (self._points[j], dist))
                            dictionary[self._points[j]].add(
                                (self._points[i], dist))
                    elif self._space == 'projective':
                        return None
            return wGraph(dictionary, epsilon)

        elif methodarray[0] == 'approximate':
            return None
        elif methodarray[0] == 'randomized':
            return None
        elif methodarray[0] == 'landmarking':
            return None

        else:
            raise TypeError(
                'Method should be one of subdivision, exact, approximate, randomized, or landmarking.')

    def _selectpoint(self, pointarray, k, n):
        """
        gives the kth smallest point of "self._points", according to the nth coordinate
        we use this to give the median, but a general solution for k is needed for the recursive algorithm
        this algorithm is O(n) for best and worst cases
        """

        a = pointarray[:]
        c = []
        while(len(a) > 5):
            for x in range(int(math.floor(len(a) / 5))):
                b = pointarray[5 * x:5 * x + 5]
                b.sort(key=lambda x: x._coords[n])
                c.append(b[int(math.floor(len(b) / 2))])
            a = c
            c = []
        pivot = a[int(math.floor(len(a) / 2))]

        lesser = [
            point for point in pointarray
            if point._coords[n] < pivot._coords[n]]
        if len(lesser) > k:
            return self._selectpoint(lesser, k, n)  # recursive
        k -= len(lesser)

        equal = [
            point for point in pointarray
            if point._coords[n] == pivot._coords[n]]
        if len(equal) > k:
            return pivot  # basecase
        k -= len(equal)

        greater = [
            point for point in pointarray
            if point._coords[n] > pivot._coords[n]]
        return self._selectpoint(greater, k, n)  # recursive

    def _subdivide_neighbors(
            self,
            e,
            dictionary,
            pointarray,
            coordinate=0,
            method='exact',
            depth=-1):
        """
        @Mason: document 'e' please.

        method and depth are accumulators for the recursive calls
        divides the space into two regions about the median point relative to "coordinate"
        glues the two regions, then recursively calls itself on the two regions.
        """
        if len(pointarray) > 1:
            median = self._selectpoint(
                pointarray, len(pointarray) / 2, coordinate)
            smaller = []
            bigger = []
            gluesmaller = []
            gluebigger = []

            #split into two regions
            for i, _ in enumerate(pointarray):
                if pointarray[i]._coords[
                        coordinate] < median._coords[coordinate]:
                    smaller.append(pointarray[i])
                    if pointarray[i]._coords[
                            coordinate] > median._coords[coordinate] - e:
                        gluesmaller.append(pointarray[i])

                if pointarray[i]._coords[
                        coordinate] >= median._coords[coordinate]:
                    bigger.append(pointarray[i])
                    if pointarray[i]._coords[
                            coordinate] < median._coords[coordinate] + e:
                        gluebigger.append(pointarray[i])

            #glue together the two regions
            for i, _ in enumerate(gluesmaller):
                for j, _ in enumerate(gluebigger):
                    dist = np.sqrt(
                        sum(
                            ((gluesmaller[i])._coords - gluebigger[j]._coords) *
                            (gluesmaller[i]._coords - gluebigger[j]._coords)))
                    if dist < e:
                        dictionary[gluesmaller[i]].add((gluebigger[j], dist))
                        dictionary[gluebigger[j]].add((gluesmaller[i], dist))

            if depth == -1:  # depth -1 means fully recursive. all edges are formed by "gluing"
                coordinate = (coordinate + 1) % self.dimension()
                self._subdivide_neighbors(
                    e, dictionary, smaller, coordinate, method, depth=-1)
                self._subdivide_neighbors(
                    e, dictionary, bigger, coordinate, method, depth=-1)
            if depth > 0:
                coordinate = (coordinate + 1) % self.dimension()
                self._subdivide_neighbors(e, depth - 1, coordinate, smaller)
                self._subdivide_neighbors(e, depth - 1, coordinate, bigger)
            if depth == 0:
                self._neighborhood_graph(e, method, smaller, dictionary)
                self._neighborhood_graph(e, method, bigger, dictionary)
