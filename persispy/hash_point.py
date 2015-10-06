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
    def __init__(self,coords):
        self._coords=np.array(coords)

    def __hash__(self):
        try:
            out=self._hash
            return out
        except:
            try:
                self._hash=int(hashlib.sha1(self._coords.view()).hexdigest(),16)
                out=self._hash
                return out
            except AttributeError as x:
                print "Please pass numpy array of a single point, not", x

    def __repr__(self):
        return self._coords.__repr__()

