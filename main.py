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
from timeit import default_timer as timer
import pandas as pd

from quotes import buildDailyPriceData, buildDummyData, createIndexedPricing
from visualization import visualizePrices, animateGIF

timerStart = timer()
    
#Select Dates  
startDate = datetime.strptime('20150101', '%Y%m%d')
endDate = datetime.strptime('20160101', '%Y%m%d')

#Get data for S&P500 Constituents
SP500Constituents = pd.read_csv('SP500_constituents.csv')

#Use THIS line for online stock price building (do not use line 33)
#SP500StockPrices = buildDailyPriceData(SP500Constituents['Symbol'], startDate, endDate)

#Use THIS line for offline testing (built from .csv file) (do not use line 30)
SP500StockPrices = buildDummyData()

SP500IndexedPrices = createIndexedPricing(SP500StockPrices, 100)

timerEnd = timer() #Doesn't include visualization in timer
print('Calculation time: {0} sec'.format(timerEnd - timerStart))

visualizePrices(SP500IndexedPrices)

#animateGIF('../images/prototype_animation.gif', SP500IndexedPrices)


print('End')
    
