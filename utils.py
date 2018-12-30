import os
import sys
import logging
from collections import defaultdict
from pathlib import Path
import logging
import subprocess
import pandas as pd
import itertools

logger = logging.getLogger(__name__)
import re

class ProgramError(Exception):
    """An :py:class:`Exception` raised in case of a problem.

    :param msg: the message to print to the user before exiting.
    :type msg: string

    """
    def __init__(self, msg):
        """Construction of the :py:class:`ProgramError` class.

        :param msg: the message to print to the user
        :type msg: string

        """
        self.message = str(msg)

    def __str__(self):
        """Creates a string representation of the message."""
        return self.message


class ConfigReader():
    """
    Class for reading and managing configuration files. This class is useful
    to load python files as config files. It offers a maximum of flexibility
    but is not recommended: modifying sys.path dynamically is never a good idea
    and it can be dangerous.
    """
    def __init__(self, config_file):

        logger.debug("Checking if config file {} exists".format(config_file))
        if not os.path.isfile(config_file):
            logger.error("Config file  %s cannot be found"%(config_file))
            sys.exit(0)

        self.config_file = config_file
        p = Path(config_file)
        p = p.resolve()
        sys.path.append(str(p.parent))
        try:
            self.params =  __import__(p.stem)

        except ProgramError as e:
                logger.error("Fail to import config from: %s\n%s"%(config_file,
                                                                   e.message))
                sys.exit(0)

    def check_params(self, required_parameters=[]):
        """
        Check the presence of mandatory paramaneters in the config file.

        :param required_parameters: list of required paramaters (str)
        :type required_parameters: list

        """
        for rp in required_parameters:
            if not hasattr(self.params, rp):
                logger.error("'{}' parameter not found in config"
                             " file {}".format(rp, self.config_file))
                sys.exit(0)
        return True

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    from: https://code.activestate.com/recipes/577058/
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        #sys.stdout.write(question + prompt)
        logger.info(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            logger.critical("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_list_of_files(directory, extension=False):
    """
    Return a list of files from a given directory. The list can be filtered by
    specifying strings for 'extension'
    """
    logger.debug("Scanning folder {}".format(directory))
    raw = os.listdir(directory)
    logger.debug("{} files found".format(len(raw)))

    to_keep = []
    if extension:
        logger.debug("Filtering file with extension: {}".format(extension))
        for f in raw:
            if f.endswith(extension):
                to_keep.append(f)
    else:
        to_keep = raw

    logger.debug("{} files remaining".format(len(to_keep)))
    return to_keep
