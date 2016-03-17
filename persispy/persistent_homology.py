import sortedcontainers
from collections import defaultdict
import numpy as np
import itertools as it
import weighted_simplicial_complex as wsc
import matplotlib.pyplot as plt


class PersistentHomology:
    def __init__(self, simplicial_complex, n):
        self.Currentindex=0
        self.VertexDict = dict() #look up simplex container from tuple of vertices
        _wSimplices = [] 
        for dimension in simplicial_complex._simplices:
            if dimension>n:
                break
            _wSimplices.extend(simplicial_complex._simplices[dimension])
        self.Simplices = sorted([SimplexContainer(s) for s in sorted(_wSimplices)])
        self.PersistencePairs = dict()
        for i,s in enumerate(self.Simplices):
            self.VertexDict[tuple(s.simplex._vertices)] = s
            s.index=i
            s.compute_entries(self)
        for s in self.Simplices:
            #print [v._index for v in s.simplex._vertices]
            if len(s.simplex._vertices)!=1:
                rowiszero = False
                x=len(s.entries)
                while s.entries[-1] in self.PersistencePairs:
                    assert len(s.entries)==len(self.PersistencePairs[s.entries[-1]].entries)
                    s.entries = s.entries ^ (self.PersistencePairs[s.entries[-1]].entries)
                    
                    if len(s.entries)==0:
                        print 'zero'
                        rowiszero=True
                        break
                    #print [x.index for x in s.entries]
                if not rowiszero:
                    #print 'pair: '+ str(s.index)+' '+str(s.entries[-1].index)+' '+str(-s.entries[-1].simplex._weight+s.simplex._weight)
                    self.PersistencePairs[s.entries[-1]]=s
            
    def plotBarCode(self):
        for s in self.Simplices:
            if s in self.PersistencePairs:
                plt.axhline(y=s.index,xmin=s.simplex._weight,xmax=self.PersistencePairs[s].simplex.weight)
                print 'here'
        plt.axis([0,2,0,len(self.Simplices)])
        plt.show()
        
class SimplexContainer:
    def __init__(self, sim):
        self.simplex = sim
        self.entries = sortedcontainers.SortedSet()
        self.index = -1
    def compute_entries(self, ph):
        if len(self.simplex._vertices)<2:
            return
        for x in range(len(self.simplex._vertices)):
            # Make more pythonic!
            self.entries.add(ph.VertexDict[tuple(self.simplex._vertices[:x]+self.simplex._vertices[x+1:])])
            
    def __hash__(self):
        return hash(tuple(self.simplex._vertices))
    def __cmp__(self, other):
        return self.simplex.__cmp__(other.simplex)
   
