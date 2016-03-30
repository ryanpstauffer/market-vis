# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market-vis test code v.001
Market Visualization Prototype
This will eventually be divided into modules (with this main module being the glue)
"""

import numpy as np
from mayavi import mlab
import datetime
import pandas as pd

#from optimization import *
from data import connect_MySQL, get_returns, new_total_returns
from viz import picker_callback

#dphi, dtheta = np.pi/250.0, np.pi/250.0
#[phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi,0:2*np.pi+dtheta*1.5:dtheta]
#m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
#r = np.sin(m0*phi)**m1 + np.cos(m2*phi)**m3 + np.sin(m4*theta)**m5 + np.cos(m6*theta)**m7
#x = r*np.sin(phi)*np.cos(theta)
#y = r*np.cos(phi)
#z = r*np.sin(phi)*np.sin(theta)
#
#s = mlab.mesh(x, y, z)
#mlab.show()


timer = datetime.datetime.now()
print('Assembling Market Data')
startdate = datetime.datetime.strptime('20100102', '%Y%m%d')
enddate = datetime.datetime.strptime('20110102', '%Y%m%d')

#Pull Data from SQL database
print("Pulling Market Data from MySQL")
con = connect_MySQL()
stock_rets = get_returns(startdate, enddate)
stock_list = list(set(stock_rets.index))
print('Pulled data for %s stocks' % len(stock_list))

dates = list(set(stock_rets.price_date))
dates.sort()

#x = np.array([list(xrange(len(dates)+1)),]*len(stock_list)).transpose()
#y = np.array([stocks,]*(len(dates)+1))

#ret_matrix = pd.DataFrame()
##ret_matrix = np.zeros(((len(dates)+1),len(stock_list)))
#for s in xrange(len(stock_list)):
#    print(s)
#    ticker = (stock_list[s])
#    print(ticker)
#    rets = get_specific_returns(ticker, startdate, enddate, con)
#    rets.rename(columns={'return':ticker}, inplace=True)
#    print rets.index
#    ret_matrix = pd.concat((ret_matrix, rets), axis=1)
##    print(rets)
#print(ret_matrix)
#
#x_length, y_length = ret_matrix.shape
#x = np.array([list(xrange(x_length)),]*y_length).transpose()
#y = np.array([ret_matrix.columns,]*y_length)
#z = ret_matrix

#x, y, z = total_returns_chart(stock_rets)
x, y, z = new_total_returns(stock_list, startdate, enddate, con)
dims = x.shape
fig = mlab.figure(1)
vis = mlab.surf(x, y, z, warp_scale='auto')
mlab.outline(vis)
mlab.orientation_axes(vis)
mlab.title('Nasdaq 100 Market Data Visualization', size = .25)
mlab.axes(vis, xlabel = 'Time', ylabel = 'Company', zlabel = 'Value (Starting from 100)')
#    cursor3d = mlab.points3d(0., 0., 0., mode='axes',
#                                color=(0, 0, 0),
#                                scale_factor=20)
#picker = fig.on_mouse_pick(picker_callback)
print('Total time: ', (datetime.datetime.now() - timer))
#mlab.show()

print('End')
    