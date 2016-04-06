# -*- coding: utf-8 -*-
"""

[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Wed Apr  6 14:10:13 2016
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market Visualization Prototype
marketvis.__main__: executed when marketvis directory is called as script
"""

import argparse
from .marketvis import main

parser = argparse.ArgumentParser(description="Market Visualization Tool")
parser.add_argument("mode", metavar="mode", choices=["live", "test"], default="test",
                    help="Running mode: live (online downloads) | test (offline test data)")
parser.add_argument("startDate", nargs='?', type=str, default="20150101",
                    help="Start date of the live data pull (YYYYMMDD)")
parser.add_argument("endDate", nargs='?', type=str, default="20160101",
                    help="End date of the live data pull (YYYYMMDD)")  
parser.add_argument("-v", "--verbose", action="store_true", 
                    help="Includes time printouts during runtime")
args = parser.parse_args()
main(args.mode, args.startDate, args.endDate, args.verbose)
