import sortedcontainers
from collections import defaultdict
import numpy as np
import itertools as it
import weighted_simplicial_complex as wsc
import matplotlib.pyplot as plt
import colorsys

class PersistentHomology:
    def __init__(self, simplicial_complex, n):
        self.Currentindex=0
        self.VertexDict = dict() #look up simplex container from tuple of vertices
        _wSimplices = [] 
        for dimension in simplicial_complex._simplices:
            if dimension<=n+1:
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
                while s.entries[0] in self.PersistencePairs:
                    s.entries = s.entries ^ (self.PersistencePairs[s.entries[0]].entries)
                    #print 'xor'
                    if len(s.entries)==0:
                        rowiszero=True
                        break
                    #print [x.index for x in s.entries]
                if not rowiszero:
                    #print 'pair: '+ str(s.index)+' '+str(s.entries[-1].index)+' '+str(-s.entries[-1].simplex._weight+s.simplex._weight)
                    self.PersistencePairs[s.entries[0]]=s
            
    def plotBarCode(self,d,e,hue = 0,saturation = .5,lightness=.5):
        i=1
        j=1;
        moreElements=True
        #WeightOrderedSimplices=sorted(self.Simplices,key=lambda sim: -sim.simplex._weight)
        while moreElements:
            moreElements=False
            for s in self.Simplices:
                if s in self.PersistencePairs:
                    if len(s.simplex._vertices)>j:
                        moreElements=True
                    if len(s.simplex._vertices)==j:
                        if s.simplex._weight!=self.PersistencePairs[s].simplex._weight:
                            y=i
                            a = 1-(self.PersistencePairs[s].simplex._weight-s.simplex._weight)/e
                            rgb = colorsys.hls_to_rgb((hue+len(s.simplex._vertices)*(3-5**.5)*.5)%1.0,saturation,lightness)
                            i=i+1
                            plt.plot([s.simplex._weight,self.PersistencePairs[s].simplex._weight],[y,y],color=(rgb[0],rgb[1],rgb[2],1-a),linestyle='-', linewidth=1)
            j=j+1
            i=i+30
            
        plt.axis([0,e,0,i])
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
    
    def __lt__(self,other):
        return self.simplex < other.simplex

    def __gt__(self,other):
        return other < self

    def __le__(self,other):
        return self.simplex <= other.simplex

    def __ge__(self,other):
        return other <= self

    def __eq__(self,other):
        return self.simplex==other.simplex

    def __ne__(self,other):
        return not self==other

    def __cmp__(self, other):
        return self.simplex.__cmp__(other.simplex)

