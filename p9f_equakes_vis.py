'''
Author: Derek Martin
Assignment: CIS 210 Winter 2018-19 Final Project Earthquake Visualizer
Credits: N/A
Description: Use file processing and data mining to discover patterns of earthquake activity around the world
over the past year; plot results on a world map.
'''
import math, random, turtle, doctest

def readFile(filename):
    '''
    (string) -> dictionary

    Read the equakes file and pull the latitude, longitude, and magnitude values into dictionaries with corresponding keys.

    > readFile("shortlist.txt")
    ({1: [44.8263333333333, -123.786833333333], 2: [42.0223333, -124.2715], 3: [45.6766667, -122.8965]},
    {1: [2.53], 2: [2.99], 3: [2.56]})
    '''
    equakeFile = open(filename, "r")
    equakeDict = {}
    magDict = {}
    key = 0
    
    for line in equakeFile:
        quake = line.split(',') # Separate the data points from each equake
        if key != 0: # Ignore header in equakes file
            equakeDict[key] = [float(quake[1]), float(quake[2])] # Add latitude and longitude to dictionary
            magDict[key] = [float(quake[4])] # Add magnitudes to magDict
        key += 1
    return equakeDict, magDict

def euclidD(point1, point2):
    '''
    (number sequence), (number sequence) -> float

    Calculate and return the approximate distance between two points in a multi-dimensional plane.

    >>> euclidD((5, 19), (17, 4))
    19.209372712298546
    
    >>> euclidD([5, 2], [6, 4])
    2.23606797749979
    '''
    total = 0
    for index in range(len(point1)):
        diff = (point1[index] - point2[index]) ** 2 # Square the difference to eliminate negative values
        total = total + diff

    euclidDistance = math.sqrt(total) # Calculate the square root to approximate the distance
    return euclidDistance

def createCentroids(k, equakeDict):
    '''
    (int), (dict) -> list

    Calculate unique random values for centroids 'k' number of times.

    > createCentroids(4, readFile("shortlist.txt")[0])
    [[44.8213333, -122.2221667], [44.613, -124.3475], [44.4363, -126.0199], [44.228, -125.4033]]
    '''
    centroids = []
    centroidCount = 0
    centroidKeys = []

    while centroidCount < k:
        rkey = random.randint(1,len(equakeDict))
        if rkey not in centroidKeys: # Eliminate duplicate centroids
            centroids.append(equakeDict[rkey])
            centroidKeys.append(rkey) # Store the keys of each centroid for easy access
            centroidCount += 1
    return centroids

def createClusters(k, centroids, equakeDict, repeats):
    '''
    (int), (list), (dict), (int) -> list

    Create and return clusters by comparing items in 'equakeDict' to given centroids.

    **NOTE: 'k' must be == to 'k' from createCentroids() argument.

    > createClusters(4, createCentroids(4, readFile("shortlist.txt")[0]), readFile("shortlist.txt")[0], 3)
    **** PASS 0 ****
    **** PASS 1 ****
    **** PASS 2 ****
    [[2, 5, 7, 8, 9, 10, 12, 14], [1, 4, 13], [3, 11], [6]]

    **NOTE: This mockup function call example happens to avoid using initialized variables as arguments
    '''
    for apass in range(repeats):
        print("**** PASS", apass, "****")
        clusters = []
        for i in range(k):
            clusters.append([]) # Create a list of 'k' empty clusters

        for akey in equakeDict:
            distances = []
            for clusterIndex in range(k):
                dist = euclidD(equakeDict[akey], centroids[clusterIndex]) # Calculate distance between each dictionary item and each centroid
                distances.append(dist) # Store distances in a list

            mindist = min(distances) # Find closest centroid to dictionary item's value
            index = distances.index(mindist)

            clusters[index].append(akey) # Append the dictionary value's key to the proper cluster

        dimensions = len(equakeDict[1])
        for clusterIndex in range(k):
            sums = [0] * dimensions
            for akey in clusters[clusterIndex]:
                datapoints = equakeDict[akey]
                for ind in range(len(datapoints)):
                    sums[ind] = sums[ind] + datapoints[ind] # Calculate running sums of each dimension in data set
            for ind in range(len(sums)):
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:
                    sums[ind] = sums[ind] / clusterLen # Compute mean value of each dimension in data set to recalculate centroids

            centroids[clusterIndex] = sums # Reassigns values to centroid list
        '''
        for c in clusters:
            print ("CLUSTER")
            for key in c:
                print(equakeDict[key], end="  ")
            print()
        '''
    return clusters

def visualizeQuakes(k, r, dataFile):
    '''
    (int), (int), (str) -> None

    Call readFile(), createCentroids(), createClusters(), and eqDraw() to plot the equakes onto the world map based on coordinates.

    > visualizeQuakes(6, 7, "earthquakes.csv")
    **** PASS 0 ****
    **** PASS 1 ****
    **** PASS 2 ****
    **** PASS 3 ****
    **** PASS 4 ****
    **** PASS 5 ****
    **** PASS 6 ****
    (Turtle Graphics simulation)
    '''
    datadict = readFile(dataFile) # Call readFile() and assign value to variable
    quakeCentroids = createCentroids(k, datadict[0]) # Call createCentroids() and assign value to variable
    clusters = createClusters(k, quakeCentroids, datadict[0], r) # Call createClusters() and assign value to variable
    eqDraw(k, datadict, clusters) # Call eqDraw()
    return None

def eqDraw(k, eqDict, eqClusters):
    '''
    (int), (dict), (list) -> None

    Use Turtle Graphics to plot each equake onto the world map using unique colors for each cluster.

    > eqDraw(6, readFile("shortlist.txt"), createClusters(6, createCentroids(6, readFile("shortlist.txt")[0]), readFile("shortlist.txt")[0], 7))
    **** PASS 0 ****
    **** PASS 1 ****
    **** PASS 2 ****
    **** PASS 3 ****
    **** PASS 4 ****
    **** PASS 5 ****
    **** PASS 6 ****
    (Turtle Graphics simulation)

    **NOTE: This mockup function call example happens to avoid using initialized variables as arguments
    '''
    quakeT = turtle.Turtle() # Create a turtle
    quakeT.speed('fastest')
    quakeWin = turtle.Screen()
    quakeWin.bgpic("worldmap1800_900.gif")
    quakeWin.screensize(1800,900) # Set width and height of drawing window

    wFactor = (quakeWin.screensize()[0] / 2) / 180
    hFactor = (quakeWin.screensize()[1] / 2) / 90

    quakeT.hideturtle()
    quakeT.up()

    colorlist = ["red","green","blue","orange","cyan","yellow"]

    for clusterIndex in range(k):
        quakeT.color(colorlist[clusterIndex]) # Create list of colors
        for akey in eqClusters[clusterIndex]:
            lat = eqDict[0][akey][0] # Extract latitude
            lon = eqDict[0][akey][1] # Extract longitude
            mag = eqDict[1][akey][0] # Extract magnitude
            quakeT.goto(lon*wFactor,lat*hFactor)
            quakeT.pensize(mag) # Set pensize to magnitude value
            quakeT.dot() # Plot dots onto world map
    quakeWin.exitonclick()
    return None

def main():
    ''' Main function that calls visualizeQuakes() '''
    k = 6
    r = 7
    f = "earthquakes.csv"
    visualizeQuakes(k, r, f)
    return None

main()
