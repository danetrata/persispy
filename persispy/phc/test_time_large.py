import phcpy
from persispy.phc import interface, interface_solve
from persispy.samples import points
import timeit

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def main():
    runs = []
    i = 0
    x = 10
    while(i < 4):
        runs.append(x)
        x = x**2
        i = i + 1
    print runs
    for testPoints in runs:
        print "phc "+str(testPoints)+" point complex sphere"
        wrapped = wrapper(interface.phc_cloud, eqn = "x^2+y^2+z^2-1", \
            num_points=testPoints, return_complex=True)
        print testPoints, timeit.timeit(wrapped, number=10)

if __name__== "__main__": main()

