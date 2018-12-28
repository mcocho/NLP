#!/usr/bin/env python

from datetime import date, datetime
import sqlite3
import time
import logging
import sys
import os

from main import parse_args
from utils import ConfigReader, query_yes_no

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(name)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("create_db")

__status__ = "Development"
__version__ = "0.0.1"

desc = """ This script creates an empty sqlite database.
"""

# Hold the table descriptions in a dict, in case we create multiple tables
# Note: sqlite doesn not have built-in date/time function so we store the dates
# as TEXT
tables = {
    'camera' : '''
    CREATE TABLE camera(
    id INTEGER PRIMARY KEY,
    date TEXT,
    day TEXT,
    street TEXT,
    surburn TEXT,
    date_added  TIMESTAMP DEFAULT (DATETIME(current_timestamp, 'localtime')))
    ''',
}


def create_db(database):
    db = sqlite3.connect(database)
    # This lock the database:
    # ( see http://stackoverflow.com/questions/8828495/how-to-lock-a-sqlite3-database-in-python
    with db:
        cursor = db.cursor()
        for tb_name, create_statement in tables.items():
            cursor.execute('drop table if exists %s'%tb_name)
            logger.info ("Creating table : %s"%tb_name)
            cursor.execute(create_statement)
            db.commit()
    db.close()


if __name__ == "__main__":
    args = parse_args()
    args.description = desc
    # Set log level:
    if args.log_level.lower() == 'debug':
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Reading config from file: {}".format(args.config))
    cr = ConfigReader(args.config)
    # Check config file contains all the required parameters
    cr.check_params(['database'])
    config = cr.params

    logger.debug("Checking if db {} already exists".format(config.database))
    if os.path.isfile(config.database):
        logger.info("DB {} already exists and will be overwritten")
        if not query_yes_no("Continue ?"):
            sys.exit(0)

    logger.info("Create the database: {}".format(config.database))
    create_db(config.database)

    logger.debug("Checking if pdf directory {} exists".format(config.pdf_folder))
    populate_db = False
    if os.path.isdir(config.pdf_folder):
        pdfs = get_list_of_files(config.pdf_folder, extension='pdf')
        logger.info("\t {} pdf files found")
        populate_db = query_yes_no("Do you want to populate the database ?")

    if populate_db:
        pass
        # TODO: write download_pdfs.py to download all the pdfs available
        # TODO: parse pdf and insert into db

    logger.info("Finished")
    #create_db()
