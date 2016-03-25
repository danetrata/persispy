import numpy as np
import numpy.random as npr
import scipy.sparse.csgraph as csgraph
import scipy.sparse as sparse
from persispy.utils import tuples
# from persispy.hash_edge import HashEdge
from persispy.hashing import HashEdge
from numpy import array
import itertools
import sys

DEBUG = False

class wSimplex:
    '''
    An oriented simplex.
    '''
    def __init__(self,vertices,weight):
        '''
        The orientation is the one given by the list of vertices.

        Variables:
            _vertices: a list of points.
            _weight: the weight.
        '''
        self._vertices=tuple(sorted(list(vertices), key=lambda v:v._index))
        self._weight=weight
        self._index=-1 #the index of this simplex in the compatible total ordering

    def weight(self):
        return self._weight

    def __repr__(self):
        return 'Weighted simplex '+ str(self._vertices)+' with weight '+str(self._weight)

    def __eq__(self,right):
        if set(self._vertices)==set(right._vertices) and self._weight==right._weight:
            return True
        else:
            return False

    def __lt__(self,other):
        return self._weight < other._weight

    def __gt__(self,other):
        return other < self

    def __le__(self,other):
        return self._weight <= other._weight

    def __ge__(self,other):
        return other <= self

    def __eq__(self,other):
        return self._weight==other._weight and self._vertices==other._vertices

    def __ne__(self,other):
        return not self==other

    # DEPRECIATED in python3
    def __cmp__(self,other):
        value = 0.0;
        # This is extremely dangerous as set is a standard library class in
        # Python. In any case, __cmp__ is depreciated in python3.
        set = False;
        if (self._weight!=other._weight) and not set:
            value = self._weight - other._weight
            set = True
        if (len(self._vertices)!=len(other._vertices)) and not set:
            walue = len(self._vertices)-len(other._vertices)
            set = True
        if not set:
            if self._vertices!=other._vertices:
                for i in range(len(self._vertices)):
                    if self._vertices[i]!=other._vertices[i]:
                        if self._vertices[i]<other._vertices[i]:
                            return -1
                        if self._vertices[i]>other._vertices[i]:
                            return 1
        if value<0:
            return -1
        if value>0:
            return 1
        return 0

