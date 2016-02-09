import numpy as np
import hashlib as hashlib

"""
HashEdge's behavior will be different from HashPoint.
In this module, we will use a factory to keep all of the HashPoint setup
contained in here.
"""

'''
Acts like a dict

A wrapped numpy array to allow hashing.

Takes a single pair of points which defines an edge.
Points can either be a np.array, a tuple or a list.

NOTE: 
'''

class HashEdge:


    def __init__(self, edge, index = 0):

        self.index = index
        print edge

# assumes an undirected graph, where point and endPoints are unordered
# allows cmp to compare the edge
        for axis in (0, 1):
            edge = sorted( edge, key = lambda component: component[axis])

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
            out=self._hash
            return out
        except:
            self._hash=int(hashlib.sha1(self.edge.view()).hexdigest(),16)
            return self._hash

    def __repr__(self):
        return str(self.edge)

    def __str__(self):
        return "edge "+str(self.index)+": %s" % str(self.edge)

    def keys(self):
        return self.index

    def values(self):
        return self.coords
    
    def items(self):
        return self.index, self.coords

    def __cmp__(self,other):
        if self.edge.all() == other.edge.all():
            return 0


def test():
    print HashEdge(np.array(([0,0,0],[1,1,1])), index = 0)
    print HashEdge(np.array(([0,0,0],[1,1,1])), index = 1)
    print HashEdge([[0,0,0],[1,1,1]])

if __name__ == "__main__": test()
