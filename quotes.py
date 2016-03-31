# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Wed Dec 16 22:44:15 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

This module based initially on http://www.theodor.io/scraping-google-finance-data-using-pandas/
Market Visualization Prototype
"""

#Clean up dependencies!!!!

from datetime import datetime, date
import pandas as pd
#import pandas_datareader.data as web
import json
import urllib

import urllib2


#Specify date range
start = datetime(2015,12,1)
end = datetime.today()

#specify symbol
symbol = 'AAPL'

#aapl_from_google = web.DataReader('{0}google{1}{2}'.format(symbol, start, end))

#aapl_from_google = web.DataReader("%s" % symbol, 'google', start, end)


def get_intraday_data(symbol, interval_seconds=61, num_days=10):
    # Specify URL string based on function inputs.
    url_string = 'http://www.google.com/finance/getprices?q={0}'.format(symbol.upper())
    url_string += "&i={0}&p={1}d&f=d,c".format(interval_seconds,num_days)
#    url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds,num_days)
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(url_string)).read()
    r = r.splitlines()
#    print(r)

    # Split each line by a comma, starting at the 8th line
    r = [line.split(',') for line in r[7:]]

    # Save data in Pandas DataFrame
    df = pd.DataFrame(r, columns=['Datetime',symbol])

    # Convert UNIX to Datetime format
    df['Datetime'] = df['Datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))
    df.index = df['Datetime']

    return df[symbol]

def get_daily_data(symbol, start_date, end_date=date.today().isoformat()):
    ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
    symbol = symbol.upper()
    start = date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    url_string = "http://www.google.com/finance/historical?q={0}".format(symbol)
    url_string += "&startdate={0}&enddate={1}&output=csv".format(
                      start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))

    #Convert URL output ot dataframe
    df = pd.read_csv(urllib.urlopen(url_string))
    
    # Convert strings to Datetime format
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: datetime.strptime(x, '%d-%b-%y'))
    #Index by date    
    df.index = df[df.columns[0]]
    df.drop(df.columns[0], axis=1, inplace=True)
    
    return df


def get_last_price(symbol):
    
    #NEED TO MAKE THIS RETURN TIME, BUT WORKS JANKILY FOR NOW...
    #Returns last price and date time of a given symbol (from Google Finance API)
    # Specify URL string based on function inputs.
    url_string = 'http://www.google.com/finance/info?client=ig&q={0}'.format(symbol.upper())
#    url_string += "&i={0}&p={1}d&f=d,c".format(interval_seconds,num_days)
    
    # Request the text, and split by each line
    r = urllib2.urlopen(urllib2.Request(url_string)).read()
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
    
if __name__ == '__main__':        
#    test = get_intraday_data('AAPL',61,1)
#    test2 = get_intraday_data('GOOGL',61,1)
#    new = pd.concat([test,test2], axis=1, join='outer')
    
    test = get_daily_data('AAPL','2016-02-20')
    test.rename(columns={'Close' : 'AAPL'}, inplace = True)
    test2 = get_daily_data('GOOGL','2016-02-20')
    new = pd.concat([test['AAPL'],test2['Close']], axis=1, join='outer')
#    last = get_last_price('AAPL')


