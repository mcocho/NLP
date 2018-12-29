import urllib
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
import tabula
import logging
logger = logging.getLogger(__name__)

class html_parser(object):
    def __init__(self, url=None,
                 download_directory=None):
        self.url = url
        self.download_directory = download_directory

        self._page = None
        self._pdf_links = []

    def parse_page(self):

        self._page = urllib.request.urlopen(self.url,
                                      timeout=10)
        # parse html code and store html elements with links to pdf's in resSet
        soup = BeautifulSoup(self._page,'html.parser')
        resSet = soup.find_all(href=re.compile(".pdf"))
        u = urllib.parse.urlparse(self.url)
        # extract link strings from resSet and store in list

        for link in resSet:
            s = "{}://{}{}".format(u.scheme, u.hostname, link.attrs.get('href'))
            # TODO: better use a proper regex here
            s = s.replace('?la=en', '')
            self._pdf_links.append(s)




class pdf_parser():
    def __init__(self, path=None, dataBase=None):
        
        self.path = path
        self.dataBase = dataBase

        self.speedCamWk1 = None
        self.speedCamWk2 = None

    def parse_pdf(self):
        
        ## read tables from pdf, assuming the 1st one is located in the 1st half of the page
        # and that the seconc one is located in the second half. tabula is being fiddly, so 
        # 1st column name of the table is the date, and the 1st row is 
        # "street name, suburb, street name, suburb", the next rows are the actual street names/suburbs
        #TODO:
        # could use pass read_pdf a template here, to make this cleaner.
        self.speedCamWk1 = tabula.read_pdf(self.path,relative_area=True,area=(0,0,50,100))
        self.speedCamWk2 = tabula.read_pdf(self.path,relative_area=True,area=(50,0,100,100))

        #TODO:
        #write to database

