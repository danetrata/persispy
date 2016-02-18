import csv

def float_or_int(string):
    try:
        return int(string)
    except ValueError:
        return float(string)

def read_csv(filename):
    """
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # assumes a header
        sheet = [row for row in reader]
        
    columns = []
    for column in zip(*sheet):
        columns.append(np.array([float_or_int(item) for item in column]))
    return columns



def show(fig):
    """
    Due to avoiding pyplot, we must handle all the backend calls...
    """
    master = tk.Tk()
    canvas = FigureCanvasTkAgg(fig, master = master)
    NavigationToolbar2TkAgg(canvas, master)
    canvas.get_tk_widget().pack()
    canvas.draw()
    master.mainloop()

import matplotlib.pyplot as plt
def plot_data(x, y, title, subtitle, xtitle, ytitle, threshold = False):
    """
    input: x axis, y axis
    where the index of each is a point
    creates a scatter plot
    """
    fig, ax = plt.subplots(2, sharex=True, sharey=True)
    for sub in ax:
        sub.set_xlim(0, max(x))
        sub.set_ylim(0, max(y))

    scatter(ax[0],
            x,
            y,
            title,
            subtitle,
            xtitle,
            ytitle
            )
    heat_map(ax[1],
            x,
            y,
            title,
            subtitle,
            xtitle,
            ytitle
            )

        
    for sub in ax:
        if threshold:
            add_threshold(sub, x, threshold)

    fig.tight_layout()

    plt.show()
    
def add_threshold(ax, x, formula):
    x = np.array(range(min(x), max(x)))
    
    f = formula(x) 
    ax.plot(x, f, '-')

def scatter(ax, x, y, title, subtitle, xtitle, ytitle):
    ax.plot(x, y, 'ro')

    ax.set_title(title+"\n"+subtitle+" number of points: "+str(len(x)))
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)


def heat_map(ax, x, y, title, subtitle, xtitle, ytitle):

# Calculate the point density
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    

    ax.scatter(x, y, c=z, s=100, edgecolor='')
    ax.set_title(title+"\n"+subtitle+" number of points: "+str(len(x)))
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)

from mpl_toolkits.mplot3d import Axes3D

def plot3d(x, y, z, title, subtitle, xtitle, ytitle, ztitle):

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, marker = '.', color = '#ff6666')
    plt.title(title+"\n"+subtitle)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_zlabel(ztitle)
    ax.elev = 30
    ax.axim = 25

    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
def plot3d_surface(x, y, z, title, subtitle, xtitle, ytitle, ztitle):

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
# note this: you can skip rows!

    xi = np.linspace(min(x),max(x),100)
    yi = np.linspace(min(y),max(y),100)
# VERY IMPORTANT, to tell matplotlib how is your data organized
    zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

    CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, color='k')
    ax = fig.add_subplot(1, 2, 2, projection='3d')

    xig, yig = np.meshgrid(xi, yi)

    surf = ax.plot_surface(xig, yig, zi, linewidth=0)

    plt.title(title+"\n"+subtitle)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_zlabel(ztitle)

    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


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
        temp = data
        temp.sort()
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
            value = int(value)
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


import sys
def main():
    stat = Stats()
    if(1 < len(sys.argv)):
        prompt = sys.argv[1]
    else:
        prompt = raw_input("Enter a filename: ")
    numPoints, distance, connectedComponents = read_csv(prompt)
    dataSet = [numPoints, distance, connectedComponents]

    dataSetName = ["number of points", 
            "distance between points", 
            "connected components"]

#     i = 0
#     for variable in dataSet:
# #         print dataSet
#         print "\n\n\n" + dataSetName[i]
#         print "size", len(numPoints)
#         print "mean", stat.mean(variable)
#         print "median", stat.median(variable)
#         print "mode", stat.mode(variable)
#         print "range", stat.range(variable)
#         print "varience", stat.varience(variable)
#         print "std dev", stat.standard_deviation(variable)
#         i += 1
#     meanNumPoints = stat.mean(numPoints)
    
    totallyConnected = [[],[]]
    for i in range(len(connectedComponents)):
        if connectedComponents[i] == 1 and numPoints[i] > 50:
            totallyConnected[0].append(numPoints[i])
            totallyConnected[1].append(distance[i])




    if False:
        plot3d(numPoints, distance, connectedComponents,
                "all data in one graph",
                prompt,
                dataSetName[0], dataSetName[1], dataSetName[2])

        plot_data(numPoints,
                connectedComponents,
                "points and number of components",
                prompt,
                dataSetName[0],
                dataSetName[2]
                )
        plot_data(distance,
                connectedComponents,
                "distance and number of components",
                prompt,
                dataSetName[1],
                dataSetName[2]
                )

    if False:
        plot_data(x = totallyConnected[0], 
                y = totallyConnected[1], 
                title = "totally connected components",
                subtitle = prompt,
                xtitle = dataSetName[0],
                ytitle = dataSetName[1],
                threshold = lambda n: (np.log(n)+100)/(20*n)
                )

    from scipy.optimize import curve_fit
    def func(n, c, omega): 
        return ((np.log(n)+c)/(omega*n))**(1.0/2)

#     cOptimized, omegaOptimized = curve_fit(func, 
#             totallyConnected[0], 
#             totallyConnected[1])
#     print cOptimized, omegaOptimized
#     
#     while(True):
#         comega = raw_input("enter c and \omega (seperated by a space): ")
#         comega = [float(number) for number in comega.split(' ')]
# 
#         plot_data(x = totallyConnected[0], 
#                 y = totallyConnected[1], 
#                 title = "totally connected components",
#                 subtitle = prompt,
#                 xtitle = dataSetName[0],
#                 ytitle = dataSetName[1],
#                 threshold = lambda n: ((np.log(n)+comega[0])/(comega[1]*n))**(1.0/2)
#                 )

"""
def findhttp://stackoverflow.com/questions/32146633/opencv-fit-the-detected-edges_first(item, vec):
"""
"""return the index of the first occurence of item in vec"""
        if isinstance(vec, np.int64):
            return vec
        for i in range(len(vec)):
            if item == vec[i]:
                return i
        return -1

# Now the points we want are the lowest-index 255 in each row
    window = numPoints.transpose()

    xy = []
    for i in range(len(window)):
        col = window[i]
        j = find_first(len(numPoints), col)
        if j != -1:
            xy.extend((i, j))
# Reshape into [[x1, y1],...]
    data = np.array(xy).reshape((-1, 2))

    plt.figure(1, figsize=(8, 16))
    ax1 = plt.subplot(211)
    ax1.plot(data[:,1])
    plt.show()


if __name__ == "__main__": main()