class wGraph:
    def __init__(self, adjacencies, epsilon):
        '''
        Input: a dictionary of edges indexed by vertices.
        Output: a wGraph object.

        Variables:
            ._adj: the adjacency dictionary.
            ._epsilon: the distance between points
            ._connected_components - Depth first search tree of components
                created after .connected_components()
            ._edges: List of a edges of type HashEdge with the form 
                set(vertex, endPoint),
                created after .connected_edges() . Because we assume an 
                unordered graph, the edges are unordered through the use
                of hash_edge.HashEdge() .
        '''
        self._adj = adjacencies
        self._epsilon = epsilon
        self._connected_components = None
        self._edges = None

        # place holder for more efficient recursive coding
        # .connnected_components() has issues without the following line
        if len(adjacencies) > 1000:
            sys.setrecursionlimit(len(adjacencies))

    @classmethod
    def from_edge_list(cls,vertices,edges,validate=False):
        '''
        NOTE: vertices needs to be a set or list of hashable objects.
        '''
        if validate==True:
            for e in edges:
                if len(e) != 3:
                    raise TypeError('Edges are lists of pairs of distinct vertices followed by a weight.')
                if e[0]==e[1]:
                    raise TypeError('Edges are lists of pairs of distinct vertices followed by a weight.')
        
        adj={v:set() for v in vertices}
        for e in edges:
            adj[e[0]].add((e[1],e[2]))
            adj[e[1]].add((e[0],e[2]))
        return cls(adj)

    """
    start magic methods
    """

    def __repr__(self):
        return 'Weighted graph with '+repr(self.num_points())+' points and '+repr(self.num_edges())+' edges'

    def __len__(self):
        """
        We return the number of edges.
        also see .order() and .num_edges()
        """
        return self.num_edges()


    """
    end magic methods
    """

    def vertices(self):
        return self._adj.keys()

    def num_points(self):
        return len(self._adj.keys())

    def order(self):
        return self.num_edges()

    def num_edges(self):
        count=0
        for v in self._adj.keys():
            count=count+len(self._adj[v])
        return count/2

    def degree(self, p):
        """
        returns the degree of the point
        """
        return len(self._adj[p])

    def metric(self,p,q):
        if p not in self._adj.keys() or q not in self._adj.keys():
            raise ValueError('The points must be vertices.')
        else:
            for e in self._adj[p]:
                if e[0]==q:
                    return e[1]
            return -1    

    def connected_component(self, point, visited, time):
        """
        RECURSIVE
        We note the time passed by the input when a node was visited in the 
        'visited' dict. We then call itself on any adjacent nodes that have
        not been visted.
        """
        if DEBUG: print(time)
        visited[point]=time
        for neighbor in self._adj[point]:
            if not visited[neighbor[0]]: # uses the fact that 0 evals to False
                self.connected_component(neighbor[0], visited, time)

    def connected_components(self):
        '''
        We returns a list giving the connected components of the wGraph.
        NOTICE: Gives only a depth first search tree. This is to save operations
        if our only goal is to count the number of connected components.
        Call .connected_edges() for the connected component with edges.
        '''
        visited = {d:0 for d in self._adj}

        time=0
        for point in self._adj: # runs in O(|points| + |edges|)
            if visited[point] == 0:
                time = time + 1
                self.connected_component(point, visited, time)
        
        components = []         
        for connected in range(1, time+1): # runs in O(|components|)
            component = []
            for point in visited: # runs in O(|points in component|)
                if visited[point] == connected:
                    component.append(point)
            if component:
                components.append(component)


        self._connected_components = components

        return components

    def singletons(self, padding = False):
        if not self._connected_components:
            self.connected_components()
        cp = self._connected_components
        if DEBUG:
            for item in cp:
                print(item)

        singles = []
        for component in cp:
            if len(component) == 1: # if the component is a point
                component = list(component[0])
                if DEBUG: print(component)
                while len(component) < padding:
                    component.append(0)
                if DEBUG: print(component)
                singles.append(component)
        return singles

    def connected_edges(self, padding = False):
        """
        Returns a list of edges that make up a connected component. We assume
        no multiple edges.
        """

        if not self._connected_components:
            self.connected_components()
        cp = self._connected_components

        componentIndex = 0
        components = []
        for component in cp:
            edges = {}
            if len(component) > 1: # if the component is not a point
                edgeIndex = 0
                for vertex in component:
                    vertexList = list(vertex)
                    while len(vertexList) < padding:
                        vertexList.append(0)
                    for endPoint in self._adj[vertex]:
                        endPointList = list(list(endPoint)[0])
                        while len(endPointList) < padding:
                            endPointList.append(0)
                        edges[edgeIndex] = HashEdge(
                                array([ vertexList, endPointList]),
                                index = edgeIndex
                                )
                        edgeIndex += 1
            if edges:
                componentIndex += 1
                edges = edges.values()
                edges = set(edges)
                components.append(edges)

        self._edges = components
        return components

    def cloud_dist(self,pointlist):
        '''
        Returns the maximum of the distances of all pairs of points in 
        pointlist.
        '''
        dist=0
        if len(pointlist)==1:
            return dist
        for t in tuples(2,pointlist):
            d=self.metric(t[0],t[1])
            if d>=0:
                dist=max(dist,d)
            else:
                return -1
        return dist


    def neighborhood_graph(self, epsilon):
        '''
        INPUT: epsilon.
        OUTPUT: the subgraph consisting of those edges with weight less than epsilon.
        '''
        keys=self._adj.keys()
        adj={v:[] for v in keys}
        for k in keys:
            for v in self._adj[k]:
                if v[1]<epsilon:
                    adj[k].append(v)
        return wGraph(adj)

    def VRComplex(self, epsilon, dimension, method='incremental'):
        # Do we even need this any more?
        def lowerNBRS(vtx):
            vtxs = []
            for i in range(vtx + 1, len(self._adj.keys())):
                if i in self._adj[vtx]:
                    vtxs.append(i)
            return vtxs

        def intersect(a, b):
            inter = []
            for i in range(0, len(a)):
                if (a[i] in b):
                    inter.append(a[i])
            return inter

        def addCoface(dimension, simplex, vtxSet, complex):
            complex[len(simplex)].append(wSimplex(simplex,self.cloud_dist(simplex)))
            if len(simplex) > dimension - 1:
                return complex
            else:
                for v in vtxSet:
                    simp = simplex.append(v)
                    vtxSet2 = intersect(lowerNBRS(v), vtxSet)
                    addCoface(dimension, simp, vtxSet2, complex)
                return complex

        if method=='inductive':
            return None

        elif method == 'incremental':
            complex = {n:[] for n in range(dimension+1)}
            for u in self._adj.keys():
                vtxSet = lowerNBRS(u)
                addCoface(dimension, [u], vtxSet, complex)
            return wSimplicialComplex(self,complex)
        else:
            return None

    def adjacency_matrix(self):
        '''
        Output: a scipy.sparse.csr_matrix.
        '''
        keys=list(self._adj.keys())
        N=len(keys)
        ctr=0
        indptr=[ctr]
        indices=[]
        for k in keys:
            for e in self._adj[k]:
                ctr=ctr+1
                indices.append(keys.index(e[0]))
            indptr.append(ctr)
        data=np.array([1.0 for x in range(len(indices))])
        return sparse.csr_matrix((data,indices,indptr),shape=((len(keys),len(keys))))

    def connected_components_1(self, return_labels = False):
        '''
        Output: a positive integer.
        construction of adjacency_matrix().
        '''
        return csgraph.connected_components(self.adjacency_matrix(),directed=False, return_labels = return_labels)


