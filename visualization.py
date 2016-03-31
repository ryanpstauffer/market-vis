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
from mayavi import mlab
import datetime


def visualizePrices(prices):
    '''Creates a mayavi visualization of a pd DataFrame containing stock prices
    Inputs:
    prices => a pd DataFrame, w/ index: dates; columns: company names
    '''
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
    dims = xTime.shape
    fig = mlab.figure(bgcolor=(.4,.4,.4))
    vis = mlab.surf(xTime, yCompanies, zPrices, warp_scale='auto')
    mlab.outline(vis)
    mlab.orientation_axes(vis)
    #mlab.title('S&P 500 Market Data Visualization', size = .25)
    mlab.axes(vis, nb_labels=0, xlabel = 'Time', ylabel = 'Company', zlabel = 'Price')
    #    cursor3d = mlab.points3d(0., 0., 0., mode='axes',
    #                                color=(0, 0, 0),
    #                                scale_factor=20)
    #picker = fig.on_mouse_pick(picker_callback)
    
    mlab.show()


def pickerCallback(pickerObj):
    picked = pickerObj.actors
    if vis.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
        # m.mlab_source.points is the points array underlying the vtk
        # dataset. GetPointId return the index in this array.
        x_, y_ = np.lib.index_tricks.unravel_index(pickerObj.point_id,dims)
        print('Data indices: %i, %i' % (x_, y_))
        print(x[x_, y_], y[x_, y_], z[x_, y_] )
        cursor3d.mlab_source.set(x=x[x_, y_],
                                 y=y[x_, y_],
                                 z=z[x_, y_])