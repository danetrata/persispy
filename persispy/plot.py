
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

def sanitize_points(points):
    """
    makes sure all types of points can be plotted
    returns them into seperated axises
    """
    pass

def sanitize_edge(edges):
    """
    makes sure all types of points can be plotted
    returns them into seperated axises
    """
    pass

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

def plot2d(graph, gui = False):
    if isinstance(graph, PointCloud):
        plot2d_pc(graph, gui)
    if isinstance(graph, wGraph):
        plot2d_ng(graph, gui)

def plot3d(graph, gui = False):
    if isinstance(graph, PointCloud):
        plot3d_pc(graph, gui)
    if isinstance(graph, wGraph):
        plot3d_ng(graph, gui)

def plot2d_pc(pointCloud, gui = False):
    """
    avoiding pyplot to be able to display nicely in a GUI
    """
    fig = Figure()

    ax = fig.add_subplot(111)
    fig.set_size_inches(10.0,10.0)

    xcoords = [p._coords[0] for p in pointCloud._points]
    ycoords = [p._coords[1] for p in pointCloud._points]

    ax.scatter(xcoords,ycoords, marker = 'o', color = "#ff6666")

    ax.grid(True)
    ax.axis([1.1*min(xcoords),1.1*max(xcoords),1.1*min(ycoords),1.1*max(ycoords)])
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
# what do?
#     plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

    if gui:
        return fig
    else:
        show(fig)







def plot2d_ng(wGraph,
        axes=(0,1),
        shading_axis=2,
        method='subdivision', 
        save = False, 
        title = False,
        gui = False):
    """
    Plots the 2d neighborhood graph
    """

    fig = Figure()

    edges = []
    color = []

    # For the two plotting directions
    minx=min(p[0] for p in wGraph._adj.keys())
    maxx=max(p[0] for p in wGraph._adj.keys())
    miny=min(p[1] for p in wGraph._adj.keys())
    maxy=max(p[1] for p in wGraph._adj.keys())

    cp = wGraph.connected_edges()

    # For the shading direction
    if len(wGraph._adj.keys()[0]) >= 3:
        minz=min(p[shading_axis] for p in wGraph._adj.keys())
        maxz=max(p[shading_axis] for p in wGraph._adj.keys())

        for p in wGraph._adj:
            if p._coords[shading_axis]<=minz+(maxz-minz)/2:
                pc=p._coords
                for e in wGraph._adj[p]:
                    qc=e[0]._coords
                    edges.append([
                            [qc[axes[0]],
                                qc[axes[1]]],
                            [pc[axes[0]],
                                pc[axes[1]]]
                            ])

                    color.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                        .5,
                        .5,
                        .5))

        for p in wGraph._adj:
            if p._coords[shading_axis]>=minz+(maxz-minz)/2:
                pc=p._coords
                for e in wGraph._adj[p]:
                    qc=e[0]._coords
                    edges.append([
                            [qc[axes[0]],
                                qc[axes[1]]],
                            [pc[axes[0]],
                                pc[axes[1]]]
                            ])

                    color.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                        .5,
                        .5,
                        .5))

    elif len(wGraph._adj.keys()[0]) == 2:
        minz = 0
        maxz = 0

        for p in wGraph._adj:
            pc=p._coords
            for e in wGraph._adj[p]:
                qc=e[0]._coords
                edges.append([
                        [qc[axes[0]],
                            qc[axes[1]]],
                        [pc[axes[0]],
                            pc[axes[1]]]
                        ])

                color.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                    .5,
                    .5,
                    .5))

    lines=mpl.collections.LineCollection(edges, color=c)

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
    Also, the function can also take a different method, and 
    automatically save a plot with or without a title
    """


    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig)
    fig.set_canvas(plt.gcf().canvas)
    ax = Axes3D(fig)

    epsilon = wGraph.epsilon
    adj = wGraph._adj
    cp = wGraph.connected_components()
    cmaps = [plt.cm.Dark2, plt.cm.Accent, plt.cm.Paired,
            plt.cm.rainbow]
    cmap = cmaps[cmap] # color mappings 
    line_colors = cmap(np.linspace(0,1, len(cp)))

    componentIndex = 0
    totalEdges = 0
    cp = wGraph.connected_edges(size = 3)

    

    for components in cp:
        for _ in components:
            totalEdges += 1

        if DEBUG:
            print edges

        lines = a3.art3d.Poly3DCollection(components)
        lines.set_edgecolor(line_colors[componentIndex])
        ax.add_collection(lines)
        componentIndex += 1
    
    if DEBUG: print totalEdges

    textstr = 'number of points $=%d$ \ndistance $=%f$\nedges $=%d$\nconnected components $=%d$' % (len(wGraph._adj), epsilon, wGraph.num_edges(), len(cp))
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
