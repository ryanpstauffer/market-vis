# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Tue Feb 10 18:27:17 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market Visualization Prototype 
Visualization and Interactive module
"""

import numpy as np
import moviepy.editor as mpy

def visualizePrices(prices):
    '''Creates a mayavi visualization of a pd DataFrame containing stock prices
    Inputs:
    prices => a pd DataFrame, w/ index: dates; columns: company names
    '''
    #Imports mlab here to delay starting of mayavi engine until necessary
    from mayavi import mlab
    
    #Because of current mayavi requirements, replaces dates and company names with integers
    x_length, y_length = prices.shape
    xTime = np.array([list(xrange(x_length)),] * y_length).transpose()
    yCompanies = np.array([list(xrange(y_length)),] * x_length)
    
    #Sort indexed prices by total return on last date
    lastDatePrices = prices.iloc[-1]
    lastDatePrices.sort_values(inplace=True)
    sortOrder = lastDatePrices.index
    zPrices = prices[sortOrder]
    
    #Create mayavi2 object
    fig = mlab.figure(bgcolor=(.4,.4,.4))
    vis = mlab.surf(xTime, yCompanies, zPrices)
    mlab.outline(vis)
    mlab.orientation_axes(vis)
    #mlab.title('S&P 500 Market Data Visualization', size = .25)
    mlab.axes(vis, nb_labels=0, xlabel = 'Time', ylabel = 'Company', zlabel = 'Price')
    
    mlab.show()

def make_frame(t):
    mlab.view(elevation=70, azimuth=360*t/4.0, distance=1400) #Camera angle
    return mlab.screenshot(antialiased=True)

def animateGIF(filename, prices):
    '''Creates a mayavi visualization of a pd DataFrame containing stock prices
    Then uses MoviePy to animate and save as a gif
    Inputs:
    prices => a pd DataFrame, w/ index: dates; columns: company names
    '''
     #Imports mlab here to delay starting of mayavi engine until necessary
    from mayavi import mlab
    
    #Because of mayavi requirements, replace dates and company names with integers
    #until workaround is figured out
    x_length, y_length = prices.shape
    xTime = np.array([list(xrange(x_length)),] * y_length).transpose()
    yCompanies = np.array([list(xrange(y_length)),] * x_length)
    
    #Sort indexed prices by total return on last date
    lastDatePrices = prices.iloc[-1]
    lastDatePrices.sort_values(inplace=True)
    sortOrder = lastDatePrices.index
    zPrices = prices[sortOrder]
    
    #Create mayavi2 object
    fig = mlab.figure(bgcolor=(.4,.4,.4))
    vis = mlab.surf(xTime, yCompanies, zPrices)
    mlab.outline(vis)
    mlab.orientation_axes(vis)
    mlab.axes(vis, nb_labels=0, xlabel = 'Time', ylabel = 'Company', zlabel = 'Price')
    
    animation = mpy.VideoClip(make_frame, duration = 4).resize(1.0)
    animation.write_gif(filename, fps=20)
    