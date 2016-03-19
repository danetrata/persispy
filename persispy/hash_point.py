import numpy as np
import hashlib as hashlib

class HashPoint:
    '''
    A wrapped numpy array to allow hashing.

    Vars: _coords (a numpy array).

    EXAMPLES:
    >>> HashPoint([1,2,3])
    array([1, 2, 3])
    '''
    def __init__(self,coords,index=0):
        self._coords=np.array(coords)
        self._index=index
	
    def __len__(self):
	    return len(self._coords)

    def __getitem__(self, key):
        return self._coords[key]

    def __hash__(self):
        try:
            out=self._hash
            return out
        except:
            self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
            return self._hash

    def __repr__(self):
        return "point "+str(self._index)+": "+str(self._coords.__repr__())[6:-1]

    def keys(self):
        return self._index

    def values(self):
        return self._coords
    
    def items(self):
        return self._index, self._coords

    # The <,>,<=,>= comparators below use only the index to compare points. The
    # == and != comparators behave as follows. Two hash points will return x==y
    # as True if and only if they have the same index and the same _coords.
    # Otherwise, they are not equal (i.e., __ne__ returns True), even if they have the same index. This has
    # a possibly strange consequence. One can have x<y False, x<=y True, but
    # x!=y also True.
    def __lt__(self,other):
        return self._index < other._index

    def __gt__(self,other):
        return other < self

    def __le__(self,other):
        return self._index <= other._index

    def __ge__(self,other):
        return other <= self

    def __eq__(self,other):
        coordinate_cmp = True
        # Note that for numpy.arrays x=numpy.array([1,2,3]) and
        # y=numpy.array([1,4,5]), x==y will return another numpy array, namely
        # array([ True,  False,  False], dtype=bool).
        for v in self._coords==other._coords:
            if v:
                continue
            else:
                coordinate_cmp = False
                break
        return self._index==other._index and coordinate_cmp

    def __ne__(self,other):
        return not self==other

    # Depreciated in python3.
    def __cmp__(self,other):
        return self._index.__cmp__(other._index)
