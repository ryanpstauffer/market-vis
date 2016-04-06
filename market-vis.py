# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

market-vis v0.01
Market Visualization Prototype
Main script
"""

import sys
from datetime import datetime
from timeit import default_timer as timer
import pandas as pd

from quotes import buildDailyPriceData, buildDummyData, createIndexedPricing
from visualization import visualizePrices, animateGIF


def main():
    programStart = timer()
        
    #Select Dates  
    startDate = datetime.strptime("20150101", "%Y%m%d")
    endDate = datetime.strptime("20160101", "%Y%m%d")
    
    #Get data for S&P500 Constituents
    SP500Constituents = pd.read_csv("SP500_constituents.csv")
    
    arg1 = str(sys.argv[1])
    if arg1 == "live":
        #Use for online stock price building, pulling from Google Finance API
        print("Pulling Data from Google Finance API")
        SP500StockPrices = buildDailyPriceData(SP500Constituents["Symbol"], startDate, endDate)
    
    elif arg1 == "test":
        #Use for offline testing (built from existing .csv file)
        print("Using Test Data from .csv")
        SP500StockPrices = buildDummyData()
        
    else:
        print("Type 'live' or 'test'")
        return 0
    
    dataPullEnd = timer()
    
    SP500IndexedPrices = createIndexedPricing(SP500StockPrices, 100)
    
    calcEnd = timer() #Doesn't include visualization in timer
    print("Data Pull Time: {0} sec".format(dataPullEnd - programStart))
    print("Calculation Time: {0} sec".format(calcEnd - dataPullEnd))
    
    visualizePrices(SP500IndexedPrices)
    
    #animateGIF('../images/prototype_animation.gif', SP500IndexedPrices)
    
    print('End')

if __name__ == "__main__":
    main()    
    
