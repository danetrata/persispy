
""" 
input: pointCloud OR
    wGraph
"""

import numpy as np
import time

"""
http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
speed up matplotlib.
have a return value that is usuable in the gui
>>>    fig, ax = plt.subplots()
>>>    line, = ax.plot(np.random.randn(100))
>>>    plt.show(block = False)
>>>    line.set_ydata(np.random.randn(100))
>>>    ax.draw_artist(ax.patch)
>>>    ax.draw_artist(line)
>>>    fig.cavnas.update()
>>>    fig.canvas.flush_events()
"""
import matplotlib
matplotlib.use('GTKAgg') 
 
def show(fig):
    """
    Due to avoiding pyplot, we must handle all the backend calls...
    """
    master = tk.Tk()
    canvas = FigureCanvasTkAgg(fig, master = master)
    NavigationToolbar2TkAgg(canvas, master)
    canvas.get_tk_widget().pack()
    canvas.draw()
    master.mainloop()

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import Tkinter as tk

from point_cloud import PointCloud
from weighted_simplicial_complex import wGraph

import matplotlib.pyplot as plt

def plot2d(*args, **kwargs):
    for object in args:
        if isinstance(object, PointCloud):
            fig = plot2d_pc(*args, **kwargs)
            return fig
        if isinstance(object, wGraph):
            return plot2d_ng(*args, **kwargs)

# def plot3d(graph, gui = False):
#     if isinstance(graph, PointCloud):
#         return plot3d_pc(graph, gui)
#     if isinstance(graph, wGraph):
#         return plot3d_ng(graph, gui, kwargs)


def plot3d(*args, **kwargs):
    for object in args:
        if isinstance(object, PointCloud):
            return plot3d_pc(*args, **kwargs)
        if isinstance(object, wGraph):
            return plot3d_ng(*args, **kwargs)

def plot2d_pc(pointCloud, gui = False):
    """
    """
#     fig = Figure()

    fig, ax = plt.subplots()

    fig.set_size_inches(10.0,10.0)

    xcoords = [p._coords[0] for p in pointCloud._points]
    ycoords = [p._coords[1] for p in pointCloud._points]

    ax.scatter(xcoords,ycoords, marker = 'o', color = "#ff6666")

    ax.grid(True)
    ax.axis([1.1*min(xcoords),1.1*max(xcoords),1.1*min(ycoords),1.1*max(ycoords)])
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
#     ax.set_xlim(-3,3)
#     ax.set_ylim(-3,3)
# what do?
#     plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

    if gui:
        return fig
    else:
        show(fig)

import matplotlib as mpl
def plot2d_ng(wGraph,
        axes=(0,1),
        shading_axis=1,
        method='subdivision', 
        save = False, 
        title = False,
        gui = False):
    """
    Plots the 2d neighborhood graph
    """

    
    def pick_ax(coords):
        x, y = coords[axes[0]], coords[axes[1]]
        return x, y

    edges = []
    colors = []

    # For the two plotting directions
    minx=min(p[0] for p in wGraph._adj.keys())
    maxx=max(p[0] for p in wGraph._adj.keys())
    miny=min(p[1] for p in wGraph._adj.keys())
    maxy=max(p[1] for p in wGraph._adj.keys())

    cp = wGraph.connected_edges()

    # For the shading direction

    minz=min(p[shading_axis] for p in wGraph._adj.keys())
    maxz=max(p[shading_axis] for p in wGraph._adj.keys())

    for p in wGraph._adj:
        if p._coords[shading_axis]<=minz+(maxz-minz)/2:
            px, py = pick_ax(p._coords)
            for e in wGraph._adj[p]:
                qx, qy = pick_ax(e[0]._coords)
                edges.append([
                        [qx, qy],
                        [px, py]])

                colors.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                    .5,
                    .5,
                    .5))

    for p in wGraph._adj:
        if p._coords[shading_axis]>=minz+(maxz-minz)/2:
            px, py = pick_ax(p._coords)
            for e in wGraph._adj[p]:
                qx, qy = pick_ax(e[0]._coords)
                edges.append([
                        [qx, qy],
                        [px, py]])

                colors.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                    .5,
                    .5,
                    .5))

    lines=mpl.collections.LineCollection(edges, color=colors)

    fig = Figure()
    ax = fig.add_subplot(111)
    fig.set_size_inches(10.0,10.0)
    if title is not False:
        fig.suptitle(title)
    ax.grid(True)
    ax.axis([minx-.1*abs(maxx-minx),maxx+.1*abs(maxx-minx),miny-.1*abs(maxy-miny),maxy+.1*abs(maxy-miny)])

    ax.set_aspect('equal')
    ax.add_collection(lines)

    x, y = pick_ax(zip(*wGraph.vertices()))
    ax.scatter(x, y, marker = 'o', color = '#ff6666')

    if gui:
        return fig
    else:
        show(fig)

