# -*- coding: utf-8 -*-

"""
Created on Sun Jul 29 23:20:28 2018
@author: sguenov
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr
import math
import csv
import random

# File format:

# a b c d e f g h i

# x = a * data1 + d

# y = b * data1 + e

# z = h * x + i * y + c * data1 + f

class cluster:
    # init with two arrays
    # vars is empty
    # unused is 1 x 12 array of ints 0 - 11 
    def __init__(self):
        self.vars = []
        self.unused = [0,1,2,3,4,5,6,7,8,9,10,11]
        #random.shuffle(self.unused)

    # input array vals and dist
    def makeFunction(self, vals, dist):
        coeffs = []
        print(self.unused)

        # convert list of string numbers to ints
        for var in vals:
            coeffs.append(int(var))
            print(int(var))

        # should be length 12
        # testing for errors
        if (len(coeffs) != 13):
            print("WTF")
            return

        #randos = []
        print(coeffs)
        self.threeVars(coeffs, dist, self.unused[0], self.unused[1], self.unused[2])

#        for i in range(2):
#        #randos.append(self.genRan(dist))
#            print(dist)
#            print(coeffs[i])
#            print(coeffs[i+3])
#            self.vars.insert(self.unused[i],(coeffs[i]*self.genRan(dist) + coeffs[i+3]))
#        self.vars.insert(self.unused[2],((coeffs[7] * self.vars[0] + coeffs[8] * self.vars[1]) + coeffs[5] + coeffs[2] * self.genRan(dist))) 

        # ideal result, so we update vars
        # dont know what this math is
        if coeffs[0] !=0 and coeffs[1] !=0:
            print("as expected")
            self.vars.insert(self.unused[3],(np.absolute(coeffs[9] * self.vars[0]/coeffs[0]/50 + coeffs[10] * self.vars[1]/coeffs[1]/50)))
        else:
            self.vars.append(np.absolute(self.vars[0]/50 + coeffs[6]*self.genRan("gaussian")))

        self.vars.insert(self.unused[4],(coeffs[11]*self.vars[0]/50 + coeffs[12]* self.vars[1]/50))
        self.addCol(self.unused[5])
        self.addCol(self.unused[6])
        self.threeVars(coeffs, dist, self.unused[7], self.unused[8], self.unused[9])

    # input lists vals and dist and three variables (p1 - p3)
    # updates self.vars with z variable as shown above
    def threeVars(self, vals, dist, p1, p2, p3):
        coeffs = vals
        for i in range(2):
        #randos.append(self.genRan(dist))
            print(dist)
            print(coeffs[i])
            print(coeffs[i+3])
            self.vars.insert(self.unused[i],(coeffs[i]*self.genRan(dist) + coeffs[i+3]))

        # seems to take the form of z variable above
        self.vars.insert(self.unused[2],((coeffs[7] * self.vars[0] + coeffs[8] * self.vars[1]) + coeffs[5] + coeffs[2] * self.genRan(dist))) 
        print("making three connected vars")

    # checks to see if string is in dist
    # outputs accordingly
    def genRan(self, dist):
        if("gauss" in dist.lower()):
            return np.random.normal(0, 1, 1000)
        if("lor" in dist.lower()):
            return np.random.standard_cauchy(1000)
        if("power" in dist.lower()):
            return np.random.power(5, 1000)
        if("asym" in dist.lower()):
            return np.random.power(math.exp(1), 1000)
        if("gam" in dist.lower()):
            return np.random.gamma(2, 2, 1000)
        else:
            print("unknown")

    # gets the value at position var in vars
    def getVar(self, var):
        return self.vars[var]

    # adds noise to vars
    # unknown scaling
    def makeNoise(self):
        self.vars.append(180*self.genRan("gauss"))
        self.vars.append(180*self.genRan("gauss"))
        self.vars.append(180*self.genRan("gauss"))
        self.vars.append(5*self.genRan("gauss"))

    # add noise to list num
    def addNoise(self, num, place = 0):
        for i in range(num):
            self.vars.append(180*self.genRan("gauss"))

    # adds a noise value at the beginning of vars
    def addCol(self, place = 0):
        self.vars.insert(place,(180*self.genRan("gauss")))

    # just prints a line
    def addCSV(self):
        print("adding from csv")

# graph class for creating figures
class graph:

    # creates a set of graphs: 2D, 3D, Histogram
    def graphSets(self, clusters, color):
        print("graph set")
        self.twoDGraphs(clusters, color)
        self.threeDGraph(clusters,color)
        self.histogram(clusters, color)
    
    # Creates a 2D scatter plot
    def twoDGraphs(self, cluster, color):
        colors = ['b', 'g', 'r', 'k', 'y', 'm','c']
        for j in range(len(cluster)):
            #factor = 5/(total/len(cluster[j].getVar(3)))
            factor = 1
            for i in range(3):
                plt.figure(i)
                if i == 2:
                    x = 0
                    y = 2
                else:
                    x = i
                    y = i + 1

                if(color):
                    index = 0
                    for k in cluster[j].getVar(3):
                        plt.plot(cluster[j].getVar(x)[index],cluster[j].getVar(y)[index],linestyle = 'None', marker = '.', markersize = factor*k, c = colors[j])
                        index += 1

                else:
                    plt.plot(cluster[j].getVar(x),cluster[j].getVar(y),linestyle = 'None', marker = '.', c = 'k')
                #print(pearsonr(cluster[j].getVar(x), cluster[j].getVar(y)))
                axes = plt.gca()
                axes.set_xlim([-300,300])
                axes.set_ylim([-300,300])

    # Creates a 3d scatter plot
    def threeDGraph(self, clusters, color):
        fig = plt.figure(3)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('x Values')
        ax.set_ylabel('y Values')
        ax.set_zlabel('z Values')
        ax.set_xlim3d(-200, 200)
        ax.set_ylim3d(-200, 200)
        ax.set_zlim3d(-200, 200)
        for j in range(len(clusters)):
            if(color):
                #for i in clusters[j].getVar(3):
                ax.scatter(clusters[j].getVar(0), clusters[j].getVar(1), clusters[j].getVar(2), s= 0.5)
            else:
                ax.scatter(clusters[j].getVar(0), clusters[j].getVar(1), clusters[j].getVar(2), s= 0.5,c='k')

    # creates a histogram of frequencies
    def histogram(self, clusters, color):
        for j in range(len(clusters)):
            if(color):
                for i in range(0,3):
                    plt.figure(i+4)
                    plt.hist(clusters[j].getVar(i), range = (-40,40)) 
            else:
                for i in range(0,3):
                    plt.figure(i+4)
                    plt.hist(clusters[j].getVar(i), bins = 20, color = 'k') 

# Class with one function that saves cluster data to filename.csv
class saver:
    def saveAsCSV(self, clusters, filename):
        with open('obscured5.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\n', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(clusters)):
                print("Saving")
                for j in range(1000):
                    spamwriter.writerow([i+1, (i+1)*1000 +j, \
                                         clusters[i].getVar(0)[j],\
                                         clusters[i].getVar(1)[j],\
                                         clusters[i].getVar(2)[j],\
                                         clusters[i].getVar(3)[j],\
                                         clusters[i].getVar(4)[j],\
                                         clusters[i].getVar(5)[j],\
                                         clusters[i].getVar(6)[j],\
                                         clusters[i].getVar(7)[j],\
                                         clusters[i].getVar(8)[j],\
                                         clusters[i].getVar(9)[j]])

# main function
if __name__ == '__main__':
    # creates graph
    g = graph()
    print("begin")

    # inits variables to use
    cos = []
    types = []
    clusters = []

    # Possibility to read from file
    mode = input("Read from file (y/n)")

    # read in information
    if mode == 'y':
        mode = input("Read CSV or instructions?")

        # instructions from ins.txt
        if "i" in mode:
            fn = "ins.txt"
            f = open(fn, "r")
            ins = f.readlines()
            num = int(len(ins)/2)
            print(num)
            # break up instructions and add to cos and types
            for i in range(num):
                print("Rip me")
                co = ins[2*i].split()
                print(co)
                cos.append(co)
                typ = ins[2*i+1]
                print(typ)
                types.append(typ)
            color = ins[len(ins) - 1]
            print(cos)

        # reads in data from a file
        elif "c" in mode:
            fn = "C:/Users/sguen/Desktop/data.csv"
            f = open(fn, "r")
            ins = f.readlines()
            num = int(len(ins)/2)
            print(num)

    # otherwise generate new data
    else:
        num = input("How many clusters would you like to plot")
        print("For each cluster, type the coeffients in a single line")
        for i in range(int(num)):
            co = str(input("Input Coeffients for cluster")).split()
            cos.append(co)
            typ = str(input("Distribution of cluster"))
            types.append(typ)
        color = str(input("Plot clusters in color? (y/n)"))

    # color or not
    if color == 'y':
        col = True
    else:
        col = False

    # make the clusters
    for i in range(int(num)):
        c = cluster()
        c.makeFunction(cos[i], types[i])
        #c.addNoise(2)
        clusters.append(c)

    # not sure what this is fore
    c = cluster()
    #c.makeNoise()
    #clusters.append(c)

    # make the set of graphs with the clusters
    g.graphSets(clusters, col)
    plt.show()

    # save data as output or not
    save = str(input("Would you like to save data as CSV"))
    if(save == 'y'):
        s = saver()
        s.saveAsCSV(clusters, "way_even_moar_data.csv")
        print("lol no i cant save")

    # close plots and exit
    cmd = str(input("Press q to close"))
    if(cmd == 'q'):
        for i in range(7):
            plt.close()
