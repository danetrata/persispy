
""" 
input: pointCloud OR
    wGraph
"""

import matplotlib.pyplot as plt
import numpy as np
import time

def plot():
    """
    http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
    speed up matplotlib.
    have a return value that is usuable in the gui
    """
    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))
    plt.show(block = False)

    line.set_ydata(np.random.randn(100))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.cavnas.update()
    fig.canvas.flush_events()

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




def plot2d(pointCloud, axes=(0,1), save = False, title = False):

    pass


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



def _display_plot(self, plt, method, save, DEBUG = True):
    """
    We display a plot.
    Additionally, we can instead save a plot automatically.
    """

    if save is False:
        plt.show()
    elif save is not False:

        def save_file(name): 
            """
            Saves the current plot. Has overwrite safeguards.
            """

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


def plot2d_neighborhood_graph(self,
        epsilon,
        axes=(0,1),
        shading_axis=2,
        method='subdivision', 
        save = False, 
        title = False):
    """
    Plots the 2d neighborhood graph
    """

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

def plot3d(self, axes=(0,1,2), save = False, title = False):
    

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






def plot3d_neighborhood_graph(self, 
        epsilon, 
        axes=(0,1,2), 
        cmap = 0,
        method='subdivision', 
        save = False, 
        title = False,
        DEBUG = False):

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

        if self._fig is None: # faster to clear than to close and open
            fig = plt.figure()

        plt.clf()
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
            for _ in edges:
                totalEdges += 1

            if DEBUG:
                print edges

            lines = a3.art3d.Poly3DCollection(edges)
            lines.set_edgecolor(line_colors[componentIndex])
            ax.add_collection(lines)
            componentIndex += 1
        
        if DEBUG: print totalEdges

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

        if self.gui:
            return fig
        print self._fig
        self._display_plot(plt, "plot3d_ng", save)

        print self._fig
        plt.close()

        return True
    else:
        return None


if __name__ == "__main__": 
    from points import plane

    pc = points.plane(200)

    pc.plot2d()
    pc.plot3d()

    ng = pc.neighborhood_graph(.13)
    ng.plot2d()
    ng.plot3d()
