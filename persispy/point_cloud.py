# TODO: We should look to seperate the methods that generate points
# and the methods that act on those points.
# Left alone for now because many modules rely on this.

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3
import mpl_toolkits.mplot3d as a3
import weighted_simplicial_complex as wsc
from utils import tuples
from numpy import array
import math
import os as os

import sys


import hash_edge, hash_point



class PointCloud:
    
#     def __dir__(self):
#         return ["num_points()", 
#                 "dimension()", 
#                 "plot2d()", 
#                 "plot3d()", 
#                 "plot2d_neighborhood_graph(epsilon)", 
#                 "plot3d_neighborhood_graph(epsilon)", 
#                 "film_neighborhood_graph(step, num_steps)", 
#                 "neighborhood_graph(epsilon, method)"]

    def __init__(self,points,space='affine'):

        '''
        Points should be a list of hashable objects.

        Variables   :
            _points : a array of hashable points.
            _space  : either 'affine' or 'projective'.
        '''
        try:
            self._points=list(points)
        except TypeError:
            raise TypeError('Input points should be of iterable points.')
        try:
            hash(self._points[0])
        except TypeError:
            print "Detected points are not HashPoint. Attempting to convert."
            points = [hash_point.HashPoint(
                    points[n], 
                    index=n) 
                    for n in range(len(points))] 
#             raise TypeError('Input points should be of hashable points.')
        if space != 'affine' and space != 'projective':
            raise TypeError('The argument "space" should be set to either "affine" or "projective".')

        self._points = points
        self._space = space
        self._fig = None



    def __str__(self):

        try:
            repr(self.dimension())
        except AttributeError:
            raise AttributeError('The numpy array must be a single set of points.')
        return 'Point cloud with ' + repr(self.num_points()) + \
            ' points in real ' + self._space + \
            ' space of dimension ' + repr(self.dimension())


    def __repr__(self):
        return self._points.__repr__()


    def num_points(self):
        return len(self._points)

    def __len__(self):
        return len(self._points)

    def __getitem__(self, key):
        return tuple(self._points[key]._coords)


    def dimension(self):

        if self._space=='affine':
            return len(self._points[0]._coords)
        elif self._space=='projective':
            return len(self._points[0]._coords)-1


    def plot2d(self, axes=(0,1), save = False, title = False):

        if self._space=='affine':

            if self._fig is None:
                fig=plt.figure()
            plt.clf()

            ax = fig.add_subplot(111)
            fig.set_size_inches(10.0,10.0)
            if title is not False:
                fig.suptitle(title)
            xcoords=[p._coords[axes[0]] for p in self._points]
            ycoords=[p._coords[axes[1]] for p in self._points]

            ax.scatter(xcoords,ycoords, marker = 'o', color = "#ff6666")

            ax.grid(True)
            ax.axis([1.1*min(xcoords),1.1*max(xcoords),1.1*min(ycoords),1.1*max(ycoords)])
            ax.set_aspect('equal')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_xlim(-3,3)
            ax.set_ylim(-3,3)
            plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

            self._display_plot(plt, "plot2d", save)
            plt.close()

            return True
        else:
            return None


    def _display_plot(self, plt, method, save):

        if save is False:
            plt.show()
        elif save is not False:

            def save_file(name): # overwrite protection

                if os.path.isfile(name+'.png') is False:
                    plt.savefig(name)
                else:
                    attempt = 2
                    while(os.path.isfile(name+'_'+str(attempt)+'.png')):
                        attempt = attempt + 1
                    plt.savefig(name+'_'+str(attempt))


            if type(save) is bool: # default
                save_file(method)
            elif type(save) is str: # if save gets a string
                save_file(save)
        return True


    def plot3d(self,axes=(0,1,2), save = False, title = False):

        if self._space=='affine':

            if self._fig is None: # faster to clear than to close and open
                fig = plt.figure()
            plt.clf()

            ax = fig.add_subplot(111)
            fig.set_size_inches(10.0,10.0)
            if title is not False:
                fig.suptitle(title)
            ax = plt3.Axes3D(fig)
            xcoords=[p._coords[axes[0]] for p in self._points]
            ycoords=[p._coords[axes[1]] for p in self._points]
            if len(self._points[0]) == 3:
                zcoords=[p._coords[axes[2]] for p in self._points]
            else:
                zcoords=[0 for _ in self._points]
            ax.scatter(xcoords, ycoords, zcoords, marker = '.', color = '#ff6666')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_xlim(-3,3)
            ax.set_ylim(-3,3)
            ax.set_zlim(-3,3)
            # Set camera viewpoint
            # Elevation of camera (default is 30)
            ax.elev=30
            # Azimuthal angle of camera (default is 30)
            ax.azim=30
            # Camera distance (default is 10)
            ax.dist=10
            fig.add_axes(ax)

            # whether to display plot or save it
            self._display_plot(plt, "plot3d", save)

            return True
        else:
            return None


    # Makes a 2-dimensional plot of a neighborhood graph, for a given epsilon
    def plot2d_neighborhood_graph(self,
            epsilon,
            axes=(0,1),
            shading_axis=2,
            method='subdivision', 
            save = False, 
            title = False):

        if self._space=='affine':
            g=self.neighborhood_graph(epsilon,method)
            edges=[]
            c=[]

            # For the two plotting directions
            minx=min(p._coords[axes[0]] for p in self._points)
            maxx=max(p._coords[axes[0]] for p in self._points)
            miny=min(p._coords[axes[1]] for p in self._points)
            maxy=max(p._coords[axes[1]] for p in self._points)

            # For the shading direction
            minz=min(p._coords[shading_axis] for p in self._points)
            maxz=max(p._coords[shading_axis] for p in self._points)

            for p in self._points:
                if p._coords[shading_axis]<=minz+(maxz-minz)/2:
                    pc=p._coords
                    for e in g._adj[p]:
                        qc=e[0]._coords
                        edges.append([[qc[axes[0]],qc[axes[1]]],[pc[axes[0]],pc[axes[1]]]])
                        c.append(((p._coords[shading_axis]-minz)/(maxz-minz),.5,.5,.5))
            for p in self._points:
                if p._coords[shading_axis]>=minz+(maxz-minz)/2:
                    pc=p._coords
                    for e in g._adj[p]:
                        qc=e[0]._coords
                        edges.append([[qc[axes[0]],qc[axes[1]]],[pc[axes[0]],pc[axes[1]]]])
                        c.append(((p._coords[shading_axis]-minz)/(maxz-minz),.5,.5,.5))
            lines=mpl.collections.LineCollection(edges,color=c)

            if self._fig is None: # faster to clear than to close and open
                fig = plt.figure()
            plt.clf()

            ax = fig.add_subplot(111)
            fig.set_size_inches(10.0,10.0)
            if title is not False:
                fig.suptitle(title)
            ax.grid(True)
            ax.axis([minx-.1*abs(maxx-minx),maxx+.1*abs(maxx-minx),miny-.1*abs(maxy-miny),maxy+.1*abs(maxy-miny)])
            ax.set_xlim(-3,3)
            ax.set_ylim(-3,3)
            ax.set_aspect('equal')
            ax.add_collection(lines)
