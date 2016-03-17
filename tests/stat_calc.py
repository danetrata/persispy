import csv

def float_or_int(string):
    try:
        return int(string)
    except ValueError:
        return float(string)

import os
def read(object):
    if object[0] == '\'':
        object = object.replace('\'', '').rstrip()
    if os.path.isdir(object):
        sheet = read_directory(object)
    else:
        sheet = read_csv(object)

    columns = []
    for column in zip(*sheet):
        columns.append(np.array([float_or_int(item) for item in column]))
    print "number of trials:", len(columns[0])

#    if os.path.isdir(object):
#        columns = average_trials(columns)

    return columns


def average_trials(dataSet):
    
    numPoints, distance, connectedComponents = dataSet
    # dictionary indexed by (numPoints, distance) 
    npd = {}
    for i, trial in np.ndenumerate(connectedComponents):
        point = (numPoints[i], distance[i])

        if point not in npd:
            property = NPDProperty()
            npd[point] = property
        
        npd[point].connected.append(trial)

    for key, value in npd.iteritems():
        print key
        print value.connected
        print value.standard_deviation()

    sheet = []
    for key, value in npd.iteritems():
        sheet.append([key[0], key[1], value.mean()])
    columns = []
    for column in zip(*sheet):
        columns.append(np.array([item for item in column]))


    return columns

def read_csv(filename):
    """
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # assumes a header
        sheet = [row for row in reader]
        
    return sheet

def read_directory(directoryName):
    
    merged = []
    for subdir, dirs, files in os.walk(directoryName):
        for file in files:
            if file.endswith(".csv"):
                filePath = directoryName +'/'+ file
                merged += read_csv(filePath)
    
    return merged





# def show(fig):
#     """
#     Due to avoiding pyplot, we must handle all the backend calls...
#     """
#     master = tk.Tk()
#     canvas = FigureCanvasTkAgg(fig, master = master)
#     NavigationToolbar2TkAgg(canvas, master)
#     canvas.get_tk_widget().pack()
#     canvas.draw()
#     master.mainloop()

def add_title(ax, title, subtitle, trials):
    string = title+"\n"\
            "Number of Trials: "+trials+"\n"\
            r"\verb|"+subtitle+"|"
    print string
    ax.set_title(string, fontdict = {'fontsize':20})

import matplotlib.pyplot as plt
def plot_data(x, y, title, subtitle, xtitle, ytitle, threshold = False):
    """
    input: x axis, y axis
    where the index of each is a point
    creates a scatter plot
    """
    plt.rc('text', usetex=True)
    plt.rc('font', family = 'sans-serif: Computer Modern Sans serif')
    fig, ax = plt.subplots(2, sharex=True, sharey=True, facecolor = "white")
    for sub in ax:
        sub.set_xlim(0, max(x))
        sub.set_ylim(0, max(y))
        sub.set_aspect('auto')

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
    
    add_title(ax[0], title, subtitle, str(len(x)))
    if threshold:
        for sub in ax:
            function = lambda n: ((np.log(n)+threshold[0])/ \
                    (threshold[1]*n))**(1.0/threshold[2])
            add_threshold(sub, x, threshold, function)

#     fig.tight_layout()

    plt.show()
    
def process_totally_connected((numPoints, distance, connectedComponents), dataSetName, prompt):
    totallyConnected = [[],[]]
    for i in range(len(connectedComponents)):
        if connectedComponents[i] == 1 and \
                numPoints[i] > 50:
            totallyConnected[0].append(numPoints[i])
            totallyConnected[1].append(distance[i])
    



    image = zip(totallyConnected[0], totallyConnected[1])
    import itertools
    import operator
    totallyConnectedEdge = []
    def getx(point): return point[0]
    for x, g in itertools.groupby(sorted(image, key = getx), key = getx):
        totallyConnectedEdge.append(min(g, key = operator.itemgetter(1)))
    totallyConnectedEdge = zip(*totallyConnectedEdge)




    from scipy.optimize import curve_fit
    dimension = input("enter the dimension: ")
    def func(n, c, omega): 
        return ((np.log(n)+c)/(omega*n))**(1.0/dimension)

    (cOptimized, omegaOptimized), pcov = curve_fit(func, 
            totallyConnectedEdge[0], 
            totallyConnectedEdge[1])
    print cOptimized, omegaOptimized
    

    c, omega = cOptimized, omegaOptimized
    plot_data(x = totallyConnected[0], 
            y = totallyConnected[1], 
            title = "Completely Connected Components",
            subtitle = prompt,
            xtitle = dataSetName[0],
            ytitle = dataSetName[1],
            threshold = (c, omega, dimension)
            )





def add_threshold(ax, x, threshold, formula):

    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')
    textstr = "Complete Threshold = "\
            r'$\displaystyle{\left({\frac{\ln n \cdot + %.2f}{%.2f \cdot n}}\right)'\
            r'^{\frac{1}{%d}}}$' % threshold
    # place a text box in upper left in axes coords
    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
