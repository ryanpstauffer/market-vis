# market-vis
Market Visualization Prototype

Generates a three-dimensional interactive surface of market data.

Runs through a basic command line interface:

    marketvis.py [-h] [-v] mode [startDate] [endDate]

    positional arguments:
      mode           Running mode: live (online downloads) | test (offline test
                     data)
      startDate      Start date of the live data pull (YYYYMMDD)
      endDate        End date of the live data pull (YYYYMMDD)
    
    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  Includes time printouts during runtime

###Test Option
`python marketvis.py test`

Displays a visualization based on test data of S&P 500 stocks from Jan 1, 2012 to Jan 1, 2013.

###Live Option
`python marketvis.py live 20150101 20160101`

Pulls new data from the Google Finance API and creates a more up-to-date visualization.

For details about getting the prototype up and running, check out this [tutorial](https://github.com/ryanpstauffer/market-vis/wiki/Tutorial)