def wRandomGraph(n,p,epsilon):
    '''
    Returns the Gilbert (Erdos-Renyi) random graph G(n,p), which includes each edge independently with
    probability 0<p<1. A random weight in the range [0,epsilon) is assigned to each edge.
    '''
    dictionary={v:[] for v in range(n)}
    for i in range(n):
        for j in range(i+1,n):
            if npr.random() < p:
                w=epsilon*npr.random()
                dictionary[i].append([j,w])
                dictionary[j].append([i,w])
    return wGraph(dictionary,epsilon)

class wSimplicialComplex:
    def __init__(self,wgraph,simplices):
        self._wgraph=wgraph
        self._simplices=simplices

    @classmethod
    def from_clique_list(cls,wgraph,cliques,verify=False):
        '''
        Input: a wGraph together with a list of simplices on the vertex set of the graph. It
        is assumed (and not checked unless verify==True) that the 1-skeleton of every simplex is contained in
        the graph.
        '''

        simplices={0:[wSimplex([k],0) for k in wgraph._adj.keys()]}
        simplices[1]=[]

        for t in tuples(2,wgraph._adj.keys()):
            if wgraph.metric(t[0],t[1])>0:
                simplices[1].append(wSimplex(t,wgraph.metric(t[0],t[1])))

        for v in cliques:
            if verify==True:
                '''
                Check that the 1-skeleton of v is indeed contained in the wgraph.
                '''
                for vlist in tuples(2,v):
                    if wgraph.metric(vlist[0],vlist[1])==-1:
                        raise ValueError('All cliques must have 1-skeleton included in wgraph.')
            for d in range(3,len(v)+1):
                for vlist in tuples(d,v):
                    # The next crudge is to make this bit backwards compatible
                    # with python2. Note that has_key() is no longer an
                    # attribute of dictionaries in python3.
                    # TEST: I have not tested it on python2 as of 19 March 2016.
                    try:
                        if not simplices.has_key(d-1):
                            simplices[d-1]=[]
                    except AttributeError:
                        if not d-1 in simplices:
                            simplices[d-1]=[]
                    weight=0
                    for i in range(d-1):
                        inbrs=wgraph._adj[vlist[i]]
                        for j in inbrs:
                            if j[0] in vlist:
                                weight=max(weight,j[1])
                    new_simplex=wSimplex(vlist,weight)
                    if new_simplex not in simplices[d-1]:
                        simplices[d-1].append(new_simplex)
        return wSimplicialComplex(wgraph,simplices)

    def __repr__(self):
        return repr(self.dimension())+'-dimensional weighted simplicial complex with '+repr(len(self._simplices[0]))+ ' vertices and '+repr(self.simplices_positive())+ ' positive-dimensional simplices'

    def simplices_positive(self):
        return sum([len(self._simplices[k]) for k in range(1,self.dimension()+1)])

    def dimension(self):
        dim=0
        for k in self._simplices.keys():
            if len(self._simplices[k])>0:
                dim=max(k,dim)
        return dim

    def simplex_sort(self):
        '''
        Sorts the simplices with respect to the lexographic ordering dictated by the
        ordering of the vertices implicit in the list self._simplices[0].
        '''
        dictionary=[x._vertices[0] for x in self._simplices[0]]
        def simplex_cmp_lex(s,t):
            sindices=tuple([dictionary.index(x) for x in s._vertices])
            tindices=tuple([dictionary.index(x) for x in t._vertices])
            return cmp(sindices,tindices)
        for d in range(1,self.dimension()+1):
            self._simplices[d].sort(simplex_cmp_lex)
        return None

    def VRComplex(self, epsilon):
        vertices=self._wgraph._adj.keys()
        edges=dict()
        for v in vertices:
            new_edges=[]
            for e in self._wgraph._adj[v]:
                if e[1]<epsilon:
                    new_edges.append(e)
            edges[v]=new_edges
        wg=wgraph.wGraph(edges)
        simplices=dict()
        for d in self._simplices.keys():
            simplices[d]=[]
            for s in self._simplices[d]:
                if s.weight() < epsilon:
                    simplices[d].append(s)
        return wSimplicialComplex(wg,simplices)

