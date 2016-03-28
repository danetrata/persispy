"""
input: pointCloud OR
    wGraph
"""

import numpy as np
import time

import matplotlib
# TODO: Marginpar does this actually do anything? In py.test-ing I found out that it
# seems to not.--Ben
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg\
        import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk

def create_fig():
    def destroy():
        root.destroy()
        root.quit()
        plt.close('all')
    def onsize(event):
        root.winfo_width(), root.winfo_height()
# only time to call pyplot
    fig = plt.figure()
#     fig.set_size_inches(8, 8)
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", destroy)
    root.bind("<Configure>", onsize)
    frame = tk.Frame(root)
    frame.pack(side='top', fill='both', expand=1 )
    canvas = FigureCanvasTkAgg(fig, master = frame)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1 )
#     canvas.get_tk_widget().pack()
    canvas._tkcanvas.pack(side='top', fill='both', expand=1)
    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    toolbar.pack()
    return fig, root


def get_canvas(root):
    children = root.winfo_children()
    for child in children:
        if child.winfo_children():
            children.extend(child.winfo_children())


    for child in children:
        if isinstance(child, NavigationToolbar2TkAgg):
            return child

    assert False, "No Canvas in root" 

def show(root):
    canvas = get_canvas(root)
#     canvas.update()
#     canvas.flush_events()
    canvas.draw()
    root.mainloop()

from matplotlib.figure import Figure
from persispy.point_cloud import PointCloud
from persispy.weighted_simplicial_complex import wGraph


def plot2d(*args, **kwargs):
    for object in args:
        if isinstance(object, PointCloud) or isinstance(object, Intersect):
            fig = plot2d_pc(*args, **kwargs)
            return fig
        if isinstance(object, wGraph):
            return plot2d_ng(*args, **kwargs)


def plot3d(*args, **kwargs):
    for object in args:
        if isinstance(object, PointCloud) or isinstance(object, Intersect):
            return plot3d_pc(*args, **kwargs)
        if isinstance(object, wGraph):
            return plot3d_ng(*args, **kwargs)

import matplotlib.pyplot as plt

def plot2d_pc(pointCloud, gui = False):
    """
    """


    xcoords = [p._coords[0] for p in pointCloud._points]
    ycoords = [p._coords[1] for p in pointCloud._points]


    fig, ax = plt.subplots(1)
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
        plt.show(fig)

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

    x, y, pointColors = [], [], []
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
            x.append(px)
            y.append(py)
            pointColors.append(((p._coords[shading_axis]-minz)/(maxz-minz),
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

            x.append(px)
            y.append(py)
            pointColors.append(((p._coords[shading_axis]-minz)/(maxz-minz),
                .5,
                .5,
                .5))
    assert x

    lines=mpl.collections.LineCollection(edges, color=colors)


    fig, ax = plt.subplots(1)
#     fig = Figure()
#     ax = fig.add_subplot(111)
    ax.add_collection(lines)
    fig.set_size_inches(10.0,10.0)
    if title:
        fig.suptitle(title)
    ax.grid(True)
    ax.axis([minx-.1*abs(maxx-minx),maxx+.1*abs(maxx-minx),miny-.1*abs(maxy-miny),maxy+.1*abs(maxy-miny)])

    ax.set_aspect('equal')

#     x, y = pick_ax(zip(*wGraph.vertices()))
    ax.scatter(x, y, marker = 'o', color = pointColors, zorder = len(x))

    if gui:
        return fig
    else:
        plt.show(fig)

def plot3d_pc(pointCloud, axes=(0,1,2), gui = False, title = False):
    if pointCloud._space=='affine':

        xcoords=[p._coords[axes[0]] for p in pointCloud._points]
        ycoords=[p._coords[axes[1]] for p in pointCloud._points]
        if len(pointCloud._points[0]) == 3:
            zcoords=[p._coords[axes[2]] for p in pointCloud._points]
        else:
            zcoords=[0 for _ in pointCloud._points]




        fig = plt.figure()
        ax = Axes3D(fig)

        ax.scatter(xcoords, ycoords, zcoords, marker = '.', color = '#ff6666')

        fig.set_size_inches(10.0,10.0)
        if title:
            fig.suptitle(title)

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



        if gui:
            return fig
        else:
            plt.show(fig)
#             show(fig)

import mpl_toolkits.mplot3d as a3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

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

    plt.rc('text', usetex=True)
    plt.rc('font', family = 'sans-serif: Computer Modern Sans serif')
    plt.axis('off')



#     fig = plt.figure()
    fig, window = create_fig()
    window.wm_title("3D Neighborhood Graph")
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

#         scalar = float(len(component)) / numberEdges + 1
#         tempcomponent = []
#         for i, edge in enumerate(component):
#             tempcomponent.append(edge*scalar)
#         component = set(tempcomponent)

            


        if DEBUG:
            print (edges)

        lines = a3.art3d.Poly3DCollection(component)

        if componentIndex % 2 == 1:

            componentIndex = -1*componentIndex
        lines.set_edgecolor(line_colors[componentIndex])
        ax.add_collection(lines)
    
    if DEBUG: print (totalEdges)
    
    if wGraph.singletons():
        x, y, z = zip(*wGraph.singletons(padding = 3))
        ax.scatter(x, y, z, 
                marker = '.', 
                s = 15, 
                color = '#ff6666', 
                label = r"\makebox[90pt]{%d\hfill}Singletons" % len(x))


    textstr = r'\noindent\makebox[90pt]{%d\hfill}Number of Points\\ \\'\
            r'\makebox[90pt]{%f\hfill}Distance\\ \\'\
            r'\makebox[90pt]{%d\hfill}Edges\\ \\'\
            r'\makebox[90pt]{%d\hfill}Connected Components' \
    % (len(wGraph._adj), epsilon, wGraph.num_edges(), len(cp))


    
    # place a text box in upper left in axes coords
#     props = dict(boxstyle='round', facecolor='white', alpha=0.5)
#     ax.text2D(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
#             verticalalignment='top', bbox = props)

# proxy artist to show properties
    properties = ax.plot([0], [0], color = 'white', label = textstr)
    ax.legend(loc='lower left', fontsize= 'x-large', borderpad = 1)

# 
#     ax.set_xlabel('x')
#     ax.set_ylabel('y')
#     ax.set_zlabel('z')


#     # Set camera viewpoint
#     # Elevation of camera (default is 30)
#     ax.elev=30
#     # Azimuthal angle of camera (default is 30)
#     ax.azim=20
#     # Camera distance (default is 10)
#     ax.dist=10

#     ax.grid(True)
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(-3,3)
    ax.set_aspect('equal')
#     ax.autoscale_view(True, True, True)


    if gui:
        return fig
    else:
#         plt.show()
        show(window)


from persispy.phc import Intersect
from persispy.points import plane, sphere



if __name__ == "__main__": 



    pc = sphere(1000)
    plot2d(pc)
    plot3d(pc)
    ng = pc.neighborhood_graph(0.2)
    plot2d(ng)
    plot3d(ng)



    pc = Intersect('x^2 + y^2 + z^2 -1', 1000)
    plot2d(pc)
    plot3d(pc)
    ng = pc.neighborhood_graph(0.2)
    plot2d(ng)
    plot3d(ng)



#     ng = pc.neighborhood_graph(.13)
#     ng.plot2d()
#     ng.plot3d()
