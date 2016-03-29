'''
File: hashing.py

Hashable data points wrapping numpy arrays.

AUTHORS:

    - Daniel Etrata (2016-01)
    - Benjamin Antieau (2015-04)
'''


import hashlib as hashlib
import numpy as np

class HashPoint:
    '''
    A wrapped numpy array to allow hashing.

    Vars: _coords (a numpy array).

    EXAMPLES:
    >>> HashPoint([1,2,3])
    point 0: [1, 2, 3]
    '''
    def __init__(self, coords, index=0):
        self._coords = np.array(coords)
        self._index = index

    def __len__(self):
        return len(self._coords)

    def __getitem__(self, key):
        return self._coords[key]

    def __hash__(self):
        try:
            out = self._hash
            return out
        except AttributeError:
            self._hash = int(hashlib.sha1(self._coords.view()).hexdigest(), 16)
            return self._hash

    def __repr__(self):
        return "point "+str(self._index)+": "+str(self._coords.__repr__())[6:-1]

    def keys(self):
        '''
        EXAMPLES:
        >>> x = HashPoint([1,2,3])
        >>> x
        point 0: [1, 2, 3]
        >>> x.keys()
        0
        '''

        return self._index

    def values(self):
        '''
        EXAMPLES:
        >>> x = HashPoint([1,2,3])
        >>> x.values()
        array([1, 2, 3])
        '''
        return self._coords

    def items(self):
        '''
        EXAMPLES:
        >>> x = HashPoint([1,2,3])
        >>> x.items()
        (0, array([1, 2, 3]))
        '''
        return self._index, self._coords

    # The <,>,<=,>= comparators below use only the index to compare points. The
    # == and != comparators behave as follows. Two hash points will return x==y
    # as True if and only if they have the same index and the same _coords.
    # Otherwise, they are not equal (i.e., __ne__ returns True), even if they
    # have the same index. This has
    # a possibly strange consequence. One can have x<y False, x<=y True, but
    # x!=y also True.
    def __lt__(self, other):
        return self._index < other._index

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return self._index <= other._index

    def __ge__(self, other):
        return other <= self

    def __eq__(self, other):
        coordinate_cmp = True
        # Note that for numpy.arrays x=numpy.array([1,2,3]) and
        # y=numpy.array([1,4,5]), x==y will return another numpy array, namely
        # array([ True,  False,  False], dtype=bool).
        for _coordinate in self._coords == other._coords:
            if _coordinate:
                continue
            else:
                coordinate_cmp = False
                break
        return self._index == other._index and coordinate_cmp

    def __ne__(self, other):
        return not self == other

#    # Depreciated in python3.
#    def __cmp__(self, other):
#        return self._index.__cmp__(other._index)

'''
Acts like a dict

A wrapped numpy array to allow hashing.

Takes a single pair of points which defines an edge.
Points can either be a np.array, a tuple or a list.
'''

class HashEdge:
    '''
    EXAMPLES:
    >>> HashEdge(np.array(([0,0,0],[1,1,1])), index = 99)
    edge 99: [[0 0 0] [1 1 1]]
    '''
    def __init__(self, edge, index=0, DEBUG=False):

        self.index = index
        if DEBUG:
            print(edge)

# assumes an undirected graph, where point and endPoints are unordered
# allows cmp to compare the edge
# "(0, 1)" assumes an a vertex and an endPoint

        for point in (0, 1):
            edge = sorted(edge, key=lambda component: component[point])

        if isinstance(edge, np.float64):
            self.edge = edge
        else:
            self.edge = np.array(edge)

    def __len__(self):
        return len(self.edge)

    def __getitem__(self, key):
        return self.edge[key]

    def __hash__(self):
        try:
            out = self._hash
            return out
        except AttributeError:
            self._hash = int(hashlib.sha1(self.edge.view()).hexdigest(), 16)
            return self._hash

    def __repr__(self):
        return "edge "+str(self.index) +": %s" % str(self.edge).replace('\n', '')

    def keys(self):
        '''
        EXAMPLES:
        >>> e = HashEdge(np.array(([0,0,0],[1,1,1])), index = 99)
        >>> e.keys()
        99
        '''
        return self.index

    def __cmp__(self, other):
        """
        >>> HashEdge(np.array(([0,0,0],[1,2,3]))) == \
                HashEdge(np.array(([0,0,0],[1,2,3])))
        True
        >>> HashEdge(np.array(([0,0,0],[1,1,1]))) == \
                HashEdge(np.array(([1,1,1],[0,0,0])))
        True
        >>> HashEdge(np.array(([0,0,0],[1,1,1]))) == \
                HashEdge(np.array(([0,0,0],[2,2,2])))
        False
        """
        return (self.edge.flatten() == other.edge.flatten()).all()

    def __eq__(self, other):
        return self.__cmp__(other)

    def __mul__(self, other):
        """
        >>> HashEdge([[0,0,0],[1,1,3]]) * 2
        edge 0: [[0 0 0] [2 2 6]]
        """
        if not isinstance(other, float) \
                and not isinstance(other, int):
            raise NotImplementedError("Cannot multiply type %s" % type(other))
        newedge = []
        for point in self.edge:
            newedge.append([component * other for component in point])

        return HashEdge(np.array(newedge), self.index)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