class sorted_clique_list:
    def __init__(self,wg):
        '''wg is a weighted graph'''
        self._cliques=[]
        sorted_clique_list._BronKerboschPivot(set(),set(wg._adj.keys()),set(),wg._adj,self._cliques)
        self._cliques.sort()
        
    def get_simplex_iterator(self,n):
        '''
        gives an iterable which includes all n simplices
        '''
        i = set()
        for x in self._cliques:
            if len(x)>=n+1:
                i.update(itertools.combinations(x,n+1))
        return _clique_iterator(iter(i))
    
    def get_ordered_simplex_iterator(self,n):
        i = set()
        for x in self._cliques:
            if len(x)>=n+1:
                i.update(itertools.combinations(x,n+1))
        return _clique_iterator(iter(sorted(list(i))))
    
    def get_full_simplex_iterator(self,n):
        '''
        gives an iterable which includes all k simplices for k <= n
        '''
        i = self.get_simplex_iterator(n)
        j = []
        for c in self._cliques:
            if len(c)<n+1:
                j.append(c)
        return _clique_iterator(itertools.chain(iter(j),i))

    @staticmethod
    def _BronKerbosch(r,p,x,adj,c):
        if len(p)==0 and len(x)==0:
            c.append(sorted(tuple(r)))
        else:
            for v in set(p):
                nbh = {x[0] for x in adj[v]}
                sorted_clique_list._BronKerbosch(r | {v}, p & nbh, x & nbh,adj,c)
                p.remove(v)
                x.add(v)
    
    @staticmethod
    def _BronKerboschPivot(r,p,x,adj,c):
        if len(p)==0 and len(x)==0:
            c.append(sorted(tuple(r)))
        else:
            # The next line looks a little fishy.--Ben
            for u in p|x:
                break
            # u = iter(p | x).next()
            for v in iter(set(p) - adj[u]):
                nbh = {x[0] for x in adj[v]}
                sorted_clique_list._BronKerboschPivot(r | {v}, p & nbh, x & nbh,adj,c)
                p.remove(v)
                x.add(v)
            
class _clique_iterator:
    def __init__(self, i):
        self.iterator = i
        
    def __iter__(self):
        return self
    
    def next(self):
        return tuple(self.iterator.next())
    
