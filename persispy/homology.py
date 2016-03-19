import numpy as np
#import numpy.random as npr
#import scipy.sparse.csgraph as csgraph
#import scipy.sparse as sparse
from .utils import tuples

class Factorial:
    def __init__(self):
        self.values=[1L]

    def factorial(self,n):
        print "call"
        if(len(self.values)-1<n):
            print "computation"
            self.values.append(self.factorial(n-1)*n)
            return self.values[n]
        return self.values[n]

    def nPr(self,n,k):
        return self.factorial(n)/(self.factorial(n-k))

    def nCr(self,n,k):
        return self.factorial(n)/(self.factorial(n-k)*self.factorial(k))

def _SimplexIndex(simplex,n,f=Factorial()): #simplex is a wSimplex
    k=len(simplex)
    value = f.nCr(n+1,k-1)
    for i in range(k):
        value = value - f.nCr(n-simplex[i]+i,k-i)

    return value


