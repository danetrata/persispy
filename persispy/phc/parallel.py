import multiprocessing
from persispy.phc import interface

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def phc_cloud(*args, **kwargs): # wrapper for parallel
    def wrapped():
        return interface.phc_cloud(*args, **kwargs)
    print wrapped()

    pool = multiprocessing.Pool(processes=4)
    results = [pool.apply_async(wrapped) for x in range(4)]
    for x in results:
        print x.get()

def main():
    phc_cloud("x^2 + y^2 + z^2 -1", num_points=10, DEBUG=True, point_cloud=False)


if __name__ == "__main__": main()
