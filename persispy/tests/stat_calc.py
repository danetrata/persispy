import csv

def read_csv(filename):
    """
    checks for 1 connected component in column 3
    """
    column1 = []
    column2 = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # assumes a header
        for row in reader:
            if row[2] == "1":
                column1.append(float(row[0]))
                column2.append(float(row[1]))
        return column1, column2


import matplotlib.pyplot as plt
def scatter_plot(x, y):
    """
    input: x axis, y axis
    where the index of each is a point
    creates a scatter plot
    """
    plt.scatter(x, y)
    plt.xlabel("Number of points")
    plt.ylabel("Epsilon")
    plt.show()

import numpy as np
class Stats:

    def __init__(self):
        pass


    def mean(self, data):
        """
        input: list of numbers
        return: mean
        """
        return sum(data)/len(data)

    def median(self, data):
        data.sort()
        if len(data) % 2 == 0:
            mid = (len(data)/2)-1
            mid2 = len(data)/2
            return (data[mid] + data[mid2])/2.0
        else:
            mid = len(data)/2
            return data[mid]

    def mode(self, data):
        d = {}
        for value in data:
            if value not in d:
                d[value] = 0
            else:
                d[value] =  d[value] + 1
        return d

    def range(self, data):
        lowest = min(data)
        highest = max(data)
        return highest - lowest

    def difference_from_mean(self, data):
        mean = self.mean(data)
        diff = []
        for value in data:
            diff.append(value-mean)
        return diff

    def varience(self, data):
        diff = self.difference_from_mean(data)
        squaredDiff = []
        for d in diff:
            squaredDiff.append(d**2)
        sumSquaredDiff = sum(squaredDiff)
        variance = sumSquaredDiff/len(data)
        return variance


    def standard_deviation(self, data):
        return np.sqrt(self.varience(data))

    def probably_connected(self, numPoints):
        pass
        probablity
        return probablity 

    def expected_connected_radius(self, numPoints):
        pass
        radius =((np.log(numPoints)+1.0)/(1.0*numPoints))**(1/2)
        print "radius", radius
        return radius


def main():
    stat = Stats()
    prompt = raw_input("Enter a filename: ")
    numPoints, distance = read_csv(prompt)

    dataSetName = ["number of points", "distance between points"]
    i = 0
    for dataSet in [numPoints, distance]:
#         print dataSet
        print "\n\n\n" + dataSetName[i]
        print "size", len(numPoints)
        print "mean", stat.mean(dataSet)
        print "median", stat.median(dataSet)
        print "mode", stat.mode(dataSet)
        print "range", stat.range(dataSet)
        print "varience", stat.varience(dataSet)
        print "std dev", stat.standard_deviation(dataSet)
        i += 1

    meanNumPoints = stat.mean(numPoints)

    import matplotlib.pyplot as plt
    plt.plot(numPoints, distance, 'ro')
    plt.title("Totally connected graphs")
    plt.xlabel(dataSetName[0])
    plt.ylabel(dataSetName[1])
    plt.show()

#     print "radius in which points are connected is %f" % \
#             stat.expected_connected_radius(1000)
#             stat.expected_connected_radius(meanNumPoints)
#     print "probablity that points are connected is", \
#             stat.probably_connected(meanNumPoints)
#     scatter_plot(numPoints, distance)


if __name__ == "__main__": main()
