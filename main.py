# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market-vis test code v0.01
Market Visualization Prototype
This will eventually be divided into modules (with this main module being the glue)
"""

import numpy as np
from mayavi import mlab
from datetime import datetime
import pandas as pd

from quotes import buildDailyPriceData, buildDummyData, createIndexedPricing
#from optimization import *

from visualization import visualizePrices

#Assemble Test Data for temp use
t0 = datetime.now()
    
#Select Dates  
startDate = datetime.strptime('20120101', '%Y%m%d')
endDate = datetime.strptime('20130101', '%Y%m%d')

#Get data for S&P500 Constituents
print('Pulling Market Data for S&P 500 from {0} to {1}'.format(startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))
SP500Constituents = pd.read_csv('SP500_constituents.csv')

#df = buildDailyPriceData(SP500Constituents['Symbol'])


###Load dataset from .csv
#print("Pulling Market Data from .csv")
#df = pd.read_csv('SP500_daily_price_data.csv')
#
## Convert strings to Datetime format
#df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
#df.index = df[df.columns[0]]
#df.drop(df.columns[0], axis=1, inplace=True)
#
##Build Price Table
#stockPrices = df.loc[startDate:endDate]
##FIX THIS
##SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
#stockPrices.dropna(axis=1, how='any', inplace=True)
#
#stockList = list(set(stockPrices.columns))
#print('Pulled data for {0} stocks from {1} to {2}'.format(len(stockList), startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))

stockPrices = buildDummyData()

indexedPrices = createIndexedPricing(stockPrices, 100)

visualizePrices(indexedPrices)

print('Total time: ', (datetime.now() - t0))
print('End')
    