# -*- coding: utf-8 -*-
"""
data.py

Created on Tue Feb 10 18:18:16 2015
@author: Ryan Stauffer

Data handling module for Market Visualization Software
"""
import numpy as np
import pandas as pd
from mayavi import mlab
import datetime
import pandas.io.sql as psql
import MySQLdb as mdb


def connect_MySQL(): 
    # Obtain a database connection to the MySQL instance
    print("Connecting to MySQL")
    db_host = 'localhost'
    db_user = 'stauffer'
    db_pass = 'violin'   #raw_input('Password: ')
    db_name = 'securities_master'
    con = mdb.connect(db_host, db_user, db_pass, db_name)
    return con

def get_returns(start, end=None):
    if end is None:
        end = start
    
    sql = """SELECT dp.price_date, sym.PERMNO, dp.return
         FROM symbol AS sym
         INNER JOIN daily_price AS dp
         ON dp.symbol_id = sym.id
         WHERE dp.price_date >= '%s' 
         AND dp.price_date <= '%s'
         ORDER BY sym.PERMNO ASC;""" % (start, end)
        
    ret = psql.frame_query(sql, con=connect_MySQL(), index_col='PERMNO')
    return ret
    
def get_specific_returns(ticker, start, end=None, con = None):
    if end is None:
        end = start
    if con is None:
        con = connect_MySQL()
    
    sql = """SELECT dp.price_date, dp.return
         FROM symbol AS sym
         INNER JOIN daily_price AS dp
         ON dp.symbol_id = sym.id
         WHERE sym.PERMNO = '%s'
         AND dp.price_date >= '%s' 
         AND dp.price_date <= '%s'
         ORDER BY dp.price_date ASC;""" % (ticker, start, end)
        
    ret = psql.frame_query(sql, con=con, index_col='price_date')
    return ret


def total_returns_chart(stock_rets):
    t0 = datetime.datetime.now()
    #Assemble x and y grids
    print('Building Model')
    stock_list = list(set(stock_rets.index))
    stocks = list(range(len(stock_list)))
    
    dates = list(set(stock_rets.price_date))
    dates.sort()
#    print(dates)
    print('Dimensions: %s stocks for %s days' % (len(stock_list), len(dates)))
    
    x = np.array([list(xrange(len(dates)+1)),]*len(stocks)).transpose()
    y = np.array([stocks,]*(len(dates)+1))

    z = np.zeros(((len(dates)+1),len(stocks)))
    start = 100
    z[0,] = start
    #Assemble z grid
    for i in stocks:
#        print(i)
        s_lookup = stock_list[i]
        for j in range(1,(len(dates)+1)):
#            print(j)
            d_lookup = dates[j-1]
    #            print(d_lookup)
            sliced = stock_rets.loc[s_lookup]
    #            print(sliced[sliced.price_date == d_lookup]['return'])
            try:
                z[j,i] = z[(j-1),i] * (1 +float(sliced[sliced.price_date == d_lookup]['return']))
            except:
                z[j,i] = z[(j-1),i]
                
    print('Model build time: ', (datetime.datetime.now() - t0))
    return x, y, z
    
def daily_returns_chart(stock_rets):
    #Assemble x and y grids
    print('Building Model')
    stock_list = list(set(stock_rets.index))
    stocks = list(range(len(stock_list)))
    
    dates = list(set(stock_rets.price_date))
    dates.sort()
#    print(dates)
    print('Dimensions: %s stocks for %s days' % (len(stock_list), len(dates)))
    
    x = np.array([list(xrange(len(dates))),]*len(stocks)).transpose()
    y = np.array([stocks,]*len(dates))

    z = np.zeros((len(dates),len(stocks)))
    
    #Assemble z grid
    for i in stocks:
#        print(i)
        s_lookup = stock_list[i]
        for j in xrange(len(dates)):
    #            print(j)
            d_lookup = dates[j]
    #            print(d_lookup)
            sliced = stock_rets.loc[s_lookup]
    #            print(sliced[sliced.price_date == d_lookup]['return'])
            try:
                z[j,i] = float(sliced[sliced.price_date == d_lookup]['return'])
            except:
                z[j,i] = 0
                
    return x, y, z

def new_daily_returns(stock_list, startdate, enddate, con):
    ret_matrix = pd.DataFrame()
    
    for s in xrange(len(stock_list)):
        print(s)
        ticker = (stock_list[s])
        print(ticker)
        rets = get_specific_returns(ticker, startdate, enddate, con)
        rets.rename(columns={'return':ticker}, inplace=True)
        print rets.index
        ret_matrix = pd.concat((ret_matrix, rets), axis=1)
    #    print(rets)
    print(ret_matrix)
    
    x_length, y_length = ret_matrix.shape
    x = np.array([list(xrange(x_length)),]*y_length).transpose()
    y = np.array([ret_matrix.columns,]*y_length)
    z = ret_matrix
    
    return x, y, z

def new_total_returns(stock_list, startdate, enddate, con):
    x, y, ret_matrix = new_daily_returns(stock_list, startdate, enddate, con)
    
    tot_ret_matrix = ret_matrix + 1
    tot_ret_matrix.iloc[0] = 100
    z = tot_ret_matrix.cumprod(axis=0)

    #sort z by total return
    last_date = z.iloc[-1]
    last_date.sort()
    sort_order = last_date.index
    z = z[sort_order]
    
    return x, y, z