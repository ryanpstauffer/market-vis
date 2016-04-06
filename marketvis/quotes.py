# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Wed Dec 16 22:44:15 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

[This module referenced http://www.theodor.io/scraping-google-finance-data-using-pandas/]
Market Visualization Prototype
Quotes Module
"""

from datetime import datetime, date
import pandas as pd
import json
import urllib
import urllib2
import os

def getIntradayData(ticker, interval_seconds=61, num_days=10):
    # Specify URL string based on function inputs.
    urlString = 'http://www.google.com/finance/getprices?q={0}'.format(ticker.upper())
    urlString += "&i={0}&p={1}d&f=d,c".format(interval_seconds,num_days)
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(urlString)).read()
    r = r.splitlines()

    # Split each line by a comma, starting at the 8th line
    r = [line.split(',') for line in r[7:]]

    # Save data in Pandas DataFrame
    df = pd.DataFrame(r, columns=['Datetime',ticker])

    # Convert UNIX to Datetime format
    df['Datetime'] = df['Datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))
    df.index = df['Datetime']

    return df[ticker]

def getDailyData(ticker, startDate, endDate=date.today()):
    ''' Daily quotes from Google Finance API. Date format='yyyy-mm-dd' '''
    ticker = ticker.upper()
    urlString = "http://www.google.com/finance/historical?q={0}".format(ticker)
    urlString += "&startdate={0}&enddate={1}&output=csv".format(
                      startDate.strftime('%b %d, %Y'),endDate.strftime('%b %d, %Y'))

    #Convert URL output to dataframe
    df = pd.read_csv(urllib.urlopen(urlString))
    
    # Convert strings to Datetime format
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%d-%b-%y'))
    
    #Index by date    
    df.index = df[df.columns[0]]
    df.drop(df.columns[0], axis=1, inplace=True)
    
    return df


def getLastPrice(ticker):
    '''Returns last price and date time of a given ticker (from Google Finance API)'''
    # Specify URL string based on function inputs.
    urlString = 'http://www.google.com/finance/info?client=ig&q={0}'.format(ticker.upper())
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(urlString)).read()
    obj = json.loads(r[3:])
    print(obj)

    price = float(obj[0]['l'])
    
    return price
    
def buildDailyPriceData(tickerList, startDate, endDate):
    print('Pulling Market Data for S&P 500 from {0} to {1}'.format(startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))
    #Build SP500 daily price data (for saving)
    firstTicker = tickerList[0]
    print(firstTicker)
    firstTickerData = getDailyData(firstTicker, startDate, endDate)
    firstTickerData.rename(columns={'Close' : firstTicker}, inplace = True)
    df = firstTickerData[firstTicker]

    for ticker in tickerList[1:]:
        print(ticker)
        newTicker = getDailyData(ticker, startDate, endDate)
        if not newTicker.empty:
            newTicker.rename(columns={'Close' : ticker}, inplace = True)
            df = pd.concat([df, newTicker[ticker]], axis=1, join='outer')
    
    #Google returns data w/ most recent at the top, this puts data in chrono order
    stockPrices = df.sort_index()
    
    print('Pulled data for {0} stocks from {1} to {2}'.format(len(stockPrices.columns), startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))

    return stockPrices

def buildDummyData():
    '''Builds Daily Price Data from a backup .csv file
    Used for offline testing purposes
    '''
    
    #Select Dates  
    startDate = datetime.strptime('20120101', '%Y%m%d')
    endDate = datetime.strptime('20130101', '%Y%m%d')

    #Load dataset from .csv
    print("Pulling Market Data from .csv")
    dataLoc = os.path.join(os.path.dirname(__file__),"Resources/SP500_daily_price_data.csv")
    df = pd.read_csv(dataLoc)
    
    #Convert strings to Datetime format
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    df.index = df[df.columns[0]]
    df.drop(df.columns[0], axis=1, inplace=True)
    
    #Build Price Table
    stockPrices = df[startDate:endDate]
    
    print('Pulled data for {0} stocks from {1} to {2}'.format(len(stockPrices.columns), startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))
    return stockPrices 

def createIndexedPricing(stockPrices, startingIndexValue):
    '''Takes a stock prices tables and converts to indexed pricing
    (i.e. all prices are relative based on a common starting index value)
    Inputs:
    stockPrices => a panda DataFrame
    startingIndexValue => the value that all prices will start at
    '''
    #Build Returns Table
    stockReturns = stockPrices.pct_change(1)  
    
    #Build Indexed Price Table (indexed to 100)
    indexedPrices = stockReturns + 1
    indexedPrices.iloc[0] = startingIndexValue
    indexedPrices = indexedPrices.cumprod(axis=0)
    
    return indexedPrices