#             xcoords=[p._coords[axes[0]] for p in self._points]
#             ycoords=[p._coords[axes[1]] for p in self._points]
#             ax.plot(xcoords,ycoords,',')

            self._display_plot(plt, "plot2d_ng", save)

            return True
        else:
            return None




    def plot3d_neighborhood_graph(self, 
            epsilon, 
            axes=(0,1,2), 
            cmap = 1,
            method='subdivision', 
            save = False, 
            title = False):

        """ 
        For a given epsilon, makes a 3-dimensional plot of a neighborhood 
        graph.
        Currently, there are the following cmap options which are selected
        by index:
            0 - Dark2
            1 - Accent
            2 - Paired
            3 - rainbow
        Also, the function can also take a different method, and 
        automatically save a plot with or without a title
        """

        if self._space=='affine':

            if self._fig is None:
                fig=plt.figure()
            if title is not False:
                fig.suptitle(title)

            ax = plt3.Axes3D(fig)


            g=self.neighborhood_graph(epsilon, method)
            adj = g._adj
            cp = g.connected_components()
            cmaps = [plt.cm.Dark2, plt.cm.Accent, plt.cm.Paired,
                    plt.cm.rainbow]
            cmap = cmaps[cmap] # color mappings 
            line_colors = cmap(np.linspace(0,1, len(cp)))

            componentIndex = 0
            totalEdges = 0
            for component in cp:
                edges = {}
                if len(component) > 1:
                    edgeIndex = 0
                    for vertex in component:
                        for endPoint in adj[vertex]:
                            if len(self._points[0]) >= 3:
                                edges[edgeIndex] = hash_edge.HashEdge(
                                        array([
                                            [vertex[axes[0]],
                                                vertex[axes[1]],
                                                vertex[axes[2]]],
                                            [endPoint[0][axes[0]],
                                                endPoint[0][axes[1]],
                                                endPoint[0][axes[2]]]]
                                            ), index = edgeIndex
                                        )
                            elif len(self._points[0]) == 2:
                                edges[edgeIndex] = hash_edge.HashEdge(
                                        array([
                                            [vertex[axes[0]],
                                                vertex[axes[1]], 
                                                0], 
                                            [endPoint[0][axes[0]],
                                                endPoint[0][axes[1]], 
                                                0]]
                                            ), index = edgeIndex
                                        )
                            edgeIndex += 1
                edges = edges.values()
                edges = set(edges)
                for _edge in edges:
                    totalEdges += 1

                if DEBUG:
                    print edges

                lines = a3.art3d.Poly3DCollection(edges)
                lines.set_edgecolor(line_colors[componentIndex])
                ax.add_collection(lines)
                componentIndex += 1
            
            if DEBUG:
                print totalEdges

            textstr = 'number of points $=%d$ \ndistance $=%f$\nedges $=%d$\nconnected components $=%d$' % (len(self._points), epsilon, g.num_edges(), len(cp))
            # place a text box in upper left in axes coords
            props = dict(boxstyle='round', facecolor='white', alpha=0.5)
            ax.text2D(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox = props)

            fig.set_size_inches(10.0,10.0)

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

            ax.set_xlim(-3,3)
            ax.set_ylim(-3,3)
            ax.set_zlim(-3,3)

            ax.grid(True)
            ax.set_aspect('equal')

            self._display_plot(plt, "plot3d_ng", save)

            plt.close()
            return True
        else:
            return None


    # Makes movie of 2-dimensional plots
    def film_neighborhood_graph(self,step,num_steps,fps=24,method='subdivision',file_name='movie.mp4'):

        '''
        WARNING: do not run this in a Dropbox folder.

        WARNING: this function rewrites movie.mp4 in the working directory by
        default. To change this, add file_name='your_file_name.mp4' to the
        function call.

        WARNING: this function is currently very slow for large data sets,
        thanks it seems to the slowness in plotting so many points.
        '''
        if self._space=='affine':
            epsilon=0
            h=self.neighborhood_graph(step*num_steps,method)
            os.system("rm _tmp*.png")
            fig,(ax)=plt.subplots(1,1)
            # Resolution of video
            # Example: (10,10) gives a 1000x1000 pixel resolution video
            fig.set_size_inches(10.0,10.0)
            for i in range(num_steps):
                epsilon=epsilon+step
                g=h.neighborhood_graph(epsilon)
                for p in self._points:
                    if p._coords[2]<=0:
                        for e in g._adj[p]:
                            ax.plot([e[0]._coords[0],p._coords[0]],
                                     [e[0]._coords[1],p._coords[1]],color=(.5*p._coords[2]+.5,.5,.5,.5))
                for p in self._points:
                    if p._coords[2]>0:
                        for e in g._adj[p]:
                            ax.plot([e[0]._coords[0],p._coords[0]],
                                     [e[0]._coords[1],p._coords[1]],color=(.5*p._coords[2]+.5,.5,.5,.5))

                ax.grid(True)
                ax.set_aspect('equal')
                plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
                # Graph bounds
                # Depends on point cloud used, values (-3,3) and (-3,3) work for torus
                ax.set_xlim(-3,3)
                ax.set_ylim(-3,3)
                fname = '_tmp%05d.png'%i
                plt.savefig(fname)
                plt.cla()
            plt.close(fig)
            os.system("rm "+file_name)
            # Movie maker command
            # Changed to "avconv" from "ffmpeg", change back if older system (options are the same)
            os.system("avconv -r "+str(fps)+" -i _tmp%05d.png "+file_name)
            os.system("rm _tmp*.png")
            return None
        else:
            return None


    def neighborhood_graph(self,
            epsilon,
            method = "subdivision"):
        """
        calls the recursive function _neighborhood_graph
        """
        return self._neighborhood_graph(
                epsilon,
                method,
                self._points,
                {v:set() for v in self._points})


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
        methodarray=method.split(' ')

        if methodarray[0]=='subdivision':

            if self._space=='projective':
                return self.neighborhood_graph(epsilon,method='exact')
            elif self._space=='affine':
                if len(methodarray)>1:
                    d=int(methodarray[1])
                    m=''
                    for i in range(len(methodarray)-2):
                        m=m+methodarray[i+2]
                        m=m+' '

                    if m=='':
                        self._subdivide_neighbors(epsilon, 
                                dictionary, 
                                pointarray, 
                                depth=d)
                        return wsc.wGraph(dictionary, epsilon)
                    else:
                        self._subdivide_neighbors(epsilon, 
                                dictionary, 
                                pointarray, 
                                coordinate = m, 
                                depth=d)
                        return wsc.wGraph(dictionary, epsilon)
                else: #  most calls end up here
                      #  also starts the recursion
                    self._subdivide_neighbors(epsilon, dictionary, pointarray)
                    # mystery dictionary assignments..?
                    return wsc.wGraph(dictionary, epsilon)

        elif methodarray[0] == 'exact':
            '''
            Issue: this doesn't work because lists and numpy arrays are not hashable.
            '''
            for i in range(len(self._points)):
                for j in range(i+1,len(self._points)):
                    if self._space=='affine':
