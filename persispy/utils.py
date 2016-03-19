# This should be completely removed with some of the code that David Dumas
# showed us.
def tuples(k,listable_object):
    '''
    EXAMPLES:
    >>> tuples(2,[1,2,3])
    [[1, 2], [1, 3], [2, 3]]
    '''
    try:
        bag=list(listable_object)
    except TypeError:
        print('persispy.utils.tuples takes a postive integer k and a listable object.')
        raise TypeError

    t=[]
    n=len(bag)
    if n<k:
        return t
    if k==1:
        return [[x] for x in bag]
    for m in range(n):
        for u in tuples(k-1,bag[m+1:n]):
            t.append([bag[m]]+u)
    return t
