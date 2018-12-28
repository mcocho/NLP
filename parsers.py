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
    def __init__(self):
        pass