def plot3d_pc(self, axes=(0,1,2), save = False, title = False):
    if self._space=='affine':
        if self._fig is None: # faster to clear than to close and open
            fig = plt.figure()
        plt.clf() # clears the figure

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

        ax.grid(True)
        ax.set_aspect('equal')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

#         # Set camera viewpoint
#         # Elevation of camera (default is 30)
#         ax.elev=20
#         # Azimuthal angle of camera (default is 30)
#         ax.azim=30
#         # Camera distance (default is 10)
#         ax.dist=10
#         fig.add_axes(ax)
#         ax.set_aspect('equal')


        # whether to display plot or save it
        self._display_plot(plt, "plot3d", save)

        return True
    else:
        return None

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
from mpl_toolkits.mplot3d import Axes3D

def plot3d_ng(wGraph, 
        cmap = 0,
        method='subdivision', 
        save = False, 
        title = False,
        DEBUG = False,
        gui = False):

    """ 
    For a given epsilon, makes a 3-dimensional plot of a neighborhood 
    graph.
    Currently, there are the following cmap options which are selected
    by index:
        0 - Dark2
        1 - Accent
        2 - Paired
        3 - rainbow
        4 - winter
    Also, the function can also take a different method, and 
    automatically save a plot with or without a title
    """



    fig = plt.figure()


#     canvas = FigureCanvasTkAgg(fig)
#     fig.set_canvas(plt.gcf().canvas)


    ax = Axes3D(fig)

    epsilon = wGraph._epsilon
    adj = wGraph._adj
    cp = wGraph.connected_components()
    cmaps = [plt.cm.Dark2, plt.cm.Accent, plt.cm.Paired,
            plt.cm.rainbow, plt.cm.winter]
    cmap = cmaps[cmap] # color mappings 
    line_colors = cmap(np.linspace(0,1, len(cp)))
    

    cp = wGraph.connected_edges(padding = 3)
    cp.sort(key = len)

    numberEdges = wGraph.num_edges()

    for componentIndex, component in enumerate(cp):
        scalar = float(len(component)) / numberEdges + 1

        tempcomponent = []
        for i, edge in enumerate(component):
            tempcomponent.append(edge*scalar)
        component = set(tempcomponent)

            


        if DEBUG:
            print edges

        lines = a3.art3d.Poly3DCollection(component)

        if componentIndex % 2 == 1:

            componentIndex = -1*componentIndex
        lines.set_edgecolor(line_colors[componentIndex])
        ax.add_collection(lines)
    
    if DEBUG: print totalEdges
    
    if wGraph.singletons():
        x, y, z = zip(*wGraph.singletons(padding = 3))
        ax.scatter(x, y, z, marker = '.', s = 15, color = '#ff6666')


    textstr = 'number of points $=%d$ \ndistance $=%f$\nedges $=%d$\nconnected components $=%d$' % (len(wGraph._adj), epsilon, wGraph.num_edges(), len(cp))
    
    
    # place a text box in upper left in axes coords
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text2D(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox = props)



    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


#     # Set camera viewpoint
#     # Elevation of camera (default is 30)
#     ax.elev=30
#     # Azimuthal angle of camera (default is 30)
#     ax.azim=20
#     # Camera distance (default is 10)
#     ax.dist=10

    ax.grid(True)
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(-3,3)
    ax.set_aspect('equal')
#     ax.autoscale_view(True, True, True)


    if gui:
        return fig
    else:
        plt.show()



if __name__ == "__main__": 
    from points import plane

    pc = plane(150, seed = 1991)
#     plot2d(pc)
    ng = pc.neighborhood_graph(0.2)
    plot3d(ng)

#     ng = pc.neighborhood_graph(.13)
#     ng.plot2d()
#     ng.plot3d()
