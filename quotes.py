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

#Clean up dependencies!!!!

from datetime import datetime, date
import pandas as pd
#import pandas_datareader.data as web
import json
import urllib  #Is this needed?

import urllib2


def getIntradayData(ticker, interval_seconds=61, num_days=10):
    # Specify URL string based on function inputs.
    urlString = 'http://www.google.com/finance/getprices?q={0}'.format(ticker.upper())
    urlString += "&i={0}&p={1}d&f=d,c".format(interval_seconds,num_days)
#    url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds,num_days)
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(urlString)).read()
    r = r.splitlines()
#    print(r)

    # Split each line by a comma, starting at the 8th line
    r = [line.split(',') for line in r[7:]]

    # Save data in Pandas DataFrame
    df = pd.DataFrame(r, columns=['Datetime',ticker])

    # Convert UNIX to Datetime format
    df['Datetime'] = df['Datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))
    df.index = df['Datetime']

    return df[ticker]

def getDailyData(ticker, startDate, endDate=date.today()):
    ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
    ticker = ticker.upper()
    #Make this more pythonic
#    start = startDate #date(int(startDate[0:4]),int(startDate[5:7]),int(startDate[8:10]))
#    end = endDate #date(int(endDate[0:4]),int(endDate[5:7]),int(endDate[8:10]))
    urlString = "http://www.google.com/finance/historical?q={0}".format(ticker)
    urlString += "&startdate={0}&enddate={1}&output=csv".format(
                      startDate.strftime('%b %d, %Y'),endDate.strftime('%b %d, %Y'))

    #Convert URL output ot dataframe
    df = pd.read_csv(urllib.urlopen(urlString))
    
    # Convert strings to Datetime format
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%d-%b-%y'))
    #Index by date    
    df.index = df[df.columns[0]]
    df.drop(df.columns[0], axis=1, inplace=True)
    
    return df


def getLastPrice(ticker):
    '''Returns last price and date time of a given ticker (from Google Finance API)'''
    #NEED TO MAKE THIS RETURN TIME, BUT WORKS FOR NOW...
    # Specify URL string based on function inputs.
    urlString = 'http://www.google.com/finance/info?client=ig&q={0}'.format(ticker.upper())
#    url_string += "&i={0}&p={1}d&f=d,c".format(interval_seconds,num_days)
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(urlString)).read()
    obj = json.loads(r[3:])
    print(obj)

    price = float(obj[0]['l'])
#    print(price)
#    ts = obj[0]['lt_dts']
#    print(ts)
#    ts=int(ts)
#    print(type(ts))
#    time = datetime.fromtimestamp(ts)
    
    return price
    
def buildDailyPriceData(tickerList, startDate, endDate):
    print('Pulling Market Data for S&P 500 from {0} to {1}'.format(startDate.strftime('%Y%m%d'), endDate.strftime('%Y%m%d')))
    #Build SP500 daily price data (for saving)
    firstTicker = tickerList[0]
    print(firstTicker)
    firstTickerData = getDailyData(firstTicker, startDate, endDate)
    firstTickerData.rename(columns={'Close' : firstTicker}, inplace = True)
    df = firstTickerData[firstTicker]
#    test2 = get_daily_data('GOOGL','2016-02-20')
#    new = pd.concat([test['AAPL'],test2['Close']], axis=1, join='outer')
    for ticker in tickerList[1:]:
        print(ticker)
        newTicker = getDailyData(ticker, startDate, endDate)
        if not newTicker.empty:
            newTicker.rename(columns={'Close' : ticker}, inplace = True)
            df = pd.concat([df, newTicker[ticker]], axis=1, join='outer')
#    print(df)
#    return df
    # Convert strings to Datetime format
#    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
#    df.index = df[df.columns[0]]
#    df.drop(df.columns[0], axis=1, inplace=True)
    
    #Build Price Table
    stockPrices = df.sort_index()
#    print(stockPrices)
    #FIX THIS
    #SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
#    stockPrices.dropna(axis=1, how='any', inplace=True)
    
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
    df = pd.read_csv('SP500_daily_price_data.csv')
    
    #Convert strings to Datetime format
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    df.index = df[df.columns[0]]
    df.drop(df.columns[0], axis=1, inplace=True)
    
    #Build Price Table
    stockPrices = df[startDate:endDate]
    #FIX THIS
    #SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
    stockPrices.dropna(axis=1, how='any', inplace=True)
    
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

  
if __name__ == '__main__':        
#    test = getIntradayData('AAPL',61,1)
#    test2 = getIntradayData('GOOGL',61,1)
#    new = pd.concat([test,test2], axis=1, join='outer')
    
    startDate = datetime.strptime('20150101', '%Y%m%d')    
    
    test = getDailyData('AAPL', startDate)
#    test.rename(columns={'Close' : 'AAPL'}, inplace = True)
#    test2 = getDailyData('GOOGL','2016-02-20')
#    new = pd.concat([test['AAPL'],test2['Close']], axis=1, join='outer')
##    last = getLastPrice('AAPL')


