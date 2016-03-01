import sortedcontainers
from collections import defaultdict
import numpy as np
import itertools as it


class PersistentHomology:
    def __init__(self, sortedCliqueList, n):
        self.Simplices = sortedCliqueList.get_full_simplex_iterator(n)
        self.Simplices.sort()
        self.Currentindex=0
        self.VertexDict = dict()
        for i in range(len(Simplices)):
            self.VertexDict[Simplices[i].vertices] = Simplices[i]
            Simplices[i]._index=i
        
    def compute(self, epsilon):
        while self.Simplices[self.Currentindex]._weight<=epsilon:
            Currentindex = Currentindex + 1
            