#     ax.text(0.1, 0.35, textstr, transform=ax.transAxes, fontsize=20,
#             verticalalignment='top', bbox = props)
    x = np.array(range(min(x), max(x)))
    f = formula(x) 
    ax.plot(x, f, '-', linewidth = 4, color = 'black', label = textstr)
    ax.legend(loc='lower left', fontsize= 'x-large', borderpad = 1)

def scatter(ax, x, y, title, subtitle, xtitle, ytitle):
    ax.plot(x, y, 'o', color = "#ff6666")
#     ax.set_title(title+"\n"+subtitle+" Number of Trials: "+str(len(x)))
#     ax.set_title(r"\text{"+title+
#             "\n"+subtitle+" Number of Trials: "+str(len(x))+"}")
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)


def heat_map(ax, x, y, title, subtitle, xtitle, ytitle):

# Calculate the point density
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    

    ax.scatter(x, y, c=z, s=100, edgecolor='')
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)


from mpl_toolkits.mplot3d import Axes3D
from textwrap import dedent

def min_and_max(iterable, index = 0):
    min_value, max_value = None, None
    for value in iterable:
        if value[index] < min_value[index]:
            min_value = value
        if value[index] > max_value[index]:
            max_value = value
    return min_value, max_value

import scipy.spatial
def plot3d(x, y, z, title, subtitle, xtitle, ytitle, ztitle):
    """
    We let x be the number of points,
    y be the distance,
    and z be the connected components
    """
    connected = []
    totallyConnected = []
    for i in range(len(z)):
        if z[i] == 1:
            totallyConnected.append((x[i], y[i], z[i]))
        else:
            connected.append((x[i], y[i], z[i]))

    fig = plt.figure()
    ax = Axes3D(fig)

    if connected:
        connected = zip(*connected)
        textstr = "not a completely connected graph: %d"\
                % (len(z) - len(totallyConnected))
        ax.scatter(connected[0], 
                connected[1], 
                connected[2], 
                marker = 'o', 
                color = '#3399ff',
                label = textstr)

    if totallyConnected:
        totallyConnected = zip(*totallyConnected)
        textstr = "a completely connected graph: %d"\
                % len(totallyConnected[0])
        ax.scatter(totallyConnected[0], 
                totallyConnected[1], 
                totallyConnected[2],
                marker = 'o', 
                color = '#ff33ff',
                label = textstr)

    surf = ax.plot_trisurf(x, y, z, cmap=plt.cm.Dark2, linewidth = 0)



    ax.legend(loc='lower left', fontsize= 'x-large', borderpad = 1)

    plt.title(title+'\n'+subtitle)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_zlabel(ztitle)
    ax.elev = 30
    ax.axim = 25

    plt.show()



import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np



def mean(data):
    """
    input: list of numbers
    return: mean
    """
    return float(sum(data))/len(data)

def median(data):
    temp = data
    temp.sort()
    if len(data) % 2 == 0:
        mid = (len(data)/2)-1
        mid2 = len(data)/2
        return (data[mid] + data[mid2])/2
    else:
        mid = len(data)/2
        return data[mid]

def mode(data):
    d = {}
    for value in data:
        value = int(value)
        if value not in d:
            d[value] = 0
        else:
            d[value] =  d[value] + 1
    return d

def varience(data):

    meanVal = mean(data)
    diff = [] # difference from mean
    for value in data:
        diff.append(value-meanVal)

    squaredDiff = []
    for d in diff:
        squaredDiff.append(d**2)
    sumSquaredDiff = sum(squaredDiff)
    variance = float(sumSquaredDiff)/len(data)
    return variance


def standard_deviation(data):
    return np.sqrt(varience(data))





class NPDProperty:
    """
    Number of Points vs Distance Properties
    """
    
    def __init__(self):
        self.connected = []
        
    def mean(self):
        return mean(self.connected)

    def standard_deviation(self):
        return standard_deviation(self.connected)



import sys
def main():
    if(1 < len(sys.argv)):
        prompt = sys.argv[1]
    else:
        prompt = raw_input("Enter a filename or directory: ")

    
    dataSet = read(prompt)
    numPoints, distance, connectedComponents = dataSet

    dataSetName = ["Number of Points", 
            "Distance Between Points", 
            "Connected Components"]



    if True:
#        plot3d(numPoints, distance, connectedComponents,
#                "All Data in One Graph",
#                prompt,
#                dataSetName[0], dataSetName[1], dataSetName[2])

        plot_data(numPoints,
                connectedComponents,
                "Points and Number of Components",
                prompt,
                dataSetName[0],
                dataSetName[2]
                )
        plot_data(distance,
                connectedComponents,
                "Distance and Number of Components",
                prompt,
                dataSetName[1],
                dataSetName[2]
                )


    process_totally_connected(dataSet, dataSetName, prompt)


    def manual_fit():
        while(True):
            comega = raw_input("enter c and \omega (seperated by a space): ")
            c, omega = [float(number) for number in comega.split(' ')]

            plot_data(x = totallyConnected[0], 
                    y = totallyConnected[1], 
                    title = "Totally Connected Components",
                    subtitle = prompt,
                    xtitle = dataSetName[0],
                    ytitle = dataSetName[1],
                    threshold = (c, omega, dimension)
                    )

if __name__ == "__main__": main()
