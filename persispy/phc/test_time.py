from persispy.phc import interface
from persispy.samples import points
import timeit

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def main():
    runs = [x*100 for x in range(5,10)]
    print runs
    for testPoints in runs:
        print "sample "+str(testPoints)+" point sphere"
        wrapped = wrapper(points.sphere, num_points=testPoints)
        print testPoints, timeit.timeit(wrapped, number=10)

        print "phc "+str(testPoints)+" point sphere"
        wrapped = wrapper(interface.phc_cloud, eqn = "x^2+y^2+z^2-1", \
            num_points=testPoints)
        print testPoints, timeit.timeit(wrapped, number=10)

        print "phc "+str(testPoints)+" point complex sphere"
        wrapped = wrapper(interface.phc_cloud, eqn = "x^2+y^2+z^2-1", \
            num_points=testPoints, allow_complex=True)
        print testPoints, timeit.timeit(wrapped, number=10)

if __name__== "__main__": main()

