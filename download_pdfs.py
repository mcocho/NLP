#!/usr/bin/env python

from datetime import date, datetime
import sqlite3
import time
import logging
import sys
import os
import urllib

from main import parse_args
from utils import ConfigReader, query_yes_no
from parsers import html_parser

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(name)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("download_pdfs")

__status__ = "Development"
__version__ = "0.0.1"

desc = """ Download the raw pdfs
"""

if __name__ == "__main__":
    args = parse_args()
    args.description = desc
    # Set log level:
    if args.log_level.lower() == 'debug':
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Reading config from file: {}".format(args.config))
    cr = ConfigReader(args.config)
    # Check config file contains all the required parameters
    cr.check_params(['main_url', 'pdf_folder'])
    config = cr.params

    logger.info("Getting pdf documents from url: {}".format(config.main_url))
    hp = html_parser(url=config.main_url, download_directory=config.pdf_folder)
    hp.parse_page()
    logger.info("\t {} pdf documents found".format(len(hp._pdf_links)))

    # Check if destination directory exist"
    if not os.path.isdir(config.pdf_folder):
        logger.info("Destination directory {} does not exist "
                    "and will be created".format(config.pdf_folder))
        os.mkdir(config.pdf_folder)
    else:
        logger.warn("Destination directory {} exists".format(config.pdf_folder))

    logger.info("Start downloading")
    for link in hp._pdf_links:
        # get the filenames:
        fn = link.split("/")[-1]
        destination = os.path.join(config.pdf_folder, fn)
        logger.debug("Saving file {} to {} (url:{})".format(fn,
                                                            destination,
                                                            link))
        hp.download_file(link, destination)

    # TODO:
        # Generate filenames for past week to get historical data
