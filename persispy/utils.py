def tuples(k,l):
    '''
    EXAMPLES:
    >>> tuples(2,[1,2,3])
    [[1, 2], [1, 3], [2, 3]]
    '''
    t=[]
    n=len(l)
    if n<k:
        return t
    if k==1:
        return [[x] for x in l]
    for m in range(n):
        for u in tuples(k-1,l[m+1:n]):
            t.append([l[m]]+u)
    return t
