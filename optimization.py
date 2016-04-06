# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Tue Feb 10 18:16:51 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market Visualization Prototype
Optimization and Algo module 
"""

import numpy as np
import random
import scipy.spatial.distance as scidist
from scipy.interpolate import UnivariateSpline
import scipy.stats as stats
import datetime
from data import *
import matplotlib.pyplot as plt

def Cities(n, seed=None):
    "Make a set of n cities, each with random coordinates."
    City = complex # Constructor for new cities, e.g. City(300, 400)
    if seed is not None: random.seed(seed)
    return list(City(random.randrange(10, 890), random.randrange(10, 590)) for c in range(n))

def Points(n, seed=None):
    if seed is not None: random.seed(seed)
    return list((random.randrange(0,20, _int=float),0) for c in range(n))

def new_algo(points):
    print(len(points))
    #Construct Euclidean distance matrix
    dist_matrix = scidist.cdist(points, points, 'euclidean')
    # eliminate self matching
    dist_matrix = dist_matrix + np.identity(len(points)) * dist_matrix.max()
#    print(dist_matrix)
#    print(dist_matrix.shape)
    shortest = (np.where(dist_matrix == np.min(dist_matrix)))
    ind1 = shortest[0][0]
    ind2 = shortest[0][1] 
#    print(points[ind1])
#    print(pt2)
#    points[]    
#    short_index = (np.where(dist_matrix == shortest))
#    print(shortest)
    
    #Construct Ordered List
    ordered_list = [points[ind1], points[ind2]]
    unused = points
    for p in ordered_list:
        unused.remove(p)

#    print ordered_list
#    print len(unused)
    
    while unused:
        #Iterate to find shortest distance as add them together.
        search_point = ordered_list[0]
        print(search_point)
        dist1 = [np.sqrt((p[0] - search_point[0])**2 + (p[1] - search_point[1])**2) for p in unused]
        ind1 = np.argmin(dist1)
        
        search_point = ordered_list[1]
        dist2 = [np.sqrt((p[0] - search_point[0])**2 + (p[1] - search_point[1])**2) for p in unused]
        if np.amin(dist2) >= dist1[ind1]:
            new_point = unused[ind1]
            ordered_list.insert(0, new_point)
        else: 
            new_point = unused[np.argmin(dist2)]
            ordered_list.append(0, new_point)
            
        unused.remove(new_point)
        
    print ordered_list
    print len(unused)

def plot_daily_ret(ret, ret2):
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_axes([0.05, 0.5, 0.9, 0.45])
    ax2 = fig.add_axes([0.05, 0.05, 0.9, 0.3])
    
    ax.set_title(date)
    ax.set_ylabel('Daily Return')
    ax.set_xlabel('Company')
    ax.plot(ret, color = 'b')
    ax.plot(ret2, color = 'g')
    ax.plot(points_x, points_y, color = 'r')
    ax.axhline(0, linestyle = '--', color = 'k')
    ax.axhline(np.mean(ret), linestyle = '--', color = 'g')
    
    ax2.set_xlim(ax.get_ylim())
    ax2.hist(ret, bins = np.floor(len(ret)/5), normed=True, alpha=0.6)
    mu, std = stats.norm.fit(ret)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    ax2.plot(x, p, 'k', linewidth=2)
    ax2.axvline(mu, linestyle = '--', color = 'g')
    ax2.axvline((mu+std), linestyle = '--', color = 'r')
    ax2.axvline((mu-std), linestyle = '--', color = 'r')
    title = "Fit results: mu = %.5f,  std = %.5f" % (mu, std)
    ax2.set_title(title)
    
def shoreline(curve):
    tot_dist = 0
    for i in xrange(len(curve)-1):
        point1 = (curve[i][1], curve[i][0])
        point2 = (curve[(i+1)][1], curve[(i+1)][0])
        part_dist = scidist.euclidean(point2, point1)
        tot_dist += part_dist
    return tot_dist

if __name__ == '__main__':
    t0 = datetime.datetime.now()

    print('Assembling Market Data')
    date = datetime.datetime.strptime('20100115', '%Y%m%d')
    
    x_scale_factor = 1000.0
    
    #Create 1-D array of returns (Index is ret labels)
    ret = np.array(stock_rets['return'])
    
    #Determine distance between all points in unordered list
    order = list(xrange(len(ret)))
    order = [x / x_scale_factor for x in order]
    ret_2D = np.array((ret,order)).T  
    A = shoreline(ret_2D)
        
    #Sort the returns in an increasing order, creating a monotonic increasing curve
    ret2 = sorted(ret)
 
    #determine distance between all points in monotonic list
    order = list(xrange(len(ret2)))
    order = [x / x_scale_factor for x in order]
    ret2_2D = np.array((ret2,order)).T  
    M = shoreline(ret2_2D)
        
    #Determine max and min points
    points_x = (0.,(len(ret)-1))
    points_y = (min(ret),max(ret))
    S = scidist.euclidean((order[-1],max(ret)), (0.,min(ret))) 
    
    #Plot straight line from min to max
    plot_daily_ret(ret, ret2)
    
    #A-M-S results
    print('A = %s, M = %s, S = %s' % (A, M, S))
    print('A/S = %s, A/M = %s, M/S = %s' % (A/S, A/M, M/S))

    print(datetime.datetime.now() - t0)