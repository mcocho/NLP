#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging
import argparse
import numpy as np
import pandas as pd
import time


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(name)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("cam_alert")

__status__ = "Development"
__version__ = "0.0.1"


def parse_args():
    """Parses the command line options and arguments.

    Returns:
    argparse.Namespace: An object created by the :py:mod:`argparse` module. It
                        contains the values of the different options.

    """
    # Creating the parser object
    parser = argparse.ArgumentParser(
        description="This script simulates fluxes in an SBML model. "
                    "It requires a config file containing the parameters for "
                    "the simulation(s)."
    )
    # Path to config file
    parser.add_argument(
        "--config", '-c', type=str, metavar="CONFIG",
        required=True,
        help="The main CONFIG file",
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version="%(prog)s {}".format(__version__),
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=("INFO", "DEBUG"),
        default="INFO",
        help="The logging level [%(default)s]",
    )
    return parser.parse_args()


def main():
    '''
    main routine
    '''
    # Getting and checking the options
    args = parse_args()

    # Set log level:
    if args.log_level.lower() == 'debug':
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Reading config from file: {}".format(args.config))
    cr = ConfigReader(args.config)
    # Check config file contains all the required parameters
    cr.check_params(['log_file',
                     'database', 'main_url', 'pdf_folder'])
    config = cr.params

    # TODO:
    # [ ] get lastest date (entry) in db, get the current date -> get the missing pdfs from the url
    


if __name__ == "__main__":
    main()
