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
    def __init__(self,coords,index):
        self._coords=np.array(coords)
        self._index=index
    def __hash__(self):
        try:
            out=self._hash
            return out
        except:
            self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
            return self._hash

    def __repr__(self):
        return "point "+str(self._index)+": "+str(self._coords.__repr__())[6:-1]
    def __cmp__(self,other):
        return self._index.__cmp__(other._index)
