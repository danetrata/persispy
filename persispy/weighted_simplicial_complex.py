import numpy as np
import numpy.random as npr
import scipy.sparse.csgraph as csgraph
import scipy.sparse as sparse
from utils import tuples

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
        self._vertices=list(vertices)
        self._weight=weight

    def weight(self):
        return self._weight

    def __repr__(self):
        return 'Weighted simplex '+ str(self._vertices)+' with weight '+str(self._weight)

    def __eq__(self,right):
        if set(self._vertices)==set(right._vertices) and self._weight==right._weight:
            return True
        else:
            return False

class wGraph:
    def __init__(self,adjacencies):
        '''
        Input: a dictionary of edges indexed by vertices.
        Output: a wGraph object.

        Variables:
            _adj: the adjacency dictionary.
        '''
        self._adj=adjacencies

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
        
        adj={v:[] for v in vertices}
        for e in edges:
            adj[e[0]].append([e[1],e[2]])
            adj[e[1]].append([e[0],e[2]])
        return cls(adj)

    def __repr__(self):
        return 'Weighted graph with '+repr(self.num_points())+' points and '+repr(self.num_edges())+' edges'

    def degree(self,p):
        return len(self._adj[p])

    def metric(self,p,q):
        if p not in self._adj.keys() or q not in self._adj.keys():
            raise ValueError('The points must be vertices.')
        else:
            for e in self._adj[p]:
                if e[0]==q:
                    return e[1]
            return -1    

    def connected_component(self,p,visited,n):
        visited[p]=n
        for q in self._adj[p]:
            if not visited[q[0]]:
                self.connected_component(q[0],visited,n)

    def connected_components(self):
        '''
        Returns a list wGraphs giving the connected components of the wGraph.
        '''
        visited = {d[0]:0 for d in self._adj.keys()}
        n=0
        for p in self._adj.keys():
            if visited[p[0]]==0:
                n=n+1
                self.connected_component(p[0],visited,n)
        print n
        return visited

    def cloud_dist(self,pointlist):
        '''
        Returns the maximum of the distances of all pairs of points in pointlist.
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

    def num_points(self):
        return len(self._adj.keys())

    def num_edges(self):
        count=0
        for v in self._adj.keys():
            count=count+len(self._adj[v])
        return count/2

    def neighborhood_graph(self,epsilon):
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

    def VRComplex(self,epsilon,dimension,method='incremental'):
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
        keys=self._adj.keys()
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

    def connected_components_1(self):
        '''
        Output: a positive integer.

        TODO: write an algorithm to do this from the adjacency matrix, avoiding the
        construction of adjacency_matrix().
        '''
        return csgraph.connected_components(self.adjacency_matrix(),directed=False,return_labels=False)

def wRandomGraph(n,p,epsilon):
    '''
    Returns the Gilbert random graph G(n,p), which includes each edge independently with
    probability 0<p<1. A random weight in the range [0,epsilon) is assigned to each edge.
    '''
    dictionary={v:[] for v in range(n)}
    for i in range(n):
        for j in range(i+1,n):
            if npr.random() < p:
                w=epsilon*npr.random()
                dictionary[i].append([j,w])
                dictionary[j].append([i,w])
    return wGraph(dictionary)

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
                    if not simplices.has_key(d-1):
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

    def VRComplex(self,epsilon):
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