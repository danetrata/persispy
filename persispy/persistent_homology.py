'''
File: persistent_homology.py

Persistent Homology algorithm implementation

AUTHORS:

    - Mason Boeman (2016-04)
'''
import colorsys
import matplotlib.pyplot as plt
import sortedcontainers



class PersistentHomology(object):
    '''
    A Container for persistent homology information

    Vars: _coords (a numpy array).

    EXAMPLES:
    >>> HashPoint([1,2,3])
    point 0: [1, 2, 3]
    '''
    def __init__(self, simplicial_complex, n):
        self.vertex_dict = dict() #look up simplex container from tuple of vertices
        weighted_simplices = []
        for dimension in simplicial_complex._simplices:
            if dimension <= n+1:
                weighted_simplices.extend(simplicial_complex._simplices[dimension])
        self.simplex_containers = sorted([SimplexContainer(s) for s in sorted(weighted_simplices)])
        self.persistence_pairs = dict()
        for i, container in enumerate(self.simplex_containers):
            self.vertex_dict[tuple(container.simplex._vertices)] = container
            container.index = i
            container.compute_entries(self)
        for container in self.simplex_containers:
            #print [v._index for v in s.simplex._vertices]
            if len(container.simplex._vertices) != 1:
                rowiszero = False
                while container.entries[-1] in self.persistence_pairs:
                    container.entries = container.entries ^ (self.persistence_pairs[container.entries[-1]].entries)
                    #container.entries = container.entries ^ (self.persistence_pairs[container.entries[0]].entries)
                    #print 'xor'
                    if len(container.entries) == 0:
                        rowiszero = True
                        break
                    #print [x.index for x in s.entries]
                if not rowiszero:
                    self.persistence_pairs[container.entries[-1]] = container
    def get_differential(self):
        result = [[0 for i in range(len(self.simplex_containers))] for j in range(len(self.simplex_containers))]
        for container1 in self.simplex_containers:
            for container2 in container1.entries:
                result[container2.index][container1.index]=1
        return result
    def plot_bar_code(self, epsilon, hue=0, saturation=.5, lightness=.5):
        '''
        EXAMPLES:
        >>> persistent_homology.plot_bar_code(epsilon)

        >>> persistent_homology.plot_bar_code(epsilon, hue=.1, saturation=.4, lightness=.4)
        '''
        current_height = 1
        current_dimension = 1
        more_elements = True
        #WeightOrderedSimplices=sorted(self.Simplices,key=lambda sim: -sim.simplex._weight)
        while more_elements:
            more_elements = False
            for container in self.simplex_containers:
                if container in self.persistence_pairs:
                    if len(container.simplex._vertices) > current_dimension:
                        more_elements = True
                    if len(container.simplex._vertices) == current_dimension:
                        if container.simplex._weight != self.persistence_pairs[container].simplex._weight:
                            y_coordinate = current_height
                            alpha = 1-(self.persistence_pairs[container].simplex._weight-container.simplex._weight)/epsilon
                            rgb_values = colorsys.hls_to_rgb(
                                (hue+len(container.simplex._vertices)*(3-5**.5)*.5)%1.0,
                                saturation,
                                lightness)
                            current_height = current_height+1
                            plt.plot(
                                [container.simplex._weight, self.persistence_pairs[container].simplex._weight],
                                [y_coordinate, y_coordinate],
                                color=(rgb_values[0], rgb_values[1], rgb_values[2], 1-alpha),
                                linestyle='-', linewidth=1)
                else:
                    if len(container.entries)==0:
                        if len(container.simplex._vertices) > current_dimension:
                            more_elements = True
                        if len(container.simplex._vertices) == current_dimension:
                            if container.simplex._weight != epsilon:
                                y_coordinate = current_height
                                alpha = 1-(epsilon-container.simplex._weight)/epsilon
                                rgb_values = colorsys.hls_to_rgb(
                                    (hue+len(container.simplex._vertices)*(3-5**.5)*.5)%1.0,
                                    saturation,
                                    lightness)
                                current_height = current_height+1
                                plt.plot(
                                    [container.simplex._weight, epsilon],
                                    [y_coordinate, y_coordinate],
                                    color=(rgb_values[0], rgb_values[1], rgb_values[2], 1-alpha),
                                    linestyle='-', linewidth=1)
            current_dimension = current_dimension+1
            current_height = current_height+30

        plt.axis([0, epsilon, 0, current_height])
        plt.show()

class SimplexContainer(object):
    '''
    A Container for weighted simplices which maintains persistent homology information


    Vars:
        simplex (the corresponding weighted simplex object)
        entries (a list of the nonzero entries in the persistent homology matrix.
                 corresponds with a '1' in this Z/2Z implementation)
        index (an identifying number. used for human readable output)

    EXAMPLES:
    >>> HashPoint([1,2,3])
    point 0: [1, 2, 3]
    '''
    def __init__(self, sim):
        self.simplex = sim
        self.entries = sortedcontainers.SortedSet()
        self.index = -1
    def compute_entries(self, parent):
        '''
        Compute the initial values of the entries set.
        for a simplex with vertices (1,4,6,16), the entries will be the simplex containers whose vertices are:
        (1,4,6),(1,4,16),(1,6,16),(4,6,16), which are the faces of the 3-simplex.
        '''
        if len(self.simplex._vertices) < 2:
            return
        for index in range(len(self.simplex._vertices)):
            # Make more pythonic!
            self.entries.add(parent.vertex_dict[tuple(self.simplex._vertices[:index]+self.simplex._vertices[index+1:])])

    def __hash__(self):
        return hash(tuple(self.simplex._vertices))

    def __lt__(self, other):
        return self.simplex < other.simplex

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return self.simplex <= other.simplex

    def __ge__(self, other):
        return other <= self

    def __eq__(self, other):
        return self.simplex == other.simplex

    def __ne__(self, other):
        return not self == other

    def __cmp__(self, other):
        return self.simplex.__cmp__(other.simplex)

