import sortedcontainers
from collections import defaultdict
import numpy as np
import itertools as it

class PersistentHomology:
    def __init__(self, sortedCliqueList, n):
        self.componentDictionary = dict()
        self.highestLabel = defaultdict(int)
        self.eventQueue = sortedcontainers.SortedList()
        self.bettyList = defaultdict(int)
        self.componentCount = dict()
        simplices = sortedCliqueList.get_full_simplex_iterator(n)
        for s in simplices:
            self._addSimplex(s)
        
    def compute(self, epsilon):
        while self.eventQueue[0].epsilon<epsilon:
            self.eventQueue[0].handle(self.bettyList)
            del self.eventQueue[0]
        
    def _addSimplex(self, Sim):
        if len(Sim)==0:
            return np.float_(0.0)
        if Sim in self.componentDictionary:
            return self.componentDictionary[Sim].weight
        if len(Sim)==1:
            S = _SimplexContainer(Sim, self.highestLabel[0], np.float_(0.0))
            self.highestLabel[0] +=1
            self.componentDictionary[Sim] = S
            self.eventQueue.add(_event(np.float_(0.0), 0, 1))
            return np.float_(0.0)
        else:
            dim = len(Sim)-1
            
            weight = np.float_(0.0)
            for x in it.combinations(Sim, len(Sim)-1):
                weight = max(weight, self._addSimplex(x))
            if dim == 1:
                weight = np.sqrt(sum((Sim[0]._coords-Sim[1]._coords)*(Sim[0]._coords-Sim[1]._coords)))
            S = _SimplexContainer(Sim, self.highestLabel[dim], weight)
            self.highestLabel[dim]+=1
            self.componentDictionary[Sim] = S
            i = it.combinations(Sim, len(Sim)-1)
            a = self.componentDictionary[i.next()]
            for x in i:
                if a.componentIndex>self.componentDictionary[x].componentIndex:
                    a = self.componentDictionary[x]
            equal = True
            for x in it.combinations(Sim, len(Sim)-1):
                if a.componentIndex != self.componentDictionary[x].componentIndex:
                    equal = False
                    _SimplexContainer.mergeComponent(a,self.componentDictionary[x])
            if equal:
                self.eventQueue.add(_event(weight, dim, 1))
            else:
                self.eventQueue.add(_event(weight, dim-1, -1))
            return weight
                                    
            
        
        
        '''
        if Sim not in self.componentDictionary:
            dim = len(Sim)-1
            S = _SimplexContainer(Sim, self.highestLabel[dim])
            self.componentDictionary[Sim]=S
            self.highestLabel[dim]+=1
            if dim == 0:
                self.eventQueue.add(_event(0, 0, 1))
                return 0
            
            weight = 0
            for i in range(len(S.simplex)):
                weight = max(weight, self._addSimplex(S.simplex[:i]+S.simplex[i+1:]))
            if dim == 1:
                weight = np.sqrt(sum((S.simplex[0]._coords-S.simplex[1]._coords)*(S.simplex[0]._coords-S.simplex[1]._coords)))
            a = self.componentDictionary[S.simplex[:-1]]
            added = False
            lowestIndex = a
            for i in range(1,len(S.simplex)):
                b = self.componentDictionary[S.simplex[:i]+S.simplex[i+1:]]
                if a.componentIndex > b.componentIndex:
                    lowestIndex = b
                if a.componentIndex != b.componentIndex:
                    self.eventQueue.add(_event(weight, dim-1, -1))
                    added = True
            if not added:
                self.eventQueue.add(_event(weight, dim, 1))
            for i in range(0,len(S.simplex)):
                _SimplexContainer.mergeComponent(lowestIndex,self.componentDictionary[S.simplex[:i]+S.simplex[i+1:]])
            return weight
        '''    
                

                


class _SimplexContainer:
    def __init__(self, S, Ci, w):
        self._nextSimplex = None
        self._firstSimplex = self
        self.simplex = S
        self.componentIndex = Ci
        self.weight = w
        
    @staticmethod
    def mergeComponent(S1, S2):
        if S1==S2:
            return
        tempS = S1._nextSimplex
        S1._nextSimplex = S2._firstSimplex
        S=S1
        while S._nextSimplex is not None:
            S._firstSimplex = S1._firstSimplex
            S.componentIndex = S1.componentIndex
            S = S._nextSimplex
        S._firstSimplex = S1._firstSimplex
        S.componentIndex = S1.componentIndex
        S._nextSimplex = tempS
        
    def __cmp__(self, other):
        '''
        if self == None and other == none:
            return 0
        if self == None:
            return -1
        if other == None:
            return 1
        '''
        return self.componentIndex.__cmp__(other.componentIndex)

class _event:
    def __init__(self, e, b, c):
        self.epsilon = e
        self.betty = b
        self.change = c
        
    def __cmp__(self, other):
        if self.epsilon < other.epsilon:
            return -1
        if self.epsilon > other.epsilon:
            return 1
        return 0
    
    def handle(self, bettylist):
        bettylist[self.betty] += self.change
        
    def __str__(self):
        return self.__repr__
    
    def __repr__(self):
        return "("+str(self.epsilon)+", "+str(self.betty)+", "+str(self.change)+")"
    
    
    
    