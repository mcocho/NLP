#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:03:42 2018

@author: mc

Creates a list with all the links to the pdf's with the locations of speed cameras
"""

## import packages
import urllib
import re
from bs4 import BeautifulSoup

# get html code from page
url = 'https://www.police.wa.gov.au/Traffic/Cameras/Camera-locations'
page = urllib.request.urlopen(url,timeout=10)

# parse html code and store html elements with links to pdf's in resSet
soup = BeautifulSoup(page,'html.parser')
resSet = soup.find_all(href=re.compile(".pdf"))

# extract link strings from resSet and store in list
linkTable = list()
for link in resSet:
    linkTable.append('https://www.police.wa.gov.au' + link.attrs.get('href'))
        
  
        