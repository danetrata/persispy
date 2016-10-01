========
Usage
========

To get started, first we need a :class:`~persispy.point_cloud.PointCloud`.::

    >>> import persispy
    >>> import persispy.point_cloud as ppc

    >>> triangle = [(0,0),(0,1),(1,0)]
    >>> print(triangle)
    >>> tri_pc = ppc.PointCloud(triangle)
    >>> print(tri_pc)
    >>> print(tri_pc.get_points())

    [(0, 0), (0, 1), (1, 0)]
    Point cloud with 3 points in real affine space of dimension 2

From here we can construct our weighted neighborhood graph, the :class:`~persispy.weighted_simplicial_complex.wGraph`.::

    >>> tri_ng = tri_pc.neighborhood_graph(epsilon=1.5, method="subdivision")
    >>> print(tri_ng)
    >>> print(tri_ng.adjacencies(pretty=True))

    [point 0: [0, 0], point 1: [0, 1], point 2: [1, 0]]
    Weighted graph with 3 points and 3.0 edges
    {point 0: [0, 0]: {(point 2: [1, 0], 1.0), (point 1: [0, 1], 1.0)},
     point 1: [0, 1]: {(point 0: [0, 0], 1.0),
                       (point 2: [1, 0], 1.4142135623730951)},
     point 2: [1, 0]: {(point 0: [0, 0], 1.0),
                       (point 1: [0, 1], 1.4142135623730951)}}
                       
                       
If we know a process to generate points, we can then pass the list to :class:`~persispy.point_cloud.PointCloud`.::
    
    >>> from random import uniform
    >>> from math import sin, cos

    >>> circle = [ (cos(x), sin(x)) for x in [uniform(0, 2*float(22)/7) for _ in range(50)]]
    >>> circle_pc = ppc.PointCloud(circle)
    >>> circle_ng = circle_pc.neighborhood_graph(.5)
    >>> print(circle_pc)
    >>> print(circle_ng)

    Point cloud with 50 points in real affine space of dimension 2
    Weighted graph with 50 points and 185 edges
    

To visualize what our points look like, we can call the :mod:`persispy.plot` module, which has the :func:`~persispy.plot.plot2d` and :func:`~persispy.plot.plot3d` functions.::

    >>> from persispy import plot
    >>> plot.plot2d(circle_pc)
    >>> plot.plot2d(circle_ng, shading_style='component')
    
.. figure:: images/circle_point_cloud.png
   :align: center
.. figure:: images/circle_neighborhood_graph.png
   :align: center
