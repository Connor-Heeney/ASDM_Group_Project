import csv
import pandas as pd
import numpy as np
from pyproj import Proj, transform
from matplotlib import pyplot as plt


def clean_data(row):
    # remove trailing commas, whitespace
    # cleaned_row = row.rstrip()
    # Add commas in between coords
    cleaned_row = row.replace('""', "")
    return cleaned_row


def readData(filename):
    """Read data and split on ,

    Args:
        filename (_type_): text file

    Returns:
        data _type_: dataframe
    """
    data = pd.read_csv(filename, sep=",", header=None)
    return data


def reprojectData(lon, lat, outEPSG):
    # set projections
    inProj = Proj("epsg:4326")
    outProj = Proj("epsg:" + str(outEPSG))
    # reproject data
    x, y = transform(inProj, outProj, lat, lon)
    return (x, y)


class dougPeuk(object):
    """A class to hold data and run a Douglas Peucker Algorithm"""

    def __init__(self):
        """Class initialiser"""
        # global variables across all functions?
        # self.numb=numb
        # self.arr=np.random.random((numb))

    def readData1(self, filename):
        """Reads data into dataframe, and converts coordinates into British National Grid

        Args:
            filepath: location and name of data file

        Returns:
            sortedData (dataframe): Dataframe with projected coordinate values
        """
        self.data = pd.read_csv(filename, sep=",")
        print(self.data.columns)
        self.data["lat"], self.data["lon"] = reprojectData(
            self.data["lat"], self.data["lon"], 4326
        )
        return self.data

    def dataOutput(self, filepath, var1, var2):
        """_summary_

        Args:
            filepath (_type_): _description_
            generalised_lon (_type_): _description_
            generalised_lat (_type_): _description_
        """
        # Make variables into list of tuples
        self.combined_data = zip(var1, var2)

        # Write data to csv

        with open(filepath, "w", newline="") as self.outputfile:
            self.csv_writer = csv.writer(self.outputfile)

            # Add data headers
            self.csv_writer.writerow(["lon", "lat"])

            # Write data rows
            self.csv_writer.writerows(self.combined_data)

    def perp_dist(self, x1, x2, x3, y1, y2, y3):
        """
        This function returns the perpendicular distance from a point to a line segment.

        (x1,y1) and (x2,y2) define the start and end points of your line.
        (x3, y3) defines a point.
        """
        if x2 == x1:
            return abs(x3 - x1)
        self.m = (y2 - y1) / (x2 - x1)
        self.c = y1 - self.m * x1
        self.d = abs(self.m * x3 - y3 + self.c) / (self.m**2 + 1) ** 0.5
        return self.d

    def recursePeuk(self, data, tol, start_i, end_i, nodes):
        """Recursive Douglas Peucker algorithm

        Args: SortedData: input data, ordered by time
            tol: Distance buffer
            start_i: index value of first value
            end_i: index value of last value
            nodes: list, starts with start and end data values only

        Returns:
          nodes: index of sortedData values which can be used as DP nodes
        """
        # Find values at start and end index positions
        self.start = data.iloc[start_i]
        self.end = data.iloc[end_i]

        # If less than 2 points left, end loop
        if (end_i - start_i) < 2:
            return -1

        # Empty list for perpendicular distance
        self.p_dis = []

        # Loop to find perpendicular distances for all values (X3, Y3)
        # Potential way to do with np methods - faster?
        for self.index, self.row in data.iterrows():
            self.p_dis.append(
                self.perp_dist(
                    self.start["lat"],
                    self.end["lat"],
                    self.row["lat"],
                    self.start["lon"],
                    self.end["lon"],
                    self.row["lon"],
                )
            )

        # Set distance for everything from 0 to start or end, to 0
        # Makes sure distances you are not interested in are not max
        for self.i, self.value in enumerate(self.p_dis):
            if self.i < start_i:  # Left half of p_dis list becomes 0
                self.p_dis[self.i] = 0.0
            if self.i > end_i:  # Right half of p_dis list becomes 0
                self.p_dis[self.i] = 0.0

        # Find largest perp dist
        self.max_pdis = max(self.p_dis)
        # Index of largest perp dis
        self.max_pd_i = np.argmax(self.p_dis)

        # If max perp dis larger than tolerance, that point becomes new node
        if self.max_pdis > tol:
            nodes.append(self.max_pd_i)

            # function runs again, but with 2 separate arms
            # looking at points from start to new node
            self.recursePeuk(data, tol, start_i, self.max_pd_i, nodes)
            # looking at points from new node to end
            self.recursePeuk(data, tol, self.max_pd_i, end_i, nodes)

        # Output is list of indices, for points in node list
        return sorted(nodes)

    def runDP(self, tol):
        """Runs and plots the Douglas Peucker algorithm, and the squirrel movement
            Defines DP start, nodes outside of function, so they are not affected by recursion

        Args:
            tol (Float): Tolerated distance within which points generalised into line
        """
        # Define start and end index points for DP
        self.start = 0
        self.end = (len(self.data)) - 1

        # Nodes is list of index positions of points.
        # Start and end are retained regardless of tol
        # Nodes needs to be defined outside of function,
        # Otherwise new empty node list for each recurse
        self.nodes = [self.start, self.end]

        # DP function
        self.node = self.recursePeuk(self.data, tol, self.start, self.end, self.nodes)

        # Empty lists for attributes of node points
        self.generalised_lat = []
        self.generalised_lon = []
        self.generalised_time = []

        for self.nodes in self.node:
            # Fill lists with attributes of node pointsself.generalised_lat
            self.generalised_lat.append(self.data["lat"][self.nodes])
            self.generalised_lon.append(self.data["lon"][self.nodes])

        return self.generalised_lon, self.generalised_lat

    def plotDP(self):
        # Plot data
        plt.plot(self.data["lon"], self.data["lat"])
        plt.plot(self.generalised_lon, self.generalised_lat, color="red", alpha=0.5)
        plt.title("Douglas-Peucker line Generalisation")
        plt.show()


if __name__ == "__main__":

    regions = readData("data/region_data.csv")
    # Define object in dougPeuk class
    dougP1 = dougPeuk()

    # Read, run DP algorithm and plot squirrel movement
    dougP1.readData1("data/region_data.csv")
    lon, lat = dougP1.runDP(0.05)
    dougP1.plotDP()
    dougP1.dataOutput("data/region_gen.csv", lon, lat)

    # print(regions)
