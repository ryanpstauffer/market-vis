# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('marketvis/__init__.py').read(),
    re.M
    ).group(1)
 
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "market-vis",
    packages = ["marketvis"],
    package_data = {"marketvis":["Resources/*.csv"]},
    entry_points = {
        "console_scripts": ["marketvis = marketvis.marketvis:main"]
        },
    version = version,
    description = "Python Market Visualization Prototype",
    long_description = long_descr,
    author = "Ryan Stauffer",
    author_email = "ryan.p.stauffer@gmail.com",
    url = "http://ryanpstauffer.github.io/market-vis/",
    )
