"""
Takes a variety of type string and, after solving intersections with phcpy,
returns a persispy point cloud. We must reject equations with with variables t,
e, E, i, I because their meanings are reserved.
"""

from string import ascii_letters, digits

import numpy as np

from persispy.hashing import HashPoint
from persispy.point_cloud import PointCloud

from phcpy.solver import total_degree_start_system, total_degree
from phcpy.trackers import track
from phcpy.solutions import strsol2dict  # points

DEBUG = False


class Intersect(object):
    """
    We take an equation that is in general form A*x^2 + B*x + C = 0 and
    return a PointCloud on that variety.
    """

    def __init__(self,
                 eqn,
                 num_points=1,
                 bounds=1,
                 return_complex=False):
        self._bounds = bounds
        self.complex_threshold = 0.1
        self._failure = num_points
        self.eqn = eqn
        self.varlist, self.coefflist = parse(eqn)
        self.points = []
        if DEBUG:
            self.attempt = 0
#         self._startsystem, self._startsol = self._start_system()
        partition = 256
        i = 0
        while i < num_points // partition:
            self._startsystem, self._startsol = self._start_system()
            self.find_more_points(partition, return_complex)
            i = i + 1

        self.find_more_points(num_points - len(self.points), return_complex)
        self.__call__()

    def degree(self):
        """
        We return the degree of the system.
        """
        return total_degree(self._system())

    def _system(self):
        """
        We construct a square system, where the number of variables is
        equal to the number of eqations. The resulting points are
        regular and bounded by the variety.
        """
        phceqn = self.eqn + ";"
        phcsystem = [phceqn]
        for _ in range(len(self.varlist) - 1):
            phcsystem.append(self._intersect())
        return phcsystem

    #  This first block sets up the start system so the solver
    #  doesn't need to make a new one for each intersection
    def _start_system(self):
        """
        We first set up a start system so phcpy doesn't have to create
        a new one everytime.
        """

        phcsystem = self._system()
        startsystem, startsol = total_degree_start_system(phcsystem)
        if DEBUG:
            print("system of equations")
            print("--")
            for equation in phcsystem:
                print (equation)
            print("--")
            print("start solutions: ", len(startsol))
            for equation in startsystem:
                print (equation)
            for solution in startsol:
                print (solution)
            self.attempt = self.attempt + 1
            print("self.attempt #" + str(self.attempt))
        return startsystem, startsol

    #  Uses the already made start system. Otherwise, identical to
    #  the block above
    def find_more_points(self, num_points, return_complex=False):
        """
        We find additional points on the variety.
        """
        # phcpy solver
        points = []
        failure = 0
        while(len(points) < num_points):
            phcsystem = self._system()
            phcsolutions = track(phcsystem, self._startsystem, self._startsol)

            if DEBUG:
                print("system of equations")
                print("--")
                for sol in phcsolutions:
                    print(sol)
                print("--")
                print("number of solutions: ", len(phcsolutions))
                self.attempt = self.attempt + 1
                print("attempt #" + str(self.attempt))

            #  Parsing the output of solutions
            for sol in phcsolutions:
                if DEBUG:
                    print ("phc solutions: \n", sol)
                solutiondict = strsol2dict(sol)

                point = [solutiondict[variable] for variable in self.varlist]
                if return_complex:
                    points.append(tuple(point))
                else:
                    closeness = True
                    for component in point:
                        # choses the points we want
                        if self._is_close(component.imag) \
                                and self._in_bounds(component.real):
                            # sometimes phcpy gives more points than we ask,
                            # thus the additional check
                            if component == point[-1] \
                                    and closeness \
                                    and len(points) < num_points:
                                points.append(tuple(
                                    [component.real for component in point]))
                                assert len(points) < num_points
                                if DEBUG:
                                    print (
                                        "appended point:",
                                        [component.real for component in point])
                                failure = 0
                        else:
                            closeness = False
                            failure = failure + 1
            if self._failure <= failure:
                raise RuntimeError(
                    "equation has too many complex solutions in a row")

        if DEBUG:
            print ("points: ", points)

        self.points = points + self.points

    def _intersect(self):
        """
        We form intersects from the extracted terms. We return a plane with
        random coefficients to intersect the variety. The intersects must be
        of the same dimension as the variety to prevent a overdetermined
        system (which phc doesn't do nicely)
        """
        bounds = self._bounds
#         location = np.random.uniform(-bounds, bounds)
        randomlist = np.random.normal(scale=bounds, size=len(self.varlist))
        intersect = []
        for i, number in enumerate(randomlist):
            intersect.append(str(number) + " * " + self.varlist[i])
            if i < len(randomlist) - 1:
                intersect.append(" + ")
        intersect.append(";")
        intersect = "".join(intersect)
        return intersect

    def _is_close(self, number):
        """
        We need to deal with the fact that PHC always returns complex solutions,
        as small as 10^-48, so the threshold cannot be 0.
        """
        epsilon = self.complex_threshold
        result = abs(number) <= epsilon
        if DEBUG and result:
            print ("Selected component is close")
        return result

    def _in_bounds(self, number):
        """
        If we need to sample points on unbounded varieties, we check if the
        points are within a certain bound.
        """
        bounds = self._bounds
        if bounds and \
                -bounds <= number and number <= bounds:
            if DEBUG:
                print ("Selected component is in bounds")
            return True
        else:
            return False

    def __call__(self):
        cloudpoints = []
        i = 0
        for coord in self.points:
            cloudpoints.append(
                HashPoint(
                    np.array(
                        coord,
                        dtype=complex
                    ),
                    index=i
                )
            )
            i = i + 1
        self.pointcloud = PointCloud(cloudpoints)
        return self.pointcloud

    def __repr__(self):
        return self.points.__repr__()

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __getattr__(self, name):
        """
        We allow PointCloud methods to be called on the instance.
        """
        try:
            return getattr(self.pointcloud, name)
        except AttributeError:
            raise


def parse(eqn):
    """
    We parse the string into phcpy input to generate the intersects.
    """

    if DEBUG:
        print("=====")
        print("input eqn: ", eqn + ";")
        print("=====")

    terms = eqn
    # Extracting terms from the target
    for operation in ["+", "-", "*", "**", "^"]:
        terms = terms.replace(operation, " ")
    terms = terms.strip(" ")
    varlist = []
    for term in terms:
        if term in ["e", "E", "i", "I", "t"]:
            raise RuntimeError("\"" + term + "\" is reserved. Please use a "
                               "different variable.")
        if not term.isdigit() and term.isalnum() and term not in varlist:
            varlist.append(term)
    varlist.sort()
    if DEBUG:
        print("list of variables: ", varlist)

    coeffs = eqn
    coeffs = coeffs.replace("-", "+")
    coeffs = coeffs.replace(" ", "")
    coeffs = coeffs.split("+")
    coefflist = []

    for coeff in coeffs:
        has_term = False
        for character in coeff:  # we look at the string representation
            if character in ascii_letters:
                has_term = True
                break
        if has_term:
            cut = 0
            for character in coeff:
                if character in digits \
                        or character == ".":
                    cut = cut + 1
                else:
                    if cut == 0:
                        coefflist.append(1)
                    else:
                        coefflist.append(float(term[0:cut]))
                    break

    return varlist, coefflist


if __name__ == "__main__":
    import doctest
    doctest.testmod()
