import urllib
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
import tabula
import logging
import datetime
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


    def download_file(self, download_url, output_file):
        urllib.request.urlretrieve(download_url, output_file)

class pdf_parser():

    # TODO: add a check to compare the number of tables (days) and the
    # number of days from the date (infered from filename) and make sure
    # they match

    def __init__(self, filename, folder):
        self.filename = filename
        self.folder = folder

        self.fullpath = os.path.join(folder,filename)
        if not os.path.isfile(self.fullpath):
            logger.critical("Error: pdf {} does not exist".format(self.fullpath))

        self.set_date_from_filename()

        self.start_date = None
        self.stop_date = None
        self.n_tables = 0
        self.data = None # df containing the data


    def load_pdf(self):
        # Read the main pdf and put all the tables into a list
        # Note: lattice=True is required for multiline per cell

        dfs_raw = tabula.read_pdf(self.fullpath,
                                pages='all',
                                encoding='utf-8',
                                #lattice=True,
                                multiple_tables=True)
        self.n_tables = len(dfs_raw)
        logging.debug('\t{} tables found'.format(self.n_tables))
        dfl = []
        for d in dfs_raw:
            # First row containg the date
            date = pd.to_datetime(d.iloc[0][0])
            if date =='NaT':
                print(df)
            d = d.reindex(d.index.drop(0)) # Remove the first row
            # Each df consists of 4 columns, split and concat
            A = d[[0,1]]
            B = d[[2,3]]

            # First row = Street, Surburb
            A.columns = A.iloc[0]
            A = A.drop(A.index[0])

            B.columns = B.iloc[0]
            B = B.drop(B.index[0])

            C = pd.concat([A,B])
            C['Date'] = date
            C = C[~C.isna()] # Remove NA

            for d in [A,B, C]:
                if (('Street Name' not in d.columns ) or
                    ('Suburb' not in d.columns)):
                    logger.critical("Malformated dataframe {}".format(d.head()))
            dfl.append(C)

        self.data = pd.concat(dfl)
        logging.debug('\t{} entries'.format(self.data.shape[0]))

    def set_date_from_filename(self):
        """
        MediaLocations-31122018-to-06012019.pdf to dates
        """
        m = os.path.basename(self.fullpath)
        m = m.replace('.pdf','') # remove ext
        l = m.split('-')

        if len(l) != 4:
            logger.critical("Malformated filename: '{}'".format(m))
        start_str, stop_str = l[1], l[3]
        logging.debug('{}\tstart: {}\tstop: {}'.format(m,start_str, stop_str))
        self.start_date = datetime.datetime.strptime(start_str, "%d%m%Y").date()
        self.stop_date = datetime.datetime.strptime(stop_str, "%d%m%Y").date()
