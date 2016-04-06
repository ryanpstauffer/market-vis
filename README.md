# market-vis
Market Visualization Prototype

Generates a three-dimensional interactive surface of market data.

###Setup

Clone the repository, then install it:

`$ python setup.py install`

This installs the marketvis package, and allows you to run the program directly from the command line. 

Dependencies:
* Python 2.7
* Pandas
* Mayavi
* MoviePy

For more details about getting the prototype up and running, check out this [tutorial](https://github.com/ryanpstauffer/market-vis/wiki/Tutorial)

###Interface
Runs through a basic command line interface:

    marketvis [-h] [-v] mode [startDate] [endDate]

    positional arguments:
      mode           Running mode: live (online downloads) | test (offline test data)
      startDate      Start date of the live data pull (YYYYMMDD)
      endDate        End date of the live data pull (YYYYMMDD)
    
    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  Includes time printouts during runtime

###Test Option
`$ marketvis test`

Displays a visualization based on test data of S&P 500 stocks from Jan 1, 2012 to Jan 1, 2013.

###Live Option
`$ marketvis live 20150101 20160101`

Pulls new data from the Google Finance API and creates a more up-to-date visualization.





