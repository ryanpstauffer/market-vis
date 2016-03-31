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
from datetime import datetime, date
import pandas as pd

#from optimization import *

#from viz import picker_callback

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

#Assemble Test Data for temp use
timer = datetime.now()
    
#Select Dates for backtesting period    
startDate = datetime.strptime('20120101', '%Y%m%d')
endDate = datetime.strptime('20130101', '%Y%m%d')

#Load dataset from .csv
print("Pulling Market Data from .csv")
df = pd.read_csv('SP500_daily_price_data.csv')

# Convert strings to Datetime format
df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df.index = df[df.columns[0]]
df.drop(df.columns[0], axis=1, inplace=True)

#Build Price Table
stockPrices = df.loc[startDate:endDate]
#FIX THIS
#SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
stockPrices.dropna(axis=1, how='any', inplace=True)
print(stockPrices.head())

stockList = list(set(stockPrices.columns))
print('Pulled data for {0} stocks from {1} to {2}'.format(len(stockList), startDate, endDate))

#Build Returns Table
stockReturns = stockPrices.pct_change(1)
print(stockReturns.head())


#Build Indexed Price Table
indexedReturns = stockReturns + 1
indexedReturns.iloc[0] = np.repeat(1, len(stockReturns.columns))
indexedReturns = indexedReturns.cumprod(axis=0)
print(indexedReturns.head())




dates = list(set(stockReturns.index))
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

#Begin Good code here?
#x, y, z = new_total_returns(stockList, startDate, endDate, con)

ret_matrix = stockReturns
x_length, y_length = ret_matrix.shape
x = np.array([list(xrange(x_length)),]*y_length).transpose()
y = np.array([list(xrange(y_length)),]*x_length)

tot_ret_matrix = ret_matrix + 1
tot_ret_matrix.iloc[0] = 100
z = tot_ret_matrix.cumprod(axis=0)


#sort z by total return
last_date = z.iloc[-1]
last_date.sort_values(inplace=True)
sort_order = last_date.index
z = z[sort_order]

print(z.tail())

#Real code
dims = x.shape
fig = mlab.figure(1)
vis = mlab.surf(x, y, z, warp_scale='auto')
mlab.outline(vis)
mlab.orientation_axes(vis)
mlab.title('S&P 500 Market Data Visualization', size = .25)
mlab.axes(vis, xlabel = 'Time', ylabel = 'Company', zlabel = 'Value (Starting from 100)')
#    cursor3d = mlab.points3d(0., 0., 0., mode='axes',
#                                color=(0, 0, 0),
#                                scale_factor=20)
#picker = fig.on_mouse_pick(picker_callback)


##Test code
#dphi, dtheta = np.pi/250.0, np.pi/250.0
#[phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi,0:2*np.pi+dtheta*1.5:dtheta]
#m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
#r = np.sin(m0*phi)**m1 + np.cos(m2*phi)**m3 + np.sin(m4*theta)**m5 + np.cos(m6*theta)**m7
#x = r*np.sin(phi)*np.cos(theta)
#y = r*np.cos(phi)
#z = r*np.sin(phi)*np.sin(theta)
#
#s = mlab.surf(x, y, z)#, warp_scale='auto')



print('Total time: ', (datetime.now() - timer))
mlab.show()

print('End')
    