#                         dist=np.sqrt(sum((self._points[i]._coords-self._points[j]._coords) *(self._points[i]._coords-self._points[j]._coords)))
                        dist=np.sqrt(sum((self._points[i]._coords-self._points[j]._coords)**2))
                        if dist<epsilon:
                            dictionary[self._points[i]].add((self._points[j],dist))
                            dictionary[self._points[j]].add((self._points[i],dist))
                    elif self._space=='projective':
                        return None
            return wsc.wGraph(dictionary, epsilon)

        elif methodarray[0] == 'nonrecursive_subdivision':
            if self._space == 'affine':
                self._nonrecursive_subdivision(epsilon, dictionary, pointarray)
                return wsc.wGraph(dictionary,epsilon)
            return None
        elif methodarray[0]=='approximate':
            return None
        elif methodarray[0]=='randomized':
            return None
        elif methodarray[0]=='landmarking':
            return None

        else:
            raise TypeError('Method should be one of subdivision, exact, approximate, randomized, or landmarking.')

    def _nonrecursive_subdivision(self, e, dictionary, pointarray):
        raise NotImplementedError 


    def _selectpoint(self,pointarray, k, n):

        #gives the kth smallest point of "self._points", according to the nth coordinate
        #we use this to give the median, but a general solution for k is needed for the recursive algorithm
        #this algorithm is O(n) for best and worst cases


        a = pointarray[:]
        c = []
        while(len(a)>5):
            for x in range(int(math.floor(len(a)/5))):
                b=pointarray[5*x:5*x+5]
                b.sort(key = lambda x: x._coords[n])
                c.append(b[int(math.floor(len(b)/2))])
            a = c
            c = []
        pivot = a[int(math.floor(len(a)/2))]

        lesser = [point for point in pointarray if point._coords[n] < pivot._coords[n]]
        if len(lesser) > k:
            return self._selectpoint(lesser, k, n) # recursive
        k -= len(lesser)

        equal = [point for point in pointarray if point._coords[n] == pivot._coords[n]]
        if len(equal) > k:
            return pivot # basecase
        k -= len(equal)

        greater = [point for point in pointarray if point._coords[n] > pivot._coords[n]]
        return self._selectpoint(greater, k, n) # recursive


    def _subdivide_neighbors(self, e, dictionary, pointarray, coordinate=0, method='exact', depth=-1):
        #  method and depth are accumulators for the recursive calls
        #  divides the space into two regions about the median point relative to "coordinate"
        #  glues the two regions, then recursively calls itself on the two regions.
        if len(pointarray)>1:
            median = self._selectpoint(pointarray, len(pointarray)/2, coordinate)

            
            smaller     = []
            bigger      = []
            gluesmaller = []
            gluebigger  = []

            #split into two regions
            for i in range(len(pointarray)):
                if pointarray[i]._coords[coordinate] <  median._coords[coordinate]:
                    smaller.append(pointarray[i])
                    if pointarray[i]._coords[coordinate] > median._coords[coordinate]-e:
                        gluesmaller.append(pointarray[i])

                if pointarray[i]._coords[coordinate] >= median._coords[coordinate]:
                    bigger.append(pointarray[i])
                    if pointarray[i]._coords[coordinate] < median._coords[coordinate]+e:
                        gluebigger.append(pointarray[i])

            #glue together the two regions
            for i in range(len(gluesmaller)):
                for j in range(len(gluebigger)):
                    dist = np.sqrt(sum(((gluesmaller[i])._coords-gluebigger[j]._coords)*(gluesmaller[i]._coords-gluebigger[j]._coords)))
                    if dist<e:
                        
                        dictionary[gluesmaller[i]].add((gluebigger[j],dist))
                        dictionary[gluebigger[j]].add((gluesmaller[i],dist))



    # def _subdivide_neighbors(self, e, dictionary, pointarray, coordinate=0, method='exact', depth=-1):
            #recursively compute for the two regions, now using a different reference coordinate, to reduce gluing area
            if depth == -1: #depth -1 means fully recursive. all edges are formed by "gluing"
                coordinate = (coordinate+1)%self.dimension()
                self._subdivide_neighbors(e, dictionary, smaller, coordinate, method, depth=-1) 
                self._subdivide_neighbors(e, dictionary, bigger, coordinate, method, depth=-1)
            if depth > 0:
                coordinate = (coordinate+1)%self.dimension()
                self._subdivide_neighbors(e, depth-1, coordinate, smaller)
                self._subdivide_neighbors(e, depth-1, coordinate, bigger)
    # def _selectpoint(self, pointarray, k, n):
            if depth == 0:
                self._neighborhood_graph(e,method,smaller,dictionary) 
                self._neighborhood_graph(e,method,bigger,dictionary)

