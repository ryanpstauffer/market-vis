# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market-vis test code v0.01
Market Visualization Prototype
Main script
"""

from datetime import datetime
import pandas as pd

from quotes import buildDailyPriceData, buildDummyData, createIndexedPricing
from visualization import visualizePrices
#from optimization import *

t0 = datetime.now() #Time the process
    
#Select Dates  
startDate = datetime.strptime('20120101', '%Y%m%d')
endDate = datetime.strptime('20130101', '%Y%m%d')

#Get data for S&P500 Constituents
SP500Constituents = pd.read_csv('SP500_constituents.csv')

#Use THIS line for online stock price building (do not use line 33)
#stockPrices = buildDailyPriceData(SP500Constituents['Symbol'], startDate, endDate)

#Use THIS line for offline testing (built from .csv file) (do not use line 30)
stockPrices = buildDummyData()

indexedPrices = createIndexedPricing(stockPrices, 100)

visualizePrices(indexedPrices)

print('Total time: ', (datetime.now() - t0))
print('End')
    