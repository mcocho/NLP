# import packages
import urllib
import re
from bs4 import BeautifulSoup

# get html code from page
url = 'https://www.police.wa.gov.au/Traffic/Cameras/Camera-locations'
page = urllib.request.urlopen(url,timeout=10)

# parse html code and find links to pdf files
soup = BeautifulSoup(page,'html.parser')
linkTable = soup.find_all(href=re.compile(".pdf"))
    